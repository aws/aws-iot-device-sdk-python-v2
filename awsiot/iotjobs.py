# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

# This file is generated

import awscrt.mqtt
import awsiot
import concurrent.futures
import datetime
import typing

class IotJobsClient(awsiot.MqttServiceClient):

    def publish_describe_job_execution(self, request, qos):
        # type: (DescribeJobExecutionRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.job_id:
            raise ValueError("request.job_id is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get'.format(request),
            qos=qos,
            payload=request.to_payload())

    def publish_get_pending_job_executions(self, request, qos):
        # type: (GetPendingJobExecutionsRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/get'.format(request),
            qos=qos,
            payload=request.to_payload())

    def publish_start_next_pending_job_execution(self, request, qos):
        # type: (StartNextPendingJobExecutionRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/start-next'.format(request),
            qos=qos,
            payload=request.to_payload())

    def publish_update_job_execution(self, request, qos):
        # type: (UpdateJobExecutionRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update'.format(request),
            qos=qos,
            payload=request.to_payload())

    def subscribe_to_describe_job_execution_accepted(self, request, qos, callback):
        # type: (DescribeJobExecutionSubscriptionRequest, int, typing.Callable[[DescribeJobExecutionResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `DescribeJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=DescribeJobExecutionResponse.from_payload)

    def subscribe_to_describe_job_execution_rejected(self, request, qos, callback):
        # type: (DescribeJobExecutionSubscriptionRequest, int, typing.Callable[[RejectedError], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=RejectedError.from_payload)

    def subscribe_to_get_pending_job_executions_accepted(self, request, qos, callback):
        # type: (GetPendingJobExecutionsSubscriptionRequest, int, typing.Callable[[GetPendingJobExecutionsResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `GetPendingJobExecutionsResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/get/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=GetPendingJobExecutionsResponse.from_payload)

    def subscribe_to_get_pending_job_executions_rejected(self, request, qos, callback):
        # type: (GetPendingJobExecutionsSubscriptionRequest, int, typing.Callable[[RejectedError], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/get/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=RejectedError.from_payload)

    def subscribe_to_job_executions_changed_events(self, request, qos, callback):
        # type: (JobExecutionsChangedSubscriptionRequest, int, typing.Callable[[JobExecutionsChangedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-jobexecutionschanged

        Parameters:
        request - `JobExecutionsChangedSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `JobExecutionsChangedEvent`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/notify'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=JobExecutionsChangedEvent.from_payload)

    def subscribe_to_next_job_execution_changed_events(self, request, qos, callback):
        # type: (NextJobExecutionChangedSubscriptionRequest, int, typing.Callable[[NextJobExecutionChangedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-nextjobexecutionchanged

        Parameters:
        request - `NextJobExecutionChangedSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `NextJobExecutionChangedEvent`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/notify-next'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=NextJobExecutionChangedEvent.from_payload)

    def subscribe_to_start_next_pending_job_execution_accepted(self, request, qos, callback):
        # type: (StartNextPendingJobExecutionSubscriptionRequest, int, typing.Callable[[StartNextJobExecutionResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `StartNextJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/start-next/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=StartNextJobExecutionResponse.from_payload)

    def subscribe_to_start_next_pending_job_execution_rejected(self, request, qos, callback):
        # type: (StartNextPendingJobExecutionSubscriptionRequest, int, typing.Callable[[RejectedError], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/start-next/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=RejectedError.from_payload)

    def subscribe_to_update_job_execution_accepted(self, request, qos, callback):
        # type: (UpdateJobExecutionSubscriptionRequest, int, typing.Callable[[UpdateJobExecutionResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `UpdateJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=UpdateJobExecutionResponse.from_payload)

    def subscribe_to_update_job_execution_rejected(self, request, qos, callback):
        # type: (UpdateJobExecutionSubscriptionRequest, int, typing.Callable[[RejectedError], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=RejectedError.from_payload)

class DescribeJobExecutionRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'execution_number', 'include_job_document', 'job_id', 'thing_name']

    def __init__(self, client_token=None, execution_number=None, include_job_document=None, job_id=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[int], typing.Optional[bool], typing.Optional[str], typing.Optional[str]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution_number = execution_number # type: typing.Optional[int]
        self.include_job_document = include_job_document # type: typing.Optional[bool]
        self.job_id = job_id # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        if self.execution_number is not None:
            payload['executionNumber'] = self.execution_number
        if self.include_job_document is not None:
            payload['includeJobDocument'] = self.include_job_document
        return payload

class DescribeJobExecutionResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'execution', 'timestamp']

    def __init__(self, client_token=None, execution=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[JobExecutionData], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution = execution # type: typing.Optional[JobExecutionData]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> DescribeJobExecutionResponse
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
        val = payload.get('execution')
        if val is not None:
            new.execution = JobExecutionData.from_payload(val)
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class DescribeJobExecutionSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['job_id', 'thing_name']

    def __init__(self, job_id=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[str]) -> None
        self.job_id = job_id # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

class GetPendingJobExecutionsRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'thing_name']

    def __init__(self, client_token=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[str]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        return payload

class GetPendingJobExecutionsResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'in_progress_jobs', 'queued_jobs', 'timestamp']

    def __init__(self, client_token=None, in_progress_jobs=None, queued_jobs=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[typing.List[JobExecutionSummary]], typing.Optional[typing.List[JobExecutionSummary]], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.in_progress_jobs = in_progress_jobs # type: typing.Optional[typing.List[JobExecutionSummary]]
        self.queued_jobs = queued_jobs # type: typing.Optional[typing.List[JobExecutionSummary]]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> GetPendingJobExecutionsResponse
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
        val = payload.get('inProgressJobs')
        if val is not None:
            new.in_progress_jobs = [JobExecutionSummary.from_payload(i) for i in val]
        val = payload.get('queuedJobs')
        if val is not None:
            new.queued_jobs = [JobExecutionSummary.from_payload(i) for i in val]
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class GetPendingJobExecutionsSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class JobExecutionData(awsiot.ModeledClass):
    __slots__ = ['execution_number', 'job_document', 'job_id', 'last_updated_at', 'queued_at', 'started_at', 'status', 'status_details', 'thing_name', 'version_number']

    def __init__(self, execution_number=None, job_document=None, job_id=None, last_updated_at=None, queued_at=None, started_at=None, status=None, status_details=None, thing_name=None, version_number=None):
        # type: (typing.Optional[int], typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[str], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[str], typing.Optional[typing.Dict[str, str]], typing.Optional[str], typing.Optional[int]) -> None
        self.execution_number = execution_number # type: typing.Optional[int]
        self.job_document = job_document # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.job_id = job_id # type: typing.Optional[str]
        self.last_updated_at = last_updated_at # type: typing.Optional[datetime.datetime]
        self.queued_at = queued_at # type: typing.Optional[datetime.datetime]
        self.started_at = started_at # type: typing.Optional[datetime.datetime]
        self.status = status # type: typing.Optional[str]
        self.status_details = status_details # type: typing.Optional[typing.Dict[str, str]]
        self.thing_name = thing_name # type: typing.Optional[str]
        self.version_number = version_number # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionData
        new = cls()
        val = payload.get('executionNumber')
        if val is not None:
            new.execution_number = val
        val = payload.get('jobDocument')
        if val is not None:
            new.job_document = val
        val = payload.get('jobId')
        if val is not None:
            new.job_id = val
        val = payload.get('lastUpdatedAt')
        if val is not None:
            new.last_updated_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('queuedAt')
        if val is not None:
            new.queued_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('startedAt')
        if val is not None:
            new.started_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('status')
        if val is not None:
            new.status = val
        val = payload.get('statusDetails')
        if val is not None:
            new.status_details = val
        val = payload.get('thingName')
        if val is not None:
            new.thing_name = val
        val = payload.get('versionNumber')
        if val is not None:
            new.version_number = val
        return new

class JobExecutionState(awsiot.ModeledClass):
    __slots__ = ['status', 'status_details', 'version_number']

    def __init__(self, status=None, status_details=None, version_number=None):
        # type: (typing.Optional[str], typing.Optional[typing.Dict[str, str]], typing.Optional[int]) -> None
        self.status = status # type: typing.Optional[str]
        self.status_details = status_details # type: typing.Optional[typing.Dict[str, str]]
        self.version_number = version_number # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionState
        new = cls()
        val = payload.get('status')
        if val is not None:
            new.status = val
        val = payload.get('statusDetails')
        if val is not None:
            new.status_details = val
        val = payload.get('versionNumber')
        if val is not None:
            new.version_number = val
        return new

class JobExecutionSummary(awsiot.ModeledClass):
    __slots__ = ['execution_number', 'job_id', 'last_updated_at', 'queued_at', 'started_at', 'version_number']

    def __init__(self, execution_number=None, job_id=None, last_updated_at=None, queued_at=None, started_at=None, version_number=None):
        # type: (typing.Optional[int], typing.Optional[str], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.execution_number = execution_number # type: typing.Optional[int]
        self.job_id = job_id # type: typing.Optional[str]
        self.last_updated_at = last_updated_at # type: typing.Optional[datetime.datetime]
        self.queued_at = queued_at # type: typing.Optional[datetime.datetime]
        self.started_at = started_at # type: typing.Optional[datetime.datetime]
        self.version_number = version_number # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionSummary
        new = cls()
        val = payload.get('executionNumber')
        if val is not None:
            new.execution_number = val
        val = payload.get('jobId')
        if val is not None:
            new.job_id = val
        val = payload.get('lastUpdatedAt')
        if val is not None:
            new.last_updated_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('queuedAt')
        if val is not None:
            new.queued_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('startedAt')
        if val is not None:
            new.started_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('versionNumber')
        if val is not None:
            new.version_number = val
        return new

class JobExecutionsChangedEvent(awsiot.ModeledClass):
    __slots__ = ['jobs', 'timestamp']

    def __init__(self, jobs=None, timestamp=None):
        # type: (typing.Optional[typing.Dict[str, typing.List[JobExecutionSummary]]], typing.Optional[datetime.datetime]) -> None
        self.jobs = jobs # type: typing.Optional[typing.Dict[str, typing.List[JobExecutionSummary]]]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionsChangedEvent
        new = cls()
        val = payload.get('jobs')
        if val is not None:
            new.jobs = {k: [JobExecutionSummary.from_payload(i) for i in v] for k,v in val.items()}
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class JobExecutionsChangedSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class JobStatus:
    CANCELED = 'CANCELED'
    FAILED = 'FAILED'
    QUEUED = 'QUEUED'
    IN_PROGRESS = 'IN_PROGRESS'
    SUCCEEDED = 'SUCCEEDED'
    TIMED_OUT = 'TIMED_OUT'
    REJECTED = 'REJECTED'
    REMOVED = 'REMOVED'

class NextJobExecutionChangedEvent(awsiot.ModeledClass):
    __slots__ = ['execution', 'timestamp']

    def __init__(self, execution=None, timestamp=None):
        # type: (typing.Optional[JobExecutionData], typing.Optional[datetime.datetime]) -> None
        self.execution = execution # type: typing.Optional[JobExecutionData]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> NextJobExecutionChangedEvent
        new = cls()
        val = payload.get('execution')
        if val is not None:
            new.execution = JobExecutionData.from_payload(val)
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class NextJobExecutionChangedSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class RejectedError(awsiot.ModeledClass):
    __slots__ = ['client_token', 'code', 'execution_state', 'message', 'timestamp']

    def __init__(self, client_token=None, code=None, execution_state=None, message=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[str], typing.Optional[JobExecutionState], typing.Optional[str], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.code = code # type: typing.Optional[str]
        self.execution_state = execution_state # type: typing.Optional[JobExecutionState]
        self.message = message # type: typing.Optional[str]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> RejectedError
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
        val = payload.get('code')
        if val is not None:
            new.code = val
        val = payload.get('executionState')
        if val is not None:
            new.execution_state = JobExecutionState.from_payload(val)
        val = payload.get('message')
        if val is not None:
            new.message = val
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class RejectedErrorCode:
    INTERNAL_ERROR = 'InternalError'
    INVALID_JSON = 'InvalidJson'
    INVALID_REQUEST = 'InvalidRequest'
    INVALID_STATE_TRANSITION = 'InvalidStateTransition'
    RESOURCE_NOT_FOUND = 'ResourceNotFound'
    VERSION_MISMATCH = 'VersionMismatch'
    INVALID_TOPIC = 'InvalidTopic'
    REQUEST_THROTTLED = 'RequestThrottled'
    TERMINAL_STATE_REACHED = 'TerminalStateReached'

class StartNextJobExecutionResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'execution', 'timestamp']

    def __init__(self, client_token=None, execution=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[JobExecutionData], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution = execution # type: typing.Optional[JobExecutionData]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> StartNextJobExecutionResponse
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
        val = payload.get('execution')
        if val is not None:
            new.execution = JobExecutionData.from_payload(val)
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class StartNextPendingJobExecutionRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'status_details', 'step_timeout_in_minutes', 'thing_name']

    def __init__(self, client_token=None, status_details=None, step_timeout_in_minutes=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[typing.Dict[str, str]], typing.Optional[int], typing.Optional[str]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.status_details = status_details # type: typing.Optional[typing.Dict[str, str]]
        self.step_timeout_in_minutes = step_timeout_in_minutes # type: typing.Optional[int]
        self.thing_name = thing_name # type: typing.Optional[str]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        if self.status_details is not None:
            payload['statusDetails'] = self.status_details
        if self.step_timeout_in_minutes is not None:
            payload['stepTimeoutInMinutes'] = self.step_timeout_in_minutes
        return payload

class StartNextPendingJobExecutionSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class UpdateJobExecutionRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'execution_number', 'expected_version', 'include_job_document', 'include_job_execution_state', 'job_id', 'status', 'status_details', 'thing_name']

    def __init__(self, client_token=None, execution_number=None, expected_version=None, include_job_document=None, include_job_execution_state=None, job_id=None, status=None, status_details=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[int], typing.Optional[int], typing.Optional[bool], typing.Optional[bool], typing.Optional[str], typing.Optional[str], typing.Optional[typing.Dict[str, str]], typing.Optional[str]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution_number = execution_number # type: typing.Optional[int]
        self.expected_version = expected_version # type: typing.Optional[int]
        self.include_job_document = include_job_document # type: typing.Optional[bool]
        self.include_job_execution_state = include_job_execution_state # type: typing.Optional[bool]
        self.job_id = job_id # type: typing.Optional[str]
        self.status = status # type: typing.Optional[str]
        self.status_details = status_details # type: typing.Optional[typing.Dict[str, str]]
        self.thing_name = thing_name # type: typing.Optional[str]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        if self.execution_number is not None:
            payload['executionNumber'] = self.execution_number
        if self.expected_version is not None:
            payload['expectedVersion'] = self.expected_version
        if self.include_job_document is not None:
            payload['includeJobDocument'] = self.include_job_document
        if self.include_job_execution_state is not None:
            payload['includeJobExecutionState'] = self.include_job_execution_state
        if self.status is not None:
            payload['status'] = self.status
        if self.status_details is not None:
            payload['statusDetails'] = self.status_details
        return payload

class UpdateJobExecutionResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'execution_state', 'job_document', 'timestamp']

    def __init__(self, client_token=None, execution_state=None, job_document=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[JobExecutionState], typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution_state = execution_state # type: typing.Optional[JobExecutionState]
        self.job_document = job_document # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> UpdateJobExecutionResponse
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
        val = payload.get('executionState')
        if val is not None:
            new.execution_state = JobExecutionState.from_payload(val)
        val = payload.get('jobDocument')
        if val is not None:
            new.job_document = val
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class UpdateJobExecutionSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['job_id', 'thing_name']

    def __init__(self, job_id=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[str]) -> None
        self.job_id = job_id # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

