# Copyright Amazon.com, Inc. or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot
import concurrent.futures
import datetime
import typing

class IotJobsClient(awsiot.MqttServiceClient):
    """

    The AWS IoT jobs service can be used to define a set of remote operations that are sent to and executed on one or more devices connected to AWS IoT.

    AWS Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#jobs-mqtt-api

    """

    def publish_describe_job_execution(self, request, qos):
        # type: (DescribeJobExecutionRequest, int) -> concurrent.futures.Future
        """

        Gets detailed information about a job execution.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Args:
            request: `DescribeJobExecutionRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
            request is successfully published. The Future's result will be an
            exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get'.format(request),
            qos=qos,
            payload=request.to_payload())

    def publish_get_pending_job_executions(self, request, qos):
        # type: (GetPendingJobExecutionsRequest, int) -> concurrent.futures.Future
        """

        Gets the list of all jobs for a thing that are not in a terminal state.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Args:
            request: `GetPendingJobExecutionsRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Gets and starts the next pending job execution for a thing (status IN_PROGRESS or QUEUED).

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Args:
            request: `StartNextPendingJobExecutionRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Updates the status of a job execution. You can optionally create a step timer by setting a value for the stepTimeoutInMinutes property. If you don't update the value of this property by running UpdateJobExecution again, the job execution times out when the step timer expires.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Args:
            request: `UpdateJobExecutionRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Subscribes to the accepted topic for the DescribeJobExecution operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Args:
            request: `DescribeJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `DescribeJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to the rejected topic for the DescribeJobExecution operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Args:
            request: `DescribeJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to the accepted topic for the GetPendingJobsExecutions operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Args:
            request: `GetPendingJobExecutionsSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `GetPendingJobExecutionsResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to the rejected topic for the GetPendingJobsExecutions operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Args:
            request: `GetPendingJobExecutionsSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to JobExecutionsChanged notifications for a given IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-jobexecutionschanged

        Args:
            request: `JobExecutionsChangedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `JobExecutionsChangedEvent`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Args:
            request: `NextJobExecutionChangedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `NextJobExecutionChangedEvent`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to the accepted topic for the StartNextPendingJobExecution operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Args:
            request: `StartNextPendingJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `StartNextJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to the rejected topic for the StartNextPendingJobExecution operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Args:
            request: `StartNextPendingJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribes to the accepted topic for the UpdateJobExecution operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Args:
            request: `UpdateJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `UpdateJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
        """
        if not request.job_id:
            raise ValueError("request.job_id is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

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

        Subscribes to the rejected topic for the UpdateJobExecution operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Args:
            request: `UpdateJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
        """
        if not request.job_id:
            raise ValueError("request.job_id is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=RejectedError.from_payload)

class DescribeJobExecutionRequest(awsiot.ModeledClass):
    """

    Data needed to make a DescribeJobExecution request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): An opaque string used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        execution_number (int): Optional. A number that identifies a job execution on a device. If not specified, the latest job execution is returned.
        include_job_document (bool): Optional. Unless set to false, the response contains the job document. The default is true.
        job_id (str): The unique identifier assigned to this job when it was created. Or use $next to return the next pending job execution for a thing (status IN_PROGRESS or QUEUED). In this case, any job executions with status IN_PROGRESS are returned first. Job executions are returned in the order in which they were created.
        thing_name (str): The name of the thing associated with the device.

    Attributes:
        client_token (str): An opaque string used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        execution_number (int): Optional. A number that identifies a job execution on a device. If not specified, the latest job execution is returned.
        include_job_document (bool): Optional. Unless set to false, the response contains the job document. The default is true.
        job_id (str): The unique identifier assigned to this job when it was created. Or use $next to return the next pending job execution for a thing (status IN_PROGRESS or QUEUED). In this case, any job executions with status IN_PROGRESS are returned first. Job executions are returned in the order in which they were created.
        thing_name (str): The name of the thing associated with the device.
    """

    __slots__ = ['client_token', 'execution_number', 'include_job_document', 'job_id', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.execution_number = kwargs.get('execution_number')
        self.include_job_document = kwargs.get('include_job_document')
        self.job_id = kwargs.get('job_id')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'execution_number', 'include_job_document', 'job_id', 'thing_name'], args):
            setattr(self, key, val)

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
    """

    Response payload to a DescribeJobExecution request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): A client token used to correlate requests and responses.
        execution (JobExecutionData): Contains data about a job execution.
        timestamp (datetime.datetime): The time when the message was sent.

    Attributes:
        client_token (str): A client token used to correlate requests and responses.
        execution (JobExecutionData): Contains data about a job execution.
        timestamp (datetime.datetime): The time when the message was sent.
    """

    __slots__ = ['client_token', 'execution', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.execution = kwargs.get('execution')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'execution', 'timestamp'], args):
            setattr(self, key, val)

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
    """

    Data needed to subscribe to DescribeJobExecution responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        job_id (str): Job ID that you want to subscribe to DescribeJobExecution response events for.
        thing_name (str): Name of the IoT Thing that you want to subscribe to DescribeJobExecution response events for.

    Attributes:
        job_id (str): Job ID that you want to subscribe to DescribeJobExecution response events for.
        thing_name (str): Name of the IoT Thing that you want to subscribe to DescribeJobExecution response events for.
    """

    __slots__ = ['job_id', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.job_id = kwargs.get('job_id')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['job_id', 'thing_name'], args):
            setattr(self, key, val)

