# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

from aws_crt import mqtt
from awsiot import MqttServiceClient, iotshadow, iotjobs
from concurrent.futures import Future
from functools import partial
from threading import RLock
from typing import Callable, Dict
from uuid import uuid1


CLIENT_TOKEN_ATTR = "client_token"


class _MqttRpcServiceClient(object):
    """
    This class hides the complexity of performing RPCs over the MQTT's
    publish/subscribe architecture.
    """

    def __init__(self, mqtt_service_client):
        self._lock = RLock()  # type: RLock
        self._topic_entries = {}  # type: Dict[str, _RpcTopicEntry]
        self._mqtt_service_client = mqtt_service_client  # type: MqttServiceClient

    def unsubscribe(self, topic):
        # type: (str) -> Future
        """
        Tell the MQTT server to stop sending messages to this topic.

        Returns a `Future` whose result will be `None` when the server
        has acknowledged the unsubscribe.
        """
        return self._mqtt_service_client.unsubscribe(topic)

    def _start_rpc(
        self, pub_op, pub_request, sub_accepted_op, sub_rejected_op, sub_request
    ):
        future = Future()

        # Since this function returns a future, stuff any exceptions in there.
        try:
            for slot in sub_request.__slots__:
                if not getattr(sub_request, slot, None):
                    raise ValueError("request.{} is required".format(slot))

            topic_key = "{} {}".format(pub_op.__name__, repr(sub_request))

            uses_client_token = CLIENT_TOKEN_ATTR in pub_request.__slots__
            if uses_client_token:
                setattr(pub_request, CLIENT_TOKEN_ATTR, str(uuid1()))

            rpc_operation = _RpcOperation(pub_op, pub_request, topic_key, future)

        except Exception as e:
            future.set_exception(e)
            return future

        # These are things we might do once lock is released
        should_publish_now = False
        suback_futures_needing_callbacks = []
        fail_now_reason = None

        # Hold lock while mutating topic entries.
        with self._lock:
            try:
                entry = self._topic_entries.get(topic_key)
                if entry:
                    # Entry already exists, so subscriptions have already
                    # been issued. If pending subscriptions have completed,
                    # publish the request immediately.
                    entry.pending_operations.append(rpc_operation)
                    if not entry.pending_suback_futures:
                        should_publish_now = True

                else:
                    # Create entry and subscribe to its response topics.
                    entry = _RpcTopicEntry(uses_client_token)
                    entry.pending_operations.append(rpc_operation)
                    self._topic_entries[rpc_operation.topic_key] = entry
                    for sub_op_i in (sub_accepted_op, sub_rejected_op):
                        sub_future, sub_topic = sub_op_i(
                            sub_request, partial(self._on_response, topic_key)
                        )
                        suback_futures_needing_callbacks.append(sub_future)
                        entry.pending_suback_futures.append(sub_future)
                        entry.subscribed_topics.append(sub_topic)

            except Exception as e:
                self._remove_rpc(rpc_operation)
                fail_now_reason = e

        # With lock released
        if should_publish_now:
            self._publish_with_lock_released(rpc_operation)

        for suback_i in suback_futures_needing_callbacks:
            suback_i.add_done_callback(partial(self._on_suback, topic_key))

        if fail_now_reason is not None:
            self._complete_rpc_with_lock_released(rpc_operation, fail_now_reason)

        return future

    def _on_suback(self, topic_key, suback_future):
        operations_to_complete = []
        operations_to_publish = []

        with self._lock:
            try:
                entry = self._topic_entries[topic_key]
                entry.pending_suback_futures.remove(suback_future)
            except (KeyError, ValueError):
                # Do nothing, this suback must correspond to some
                # old entry that's already been dealt with.
                return

            if suback_future.exception():
                # Couldn't subscribe. Remove the topic entry and
                # mark all its pending operations as failures.
                operations_to_complete.extend(entry.pending_operations)
                for operation_i in operations_to_complete:
                    self._remove_rpc(operation_i)
            else:
                # Subscribed. If this was the last pending subscription,
                # all the operations can publish their requests now.
                if not entry.pending_suback_futures:
                    operations_to_publish.extend(entry.pending_operations)

        # With lock released
        for operation_i in operations_to_complete:
            self._complete_rpc_with_lock_released(operation_i, suback_future)

        for operation_i in operations_to_publish:
            self._publish_with_lock_released(operation_i)

    def _publish_with_lock_released(self, rpc_operation):
        """Should not be called while holding the lock"""
        try:
            pub_future = rpc_operation.pub_op(rpc_operation.pub_request)
            pub_future.add_done_callback(partial(self._on_puback, rpc_operation))
        except Exception as e:
            self._remove_rpc(rpc_operation)
            self._complete_rpc_with_lock_released(rpc_operation, e)

    def _on_puback(self, rpc_operation, pub_future):
        if pub_future.exception():
            self._remove_rpc(rpc_operation)
            self._complete_rpc_with_lock_released(rpc_operation, pub_future)

    def _on_response(self, topic_key, response):
        corresponding_operation = None
        with self._lock:
            entry = self._topic_entries.get(topic_key)
            if entry:
                if entry.uses_client_token:
                    # Find operation with matching token
                    response_token = getattr(response, CLIENT_TOKEN_ATTR, None)
                    if response_token:
                        for operation_i in entry.pending_operations:
                            if operation_i.client_token() == response_token:
                                corresponding_operation = operation_i
                                break
                else:
                    # Assume response is to the oldest operation
                    corresponding_operation = entry.pending_operations[0]

            if corresponding_operation:
                self._remove_rpc(corresponding_operation)

        # With lock released
        if corresponding_operation:
            self._complete_rpc_with_lock_released(corresponding_operation, response)

    def _remove_rpc(self, rpc_operation):
        """
        Remove operation from its topic entry. Once all operations in an entry
        are complete, the entry is removed its topics are unsubscribed from.
        """
        with self._lock:
            entry = self._topic_entries.get(rpc_operation.topic_key)
            if entry:
                # Remove operation from the entry.
                try:
                    entry.pending_operations.remove(rpc_operation)
                except ValueError:
                    return

                # If no operations remain in the entry,
                # remove the entry and unsubscribe from its topics.
                if not entry.pending_operations:
                    del self._topic_entries[rpc_operation.topic_key]
                    for topic in entry.subscribed_topics:
                        # If unsubscribe fails it just means we weren't
                        # subscribed to begin with.
                        try:
                            self.unsubscribe(topic)
                        except:
                            pass

    def _complete_rpc_with_lock_released(self, operation, result):
        """
        Set the result of the operation. This should be called with the lock
        released, to avoid the possibility of callbacks firing which set up a
        chain of events resulting in deadlock.
        """

        # If result is a Future, extract its contents
        if isinstance(result, Future):
            try:
                result = result.result()
            except Exception as e:
                result = e

        # Let subclasses transform results
        result = self._transform_result(result)

        if not operation.future.done():
            if isinstance(result, Exception):
                operation.future.set_exception(result)
            else:
                operation.future.set_result(result)

    def _transform_result(self, result):
        return result


