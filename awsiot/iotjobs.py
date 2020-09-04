# Copyright Amazon.com, Inc. or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot
import concurrent.futures
import datetime
import typing

class IotJobsClient(awsiot.MqttServiceClient):

    def publish_describe_job_execution(self, request, qos):
        # type: (DescribeJobExecutionRequest, int) -> concurrent.futures.Future
        """
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
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Args:
            request: `DescribeJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `DescribeJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `DescribeJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `GetPendingJobExecutionsSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `GetPendingJobExecutionsResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `GetPendingJobExecutionsSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `JobExecutionsChangedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `JobExecutionsChangedEvent`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `NextJobExecutionChangedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `NextJobExecutionChangedEvent`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `StartNextPendingJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `StartNextJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `StartNextPendingJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
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

        Args:
            request: `UpdateJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `UpdateJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
            which will contain a result of `None` when the server has acknowledged
            the subscription, or an exception if the subscription fails. The second
            value is a topic which may be passed to `unsubscribe()` to stop
            receiving messages. Note that messages may arrive before the
            subscription is acknowledged.
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
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Args:
            request: `UpdateJobExecutionSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a Future
            which will contain a result of `None` when the server has acknowledged
            the subscription, or an exception if the subscription fails. The second
            value is a topic which may be passed to `unsubscribe()` to stop
            receiving messages. Note that messages may arrive before the
            subscription is acknowledged.
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        execution_number (int)
        include_job_document (bool)
        job_id (str)
        thing_name (str)

    Attributes:
        client_token (str)
        execution_number (int)
        include_job_document (bool)
        job_id (str)
        thing_name (str)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        execution (JobExecutionData)
        timestamp (datetime.datetime)

    Attributes:
        client_token (str)
        execution (JobExecutionData)
        timestamp (datetime.datetime)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        job_id (str)
        thing_name (str)

    Attributes:
        job_id (str)
        thing_name (str)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        thing_name (str)

    Attributes:
        client_token (str)
        thing_name (str)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        in_progress_jobs (typing.List[JobExecutionSummary])
        queued_jobs (typing.List[JobExecutionSummary])
        timestamp (datetime.datetime)

    Attributes:
        client_token (str)
        in_progress_jobs (typing.List[JobExecutionSummary])
        queued_jobs (typing.List[JobExecutionSummary])
        timestamp (datetime.datetime)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str)

    Attributes:
        thing_name (str)
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class JobExecutionData(awsiot.ModeledClass):
    """
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        execution_number (int)
        job_document (typing.Dict[str, typing.Any])
        job_id (str)
        last_updated_at (datetime.datetime)
        queued_at (datetime.datetime)
        started_at (datetime.datetime)
        status (str)
        status_details (typing.Dict[str, str])
        thing_name (str)
        version_number (int)

    Attributes:
        execution_number (int)
        job_document (typing.Dict[str, typing.Any])
        job_id (str)
        last_updated_at (datetime.datetime)
        queued_at (datetime.datetime)
        started_at (datetime.datetime)
        status (str)
        status_details (typing.Dict[str, str])
        thing_name (str)
        version_number (int)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        status (str)
        status_details (typing.Dict[str, str])
        version_number (int)

    Attributes:
        status (str)
        status_details (typing.Dict[str, str])
        version_number (int)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        execution_number (int)
        job_id (str)
        last_updated_at (datetime.datetime)
        queued_at (datetime.datetime)
        started_at (datetime.datetime)
        version_number (int)

    Attributes:
        execution_number (int)
        job_id (str)
        last_updated_at (datetime.datetime)
        queued_at (datetime.datetime)
        started_at (datetime.datetime)
        version_number (int)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        jobs (typing.Dict[str, typing.List[JobExecutionSummary]])
        timestamp (datetime.datetime)

    Attributes:
        jobs (typing.Dict[str, typing.List[JobExecutionSummary]])
        timestamp (datetime.datetime)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str)

    Attributes:
        thing_name (str)
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

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
    """
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        execution (JobExecutionData)
        timestamp (datetime.datetime)

    Attributes:
        execution (JobExecutionData)
        timestamp (datetime.datetime)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str)

    Attributes:
        thing_name (str)
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class RejectedError(awsiot.ModeledClass):
    """
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        code (str)
        execution_state (JobExecutionState)
        message (str)
        timestamp (datetime.datetime)

    Attributes:
        client_token (str)
        code (str)
        execution_state (JobExecutionState)
        message (str)
        timestamp (datetime.datetime)
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
    """
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        execution (JobExecutionData)
        timestamp (datetime.datetime)

    Attributes:
        client_token (str)
        execution (JobExecutionData)
        timestamp (datetime.datetime)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        status_details (typing.Dict[str, str])
        step_timeout_in_minutes (int)
        thing_name (str)

    Attributes:
        client_token (str)
        status_details (typing.Dict[str, str])
        step_timeout_in_minutes (int)
        thing_name (str)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str)

    Attributes:
        thing_name (str)
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class UpdateJobExecutionRequest(awsiot.ModeledClass):
    """
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        execution_number (int)
        expected_version (int)
        include_job_document (bool)
        include_job_execution_state (bool)
        job_id (str)
        status (str)
        status_details (typing.Dict[str, str])
        step_timeout_in_minutes (int)
        thing_name (str)

    Attributes:
        client_token (str)
        execution_number (int)
        expected_version (int)
        include_job_document (bool)
        include_job_execution_state (bool)
        job_id (str)
        status (str)
        status_details (typing.Dict[str, str])
        step_timeout_in_minutes (int)
        thing_name (str)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str)
        execution_state (JobExecutionState)
        job_document (typing.Dict[str, typing.Any])
        timestamp (datetime.datetime)

    Attributes:
        client_token (str)
        execution_state (JobExecutionState)
        job_document (typing.Dict[str, typing.Any])
        timestamp (datetime.datetime)
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
    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        job_id (str)
        thing_name (str)

    Attributes:
        job_id (str)
        thing_name (str)
    """

    __slots__ = ['job_id', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.job_id = kwargs.get('job_id')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['job_id', 'thing_name'], args):
            setattr(self, key, val)