class GetPendingJobExecutionsRequest(awsiot.ModeledClass):
    """

    Data needed to make a GetPendingJobExecutions request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        thing_name (str): IoT Thing the request is relative to.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        thing_name (str): IoT Thing the request is relative to.
    """

    __slots__ = ['client_token', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        return payload

class GetPendingJobExecutionsResponse(awsiot.ModeledClass):
    """

    Response payload to a GetPendingJobExecutions request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): A client token used to correlate requests and responses.
        in_progress_jobs (typing.List[JobExecutionSummary]): A list of JobExecutionSummary objects with status IN_PROGRESS.
        queued_jobs (typing.List[JobExecutionSummary]): A list of JobExecutionSummary objects with status QUEUED.
        timestamp (datetime.datetime): The time when the message was sent.

    Attributes:
        client_token (str): A client token used to correlate requests and responses.
        in_progress_jobs (typing.List[JobExecutionSummary]): A list of JobExecutionSummary objects with status IN_PROGRESS.
        queued_jobs (typing.List[JobExecutionSummary]): A list of JobExecutionSummary objects with status QUEUED.
        timestamp (datetime.datetime): The time when the message was sent.
    """

    __slots__ = ['client_token', 'in_progress_jobs', 'queued_jobs', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.in_progress_jobs = kwargs.get('in_progress_jobs')
        self.queued_jobs = kwargs.get('queued_jobs')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'in_progress_jobs', 'queued_jobs', 'timestamp'], args):
            setattr(self, key, val)

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
    """

    Data needed to subscribe to GetPendingJobExecutions responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the IoT Thing that you want to subscribe to GetPendingJobExecutions response events for.

    Attributes:
        thing_name (str): Name of the IoT Thing that you want to subscribe to GetPendingJobExecutions response events for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class JobExecutionData(awsiot.ModeledClass):
    """

    Data about a job execution.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        execution_number (int): A number that identifies a job execution on a device. It can be used later in commands that return or update job execution information.
        job_document (typing.Dict[str, typing.Any]): The content of the job document.
        job_id (str): The unique identifier you assigned to this job when it was created.
        last_updated_at (datetime.datetime): The time when the job execution started.
        queued_at (datetime.datetime): The time when the job execution was enqueued.
        started_at (datetime.datetime): The time when the job execution started.
        status (str): The status of the job execution. Can be one of: QUEUED, IN_PROGRESS, FAILED, SUCCEEDED, CANCELED, TIMED_OUT, REJECTED, or REMOVED.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution.
        thing_name (str): The name of the thing that is executing the job.
        version_number (int): The version of the job execution. Job execution versions are incremented each time they are updated by a device.

    Attributes:
        execution_number (int): A number that identifies a job execution on a device. It can be used later in commands that return or update job execution information.
        job_document (typing.Dict[str, typing.Any]): The content of the job document.
        job_id (str): The unique identifier you assigned to this job when it was created.
        last_updated_at (datetime.datetime): The time when the job execution started.
        queued_at (datetime.datetime): The time when the job execution was enqueued.
        started_at (datetime.datetime): The time when the job execution started.
        status (str): The status of the job execution. Can be one of: QUEUED, IN_PROGRESS, FAILED, SUCCEEDED, CANCELED, TIMED_OUT, REJECTED, or REMOVED.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution.
        thing_name (str): The name of the thing that is executing the job.
        version_number (int): The version of the job execution. Job execution versions are incremented each time they are updated by a device.
    """

    __slots__ = ['execution_number', 'job_document', 'job_id', 'last_updated_at', 'queued_at', 'started_at', 'status', 'status_details', 'thing_name', 'version_number']

    def __init__(self, *args, **kwargs):
        self.execution_number = kwargs.get('execution_number')
        self.job_document = kwargs.get('job_document')
        self.job_id = kwargs.get('job_id')
        self.last_updated_at = kwargs.get('last_updated_at')
        self.queued_at = kwargs.get('queued_at')
        self.started_at = kwargs.get('started_at')
        self.status = kwargs.get('status')
        self.status_details = kwargs.get('status_details')
        self.thing_name = kwargs.get('thing_name')
        self.version_number = kwargs.get('version_number')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['execution_number', 'job_document', 'job_id', 'last_updated_at', 'queued_at', 'started_at', 'status', 'status_details', 'thing_name', 'version_number'], args):
            setattr(self, key, val)

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
    """

    Data about the state of a job execution.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        status (str): The status of the job execution. Can be one of: QUEUED, IN_PROGRESS, FAILED, SUCCEEDED, CANCELED, TIMED_OUT, REJECTED, or REMOVED.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution.
        version_number (int): The version of the job execution. Job execution versions are incremented each time they are updated by a device.

    Attributes:
        status (str): The status of the job execution. Can be one of: QUEUED, IN_PROGRESS, FAILED, SUCCEEDED, CANCELED, TIMED_OUT, REJECTED, or REMOVED.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution.
        version_number (int): The version of the job execution. Job execution versions are incremented each time they are updated by a device.
    """

    __slots__ = ['status', 'status_details', 'version_number']

    def __init__(self, *args, **kwargs):
        self.status = kwargs.get('status')
        self.status_details = kwargs.get('status_details')
        self.version_number = kwargs.get('version_number')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['status', 'status_details', 'version_number'], args):
            setattr(self, key, val)

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
    """

    Contains a subset of information about a job execution.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        execution_number (int): A number that identifies a job execution on a device.
        job_id (str): The unique identifier you assigned to this job when it was created.
        last_updated_at (datetime.datetime): The time when the job execution was last updated.
        queued_at (datetime.datetime): The time when the job execution was enqueued.
        started_at (datetime.datetime): The time when the job execution started.
        version_number (int): The version of the job execution. Job execution versions are incremented each time the AWS IoT Jobs service receives an update from a device.

    Attributes:
        execution_number (int): A number that identifies a job execution on a device.
        job_id (str): The unique identifier you assigned to this job when it was created.
        last_updated_at (datetime.datetime): The time when the job execution was last updated.
        queued_at (datetime.datetime): The time when the job execution was enqueued.
        started_at (datetime.datetime): The time when the job execution started.
        version_number (int): The version of the job execution. Job execution versions are incremented each time the AWS IoT Jobs service receives an update from a device.
    """

    __slots__ = ['execution_number', 'job_id', 'last_updated_at', 'queued_at', 'started_at', 'version_number']

    def __init__(self, *args, **kwargs):
        self.execution_number = kwargs.get('execution_number')
        self.job_id = kwargs.get('job_id')
        self.last_updated_at = kwargs.get('last_updated_at')
        self.queued_at = kwargs.get('queued_at')
        self.started_at = kwargs.get('started_at')
        self.version_number = kwargs.get('version_number')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['execution_number', 'job_id', 'last_updated_at', 'queued_at', 'started_at', 'version_number'], args):
            setattr(self, key, val)

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
    """

    Sent whenever a job execution is added to or removed from the list of pending job executions for a thing.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        jobs (typing.Dict[str, typing.List[JobExecutionSummary]]): Map from JobStatus to a list of Jobs transitioning to that status.
        timestamp (datetime.datetime): The time when the message was sent.

    Attributes:
        jobs (typing.Dict[str, typing.List[JobExecutionSummary]]): Map from JobStatus to a list of Jobs transitioning to that status.
        timestamp (datetime.datetime): The time when the message was sent.
    """

    __slots__ = ['jobs', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.jobs = kwargs.get('jobs')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['jobs', 'timestamp'], args):
            setattr(self, key, val)

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
    """

    Data needed to subscribe to JobExecutionsChanged events.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the IoT Thing that you want to subscribe to JobExecutionsChanged events for.

    Attributes:
        thing_name (str): Name of the IoT Thing that you want to subscribe to JobExecutionsChanged events for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class NextJobExecutionChangedEvent(awsiot.ModeledClass):
    """

    Sent whenever there is a change to which job execution is next on the list of pending job executions for a thing, as defined for DescribeJobExecution with jobId $next. This message is not sent when the next job's execution details change, only when the next job that would be returned by DescribeJobExecution with jobId $next has changed.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        execution (JobExecutionData): Contains data about a job execution.
        timestamp (datetime.datetime): The time when the message was sent.

    Attributes:
        execution (JobExecutionData): Contains data about a job execution.
        timestamp (datetime.datetime): The time when the message was sent.
    """

    __slots__ = ['execution', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.execution = kwargs.get('execution')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['execution', 'timestamp'], args):
            setattr(self, key, val)

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
    """

    Data needed to subscribe to NextJobExecutionChanged events.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the IoT Thing that you want to subscribe to NextJobExecutionChanged events for.

    Attributes:
        thing_name (str): Name of the IoT Thing that you want to subscribe to NextJobExecutionChanged events for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class RejectedError(awsiot.ModeledClass):
    """

    Response document containing details about a failed request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Opaque token that can correlate this response to the original request.
        code (str): Indicates the type of error.
        execution_state (JobExecutionState): A JobExecutionState object. This field is included only when the code field has the value InvalidStateTransition or VersionMismatch.
        message (str): A text message that provides additional information.
        timestamp (datetime.datetime): The date and time the response was generated by AWS IoT.

    Attributes:
        client_token (str): Opaque token that can correlate this response to the original request.
        code (str): Indicates the type of error.
        execution_state (JobExecutionState): A JobExecutionState object. This field is included only when the code field has the value InvalidStateTransition or VersionMismatch.
        message (str): A text message that provides additional information.
        timestamp (datetime.datetime): The date and time the response was generated by AWS IoT.
    """

    __slots__ = ['client_token', 'code', 'execution_state', 'message', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.code = kwargs.get('code')
        self.execution_state = kwargs.get('execution_state')
        self.message = kwargs.get('message')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'code', 'execution_state', 'message', 'timestamp'], args):
            setattr(self, key, val)

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

class StartNextJobExecutionResponse(awsiot.ModeledClass):
    """

    Response payload to a StartNextJobExecution request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): A client token used to correlate requests and responses.
        execution (JobExecutionData): Contains data about a job execution.
        timestamp (datetime.datetime): The time when the message was sent to the device.

    Attributes:
        client_token (str): A client token used to correlate requests and responses.
        execution (JobExecutionData): Contains data about a job execution.
        timestamp (datetime.datetime): The time when the message was sent to the device.
    """

    __slots__ = ['client_token', 'execution', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.execution = kwargs.get('execution')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'execution', 'timestamp'], args):
            setattr(self, key, val)

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
    """

    Data needed to make a StartNextPendingJobExecution request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution. If not specified, the statusDetails are unchanged.
        step_timeout_in_minutes (int): Specifies the amount of time this device has to finish execution of this job.
        thing_name (str): IoT Thing the request is relative to.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution. If not specified, the statusDetails are unchanged.
        step_timeout_in_minutes (int): Specifies the amount of time this device has to finish execution of this job.
        thing_name (str): IoT Thing the request is relative to.
    """

    __slots__ = ['client_token', 'status_details', 'step_timeout_in_minutes', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.status_details = kwargs.get('status_details')
        self.step_timeout_in_minutes = kwargs.get('step_timeout_in_minutes')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'status_details', 'step_timeout_in_minutes', 'thing_name'], args):
            setattr(self, key, val)

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
    """

    Data needed to subscribe to StartNextPendingJobExecution responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the IoT Thing that you want to subscribe to StartNextPendingJobExecution response events for.

    Attributes:
        thing_name (str): Name of the IoT Thing that you want to subscribe to StartNextPendingJobExecution response events for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class UpdateJobExecutionRequest(awsiot.ModeledClass):
    """

    Data needed to make an UpdateJobExecution request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        execution_number (int): Optional. A number that identifies a job execution on a device. If not specified, the latest job execution is used.
        expected_version (int): The expected current version of the job execution. Each time you update the job execution, its version is incremented. If the version of the job execution stored in the AWS IoT Jobs service does not match, the update is rejected with a VersionMismatch error, and an ErrorResponse that contains the current job execution status data is returned.
        include_job_document (bool): Optional. When included and set to true, the response contains the JobDocument. The default is false.
        include_job_execution_state (bool): Optional. When included and set to true, the response contains the JobExecutionState field. The default is false.
        job_id (str): The unique identifier assigned to this job when it was created.
        status (str): The new status for the job execution (IN_PROGRESS, FAILED, SUCCEEDED, or REJECTED). This must be specified on every update.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution. If not specified, the statusDetails are unchanged.
        step_timeout_in_minutes (int): Specifies the amount of time this device has to finish execution of this job. If the job execution status is not set to a terminal state before this timer expires, or before the timer is reset (by again calling UpdateJobExecution, setting the status to IN_PROGRESS and specifying a new timeout value in this field) the job execution status is set to TIMED_OUT. Setting or resetting this timeout has no effect on the job execution timeout that might have been specified when the job was created (by using CreateJob with the timeoutConfig).
        thing_name (str): The name of the thing associated with the device.

    Attributes:
        client_token (str): A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        execution_number (int): Optional. A number that identifies a job execution on a device. If not specified, the latest job execution is used.
        expected_version (int): The expected current version of the job execution. Each time you update the job execution, its version is incremented. If the version of the job execution stored in the AWS IoT Jobs service does not match, the update is rejected with a VersionMismatch error, and an ErrorResponse that contains the current job execution status data is returned.
        include_job_document (bool): Optional. When included and set to true, the response contains the JobDocument. The default is false.
        include_job_execution_state (bool): Optional. When included and set to true, the response contains the JobExecutionState field. The default is false.
        job_id (str): The unique identifier assigned to this job when it was created.
        status (str): The new status for the job execution (IN_PROGRESS, FAILED, SUCCEEDED, or REJECTED). This must be specified on every update.
        status_details (typing.Dict[str, str]): A collection of name-value pairs that describe the status of the job execution. If not specified, the statusDetails are unchanged.
        step_timeout_in_minutes (int): Specifies the amount of time this device has to finish execution of this job. If the job execution status is not set to a terminal state before this timer expires, or before the timer is reset (by again calling UpdateJobExecution, setting the status to IN_PROGRESS and specifying a new timeout value in this field) the job execution status is set to TIMED_OUT. Setting or resetting this timeout has no effect on the job execution timeout that might have been specified when the job was created (by using CreateJob with the timeoutConfig).
        thing_name (str): The name of the thing associated with the device.
    """

    __slots__ = ['client_token', 'execution_number', 'expected_version', 'include_job_document', 'include_job_execution_state', 'job_id', 'status', 'status_details', 'step_timeout_in_minutes', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.execution_number = kwargs.get('execution_number')
        self.expected_version = kwargs.get('expected_version')
        self.include_job_document = kwargs.get('include_job_document')
        self.include_job_execution_state = kwargs.get('include_job_execution_state')
        self.job_id = kwargs.get('job_id')
        self.status = kwargs.get('status')
        self.status_details = kwargs.get('status_details')
        self.step_timeout_in_minutes = kwargs.get('step_timeout_in_minutes')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'execution_number', 'expected_version', 'include_job_document', 'include_job_execution_state', 'job_id', 'status', 'status_details', 'step_timeout_in_minutes', 'thing_name'], args):
            setattr(self, key, val)

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
        if self.step_timeout_in_minutes is not None:
            payload['stepTimeoutInMinutes'] = self.step_timeout_in_minutes
        return payload