class _RpcTopicEntry(object):
    """A set of _RpcOperations which are subscribed to identical topics."""

    __slots__ = (
        "pending_operations",
        "subscribed_topics",
        "pending_suback_futures",
        "uses_client_token",
    )

    def __init__(self, uses_client_token):
        self.pending_operations = []  # type: List[_RpcOperation]
        self.subscribed_topics = []  # type: List[str]
        self.pending_suback_futures = []  # type: List[Future]
        self.uses_client_token = uses_client_token  # type: bool


class _RpcOperation(object):
    """An operation within an _RpcTopicEntry."""

    __slots__ = ("pub_op", "pub_request", "topic_key", "future")

    def __init__(self, pub_op, pub_request, topic_key, future):
        self.pub_op = pub_op
        self.pub_request = pub_request
        self.topic_key = topic_key  # type: str
        self.future = future  # type: Future

    def client_token(self):
        return getattr(self.pub_request, CLIENT_TOKEN_ATTR, None)


class JobsErrorResponse(Exception):
    """Exception for when the server responds with a rejection of the request."""
    def __init__(self, response):
        self.response = response  # type: iotjobs.RejectedError


class IotJobsRpcClient(_MqttRpcServiceClient):
    """
    This alternative to the `IoTJobsClient` handles the complexity of
    performing RPCs (remote procedure calls) over the MQTT's
    publish/subscribe architecture.
    """

    def __init__(self, mqtt_connection):
        # type: (mqtt.Connection) -> None
        super(IotJobsRpcClient, self).__init__(iotjobs.IotJobsClient(mqtt_connection))
        self._jobs_client = self._mqtt_service_client  # type: iotshadow.IotJobsClient

    def describe_job_execution(self, request):
        # type(iotjobs.DescribeJobExecutionRequest) -> Future
        """
        Gets detailed information about a job execution.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionRequest` instance.

        Returns a `Future` which will contain a result of `DescribeJobExecutionResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._jobs_client.publish_describe_job_execution,
            pub_request=request,
            sub_accepted_op=self._jobs_client.subscribe_to_describe_job_execution_accepted,
            sub_rejected_op=self._jobs_client.subscribe_to_describe_job_execution_rejected,
            sub_request=iotjobs.DescribeJobExecutionSubscriptionRequest(
                job_id=request.job_id, thing_name=request.thing_name
            ),
        )

    def get_pending_job_executions(self, request):
        # type(iotjobs.GetPendingJobExecutionsRequest) -> Future
        """
        Gets the list of all jobs for a thing that are not in a terminal state.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsRequest` instance.

        Returns a `Future` which will contain a result of `GetPendingJobExecutionsResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._jobs_client.publish_get_pending_job_executions,
            pub_request=request,
            sub_accepted_op=self._jobs_client.subscribe_to_get_pending_job_executions_accepted,
            sub_rejected_op=self._jobs_client.subscribe_to_get_pending_job_executions_rejected,
            sub_request=iotjobs.GetPendingJobExecutionsSubscriptionRequest(
                thing_name=request.thing_name
            ),
        )

    def start_next_pending_job_execution(self, request):
        # type(iotjobs.StartNextPendingJobExecutionRequest) -> Future
        """
        Gets and starts the next pending job execution for a thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionRequest` instance.

        Returns a `Future` which will contain a result of `StartNextPendingJobExecutionResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._jobs_client.publish_start_next_pending_job_execution,
            pub_request=request,
            sub_accepted_op=self._jobs_client.subscribe_to_start_next_pending_job_execution_accepted,
            sub_rejected_op=self._jobs_client.subscribe_to_start_next_pending_job_execution_rejected,
            sub_request=iotjobs.StartNextPendingJobExecutionSubscriptionRequest(
                thing_name=request.thing_name
            ),
        )

    def update_job_execution(self, request):
        # type(iotjobs.UpdateJobExecutionRequest) -> Future
        """
        Updates the status of a job execution.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionRequest` instance.

        Returns a `Future` which will contain a result of `UpdateJobExecutionResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._jobs_client.publish_update_job_execution,
            pub_request=request,
            sub_accepted_op=self._jobs_client.subscribe_to_update_job_execution_accepted,
            sub_rejected_op=self._jobs_client.subscribe_to_update_job_execution_rejected,
            sub_request=iotjobs.UpdateJobExecutionSubscriptionRequest(
                job_id=request.job_id, thing_name=request.thing_name
            ),
        )

    def subscribe_to_job_executions_changed_events(self, request, on_event):
        # type: (JobExecutionsChangedSubscriptionRequest, typing.Callable[[JobExecutionsChangedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Subscribe to receive events whenever a job execution is added to or
        removed from the list of pending job executions for a thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-jobexecutionschanged

        Parameters:
        request - `JobExecutionsChangedSubscriptionRequest` instance.
        on_event - Callback to invoke each time the on_event event is received.
                The callback should take 1 argument of type `JobExecutionsChangedEvent`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        return self._jobs_client.subscribe_to_job_executions_changed_events(
            request, on_event
        )

    def subscribe_to_next_job_execution_changed_events(self, request, on_event):
        # type: (NextJobExecutionChangedSubscriptionRequest, typing.Callable[[NextJobExecutionChangedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Subscribe to receive events whenever there is a change to which job
        execution is next on the list of pending job executions for a thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-nextjobexecutionchanged

        Parameters:
        request - `NextJobExecutionChangedSubscriptionRequest` instance.
        on_event - Callback to invoke each time the on_event event is received.
                The callback should take 1 argument of type `NextJobExecutionChangedEvent`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        return self._jobs_client.subscribe_to_next_job_execution_changed_events(
            request, on_event
        )

    def _transform_result(self, result):
        if isinstance(result, iotjobs.RejectedError):
            return JobsErrorResponse(result)
        else:
            return result