class UpdateJobExecutionResponse(awsiot.ModeledClass):
    """

    Response payload to an UpdateJobExecution request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): A client token used to correlate requests and responses.
        execution_state (JobExecutionState): Contains data about the state of a job execution.
        job_document (typing.Dict[str, typing.Any]): A UTF-8 encoded JSON document that contains information that your devices need to perform the job.
        timestamp (datetime.datetime): The time when the message was sent.

    Attributes:
        client_token (str): A client token used to correlate requests and responses.
        execution_state (JobExecutionState): Contains data about the state of a job execution.
        job_document (typing.Dict[str, typing.Any]): A UTF-8 encoded JSON document that contains information that your devices need to perform the job.
        timestamp (datetime.datetime): The time when the message was sent.
    """

    __slots__ = ['client_token', 'execution_state', 'job_document', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.execution_state = kwargs.get('execution_state')
        self.job_document = kwargs.get('job_document')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'execution_state', 'job_document', 'timestamp'], args):
            setattr(self, key, val)

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
    """

    Data needed to subscribe to UpdateJobExecution responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        job_id (str): Job ID that you want to subscribe to UpdateJobExecution response events for.
        thing_name (str): Name of the IoT Thing that you want to subscribe to UpdateJobExecution response events for.

    Attributes:
        job_id (str): Job ID that you want to subscribe to UpdateJobExecution response events for.
        thing_name (str): Name of the IoT Thing that you want to subscribe to UpdateJobExecution response events for.
    """

    __slots__ = ['job_id', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.job_id = kwargs.get('job_id')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['job_id', 'thing_name'], args):
            setattr(self, key, val)