class ShadowErrorResponse(Exception):
    """Exception for when the server responds with a rejection of the request."""
    def __init__(self, response):
        self.response = response  # type: iotshadow.ErrorResponse


class IotShadowRpcClient(_MqttRpcServiceClient):
    """
    This alternative to the `IoTShadowClient` handles the complexity of
    performing RPCs (remote procedure calls) over the MQTT's
    publish/subscribe architecture.
    """

    def __init__(self, mqtt_connection):
        # type: (mqtt.Connection) -> None
        super(IotShadowRpcClient, self).__init__(
            iotshadow.IotShadowClient(mqtt_connection)
        )
        self._shadow_client = self._mqtt_service_client  # type: iotshadow.IotShadowClient

    def delete_shadow(self, request):
        # type(iotshadow.DeleteShadowRequest) -> Future
        """
        Delete the shadow.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-rejected-pub-sub-topic

        Parameters:
        request - `DeleteShadowRequest` instance.

        Returns a `Future` which will contain a result of `DeleteShadowResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._shadow_client.publish_delete_shadow,
            pub_request=request,
            sub_accepted_op=self._shadow_client.subscribe_to_delete_shadow_accepted,
            sub_rejected_op=self._shadow_client.subscribe_to_delete_shadow_rejected,
            sub_request=iotshadow.DeleteShadowSubscriptionRequest(
                thing_name=request.thing_name
            ),
        )

    def get_shadow(self, request):
        # type: (iotshadow.GetShadowRequest) -> Future
        """
        Get the shadow.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-pub-sub-topic

        Parameters:
        request - `GetShadowRequest` instance.

        Returns a `Future` which will contain a result of `GetShadowResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._shadow_client.publish_get_shadow,
            pub_request=request,
            sub_accepted_op=self._shadow_client.subscribe_to_get_shadow_accepted,
            sub_rejected_op=self._shadow_client.subscribe_to_get_shadow_rejected,
            sub_request=iotshadow.GetShadowSubscriptionRequest(
                thing_name=request.thing_name
            ),
        )

    def update_shadow(self, request):
        # type(iotshadow.UpdateShadowRequest) -> Future
        """
        Update the shadow.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-pub-sub-topic

        Parameters:
        request - `UpdateShadowRequest` instance.

        Returns a `Future` which will contain a result of `UpdateShadowResponse`
        if the operation succeeds, or an exception if the operation fails.
        """
        return self._start_rpc(
            pub_op=self._shadow_client.publish_update_shadow,
            pub_request=request,
            sub_accepted_op=self._shadow_client.subscribe_to_update_shadow_accepted,
            sub_rejected_op=self._shadow_client.subscribe_to_update_shadow_rejected,
            sub_request=iotshadow.UpdateShadowSubscriptionRequest(
                thing_name=request.thing_name
            ),
        )

    def subscribe_to_shadow_delta_updated_events(self, request, on_event):
        # type: (iotshadow.ShadowDeltaUpdatedSubscriptionRequest, typing.Callable[[ShadowDeltaUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Subscribe to receive events whenever the shadow is updated and
        contains different values for desired and reported states.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-delta-pub-sub-topic

        Parameters:
        request - `ShadowDeltaUpdatedSubscriptionRequest` instance.
        on_event - Callback to invoke each time the on_event event is received.
                The callback should take 1 argument of type `ShadowDeltaUpdatedEvent`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        return self._shadow_client.subscribe_to_shadow_delta_updated_events(
            request, on_event
        )

    def subscribe_to_shadow_updated_events(self, request, on_event):
        # type: (ShadowUpdatedSubscriptionRequest, typing.Callable[[ShadowUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Subscribe to receive events whenever the shadow is updated.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-documents-pub-sub-topic

        Parameters:
        request - `ShadowUpdatedSubscriptionRequest` instance.
        on_event - Callback to invoke each time the on_event event is received.
                The callback should take 1 argument of type `ShadowUpdatedEvent`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        return self._shadow_client.subscribe_to_shadow_updated_events(request, on_event)

    def _transform_result(self, result):
        if isinstance(result, iotshadow.ErrorResponse):
            return ShadowErrorResponse(result)
        else:
            return result