class JobStatus:
    """

    The status of the job execution.

    """

    CANCELED = 'CANCELED'
    """
    """

    FAILED = 'FAILED'
    """
    """

    QUEUED = 'QUEUED'
    """
    """

    IN_PROGRESS = 'IN_PROGRESS'
    """
    """

    SUCCEEDED = 'SUCCEEDED'
    """
    """

    TIMED_OUT = 'TIMED_OUT'
    """
    """

    REJECTED = 'REJECTED'
    """
    """

    REMOVED = 'REMOVED'
    """
    """

class RejectedErrorCode:
    """

    A value indicating the kind of error encountered while processing an AWS IoT Jobs request

    """

    INTERNAL_ERROR = 'InternalError'
    """
    There was an internal error during the processing of the request.
    """

    INVALID_JSON = 'InvalidJson'
    """
    The contents of the request could not be interpreted as valid UTF-8-encoded JSON.
    """

    INVALID_REQUEST = 'InvalidRequest'
    """
    The contents of the request were invalid. The message contains details about the error.
    """

    INVALID_STATE_TRANSITION = 'InvalidStateTransition'
    """
    An update attempted to change the job execution to a state that is invalid because of the job execution's current state. In this case, the body of the error message also contains the executionState field.
    """

    RESOURCE_NOT_FOUND = 'ResourceNotFound'
    """
    The JobExecution specified by the request topic does not exist.
    """

    VERSION_MISMATCH = 'VersionMismatch'
    """
    The expected version specified in the request does not match the version of the job execution in the AWS IoT Jobs service. In this case, the body of the error message also contains the executionState field.
    """

    INVALID_TOPIC = 'InvalidTopic'
    """
    The request was sent to a topic in the AWS IoT Jobs namespace that does not map to any API.
    """

    REQUEST_THROTTLED = 'RequestThrottled'
    """
    The request was throttled.
    """

    TERMINAL_STATE_REACHED = 'TerminalStateReached'
    """
    Occurs when a command to describe a job is performed on a job that is in a terminal state.
    """

