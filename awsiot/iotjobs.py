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

import aws_crt.mqtt
import awsiot
import concurrent.futures
import datetime
import typing

class IotJobsClient(awsiot.MqttServiceClient):

    def publish_describe(self, request):
        # type: (DescribeJobExecutionRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionRequest` instance.

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
            payload=request.to_payload())

    def publish_get_pending(self, request):
        # type: (GetPendingJobExecutionsRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsRequest` instance.

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/get'.format(request),
            payload=request.to_payload())

    def publish_start_next_pending(self, request):
        # type: (StartNextPendingJobExecutionRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionRequest` instance.

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/jobs/start-next'.format(request),
            payload=request.to_payload())

    def publish_update(self, request):
        # type: (UpdateJobExecutionRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionRequest` instance.

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
            payload=request.to_payload())

    def subscribe_to_describe_accepted(self, request, on_accepted):
        # type: (DescribeJobExecutionSubscriptionRequest, typing.Callable[[DescribeJobExecutionResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `DescribeJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not on_accepted:
            raise ValueError("on_accepted is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=DescribeJobExecutionResponse.from_payload)

    def subscribe_to_describe_rejected(self, request, on_rejected):
        # type: (DescribeJobExecutionSubscriptionRequest, typing.Callable[[RejectedError], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-describejobexecution

        Parameters:
        request - `DescribeJobExecutionSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not on_rejected:
            raise ValueError("on_rejected is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=RejectedError.from_payload)

    def subscribe_to_executions_changed_events(self, request, on_job_executions_changed):
        # type: (JobExecutionsChangedEventsSubscriptionRequest, typing.Callable[[JobExecutionsChangedEvent], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-jobexecutionschanged

        Parameters:
        request - `JobExecutionsChangedEventsSubscriptionRequest` instance.
        on_job_executions_changed - Callback to invoke each time the on_job_executions_changed event is received.
                The callback should take 1 argument of type `JobExecutionsChangedEvent`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_job_executions_changed:
            raise ValueError("on_job_executions_changed is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/notify'.format(request),
            callback=on_job_executions_changed,
            payload_to_class_fn=JobExecutionsChangedEvent.from_payload)

    def subscribe_to_get_pending_accepted(self, request, on_accepted):
        # type: (GetPendingJobExecutionsSubscriptionRequest, typing.Callable[[GetPendingJobExecutionsResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `GetPendingJobExecutionsResponse`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_accepted:
            raise ValueError("on_accepted is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/get/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=GetPendingJobExecutionsResponse.from_payload)

    def subscribe_to_get_pending_rejected(self, request, on_rejected):
        # type: (GetPendingJobExecutionsSubscriptionRequest, typing.Callable[[RejectedError], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-getpendingjobexecutions

        Parameters:
        request - `GetPendingJobExecutionsSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_rejected:
            raise ValueError("on_rejected is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/get/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=RejectedError.from_payload)

    def subscribe_to_next_changed_events(self, request, on_next_job_execution_changed):
        # type: (NextJobExecutionChangedEventsSubscriptionRequest, typing.Callable[[NextJobExecutionChangedEvent], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-nextjobexecutionchanged

        Parameters:
        request - `NextJobExecutionChangedEventsSubscriptionRequest` instance.
        on_next_job_execution_changed - Callback to invoke each time the on_next_job_execution_changed event is received.
                The callback should take 1 argument of type `NextJobExecutionChangedEvent`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_next_job_execution_changed:
            raise ValueError("on_next_job_execution_changed is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/notify-next'.format(request),
            callback=on_next_job_execution_changed,
            payload_to_class_fn=NextJobExecutionChangedEvent.from_payload)

    def subscribe_to_start_next_pending_accepted(self, request, on_accepted):
        # type: (StartNextPendingJobExecutionSubscriptionRequest, typing.Callable[[StartDescribeJobExecutionResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `StartDescribeJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_accepted:
            raise ValueError("on_accepted is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/start-next/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=StartDescribeJobExecutionResponse.from_payload)

    def subscribe_to_start_next_pending_rejected(self, request, on_rejected):
        # type: (StartNextPendingJobExecutionSubscriptionRequest, typing.Callable[[RejectedError], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-startnextpendingjobexecution

        Parameters:
        request - `StartNextPendingJobExecutionSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_rejected:
            raise ValueError("on_rejected is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/start-next/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=RejectedError.from_payload)

    def subscribe_to_update_accepted(self, request, on_accepted):
        # type: (UpdateJobExecutionSubscriptionRequest, typing.Callable[[UpdateJobExecutionResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `UpdateJobExecutionResponse`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not on_accepted:
            raise ValueError("on_accepted is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=UpdateJobExecutionResponse.from_payload)

    def subscribe_to_update_rejected(self, request, on_rejected):
        # type: (UpdateJobExecutionSubscriptionRequest, typing.Callable[[RejectedError], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-api.html#mqtt-updatejobexecution

        Parameters:
        request - `UpdateJobExecutionSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `RejectedError`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")
        if not request.job_id:
            raise ValueError("request.job_id is required")

        if not on_rejected:
            raise ValueError("on_rejected is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=RejectedError.from_payload)

class DescribeJobExecutionRequest(object):
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
        if self.client_token:
            payload['clientToken'] = self.client_token
        if self.execution_number:
            payload['executionNumber'] = self.execution_number
        if self.include_job_document:
            payload['includeJobDocument'] = self.include_job_document
        return payload

class DescribeJobExecutionResponse(object):
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
        if val:
            new.client_token = val
        val = payload.get('execution')
        if val:
            new.execution = JobExecutionData.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class DescribeJobExecutionSubscriptionRequest(object):
    def __init__(self, job_id=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[str]) -> None
        self.job_id = job_id # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

class GetPendingJobExecutionsRequest(object):
    def __init__(self, client_token=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[str]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token:
            payload['clientToken'] = self.client_token
        return payload

class GetPendingJobExecutionsResponse(object):
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
        if val:
            new.client_token = val
        val = payload.get('inProgressJobs')
        if val:
            new.in_progress_jobs = [JobExecutionSummary.from_payload(i) for i in val]
        val = payload.get('queuedJobs')
        if val:
            new.queued_jobs = [JobExecutionSummary.from_payload(i) for i in val]
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class GetPendingJobExecutionsSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class JobExecutionData(object):
    def __init__(self, execution_number=None, job_document=None, job_id=None, last_updated_at=None, queued_at=None, started_at=None, status=None, thing_name=None, version_number=None):
        # type: (typing.Optional[int], typing.Optional[str], typing.Optional[str], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[str], typing.Optional[str], typing.Optional[int]) -> None
        self.execution_number = execution_number # type: typing.Optional[int]
        self.job_document = job_document # type: typing.Optional[str]
        self.job_id = job_id # type: typing.Optional[str]
        self.last_updated_at = last_updated_at # type: typing.Optional[datetime.datetime]
        self.queued_at = queued_at # type: typing.Optional[datetime.datetime]
        self.started_at = started_at # type: typing.Optional[datetime.datetime]
        self.status = status # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]
        self.version_number = version_number # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionData
        new = cls()
        val = payload.get('executionNumber')
        if val:
            new.execution_number = val
        val = payload.get('jobDocument')
        if val:
            new.job_document = val
        val = payload.get('jobId')
        if val:
            new.job_id = val
        val = payload.get('lastUpdatedAt')
        if val:
            new.last_updated_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('queuedAt')
        if val:
            new.queued_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('startedAt')
        if val:
            new.started_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('status')
        if val:
            new.status = val
        val = payload.get('thingName')
        if val:
            new.thing_name = val
        val = payload.get('versionNumber')
        if val:
            new.version_number = val
        return new

class JobExecutionState(object):
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
        if val:
            new.status = val
        val = payload.get('statusDetails')
        if val:
            new.status_details = val
        val = payload.get('versionNumber')
        if val:
            new.version_number = val
        return new

class JobExecutionSummary(object):
    def __init__(self, execution_number=None, last_updated_at=None, queued_at=None, started_at=None):
        # type: (typing.Optional[int], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime], typing.Optional[datetime.datetime]) -> None
        self.execution_number = execution_number # type: typing.Optional[int]
        self.last_updated_at = last_updated_at # type: typing.Optional[datetime.datetime]
        self.queued_at = queued_at # type: typing.Optional[datetime.datetime]
        self.started_at = started_at # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionSummary
        new = cls()
        val = payload.get('executionNumber')
        if val:
            new.execution_number = val
        val = payload.get('lastUpdatedAt')
        if val:
            new.last_updated_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('queuedAt')
        if val:
            new.queued_at = datetime.datetime.fromtimestamp(val)
        val = payload.get('startedAt')
        if val:
            new.started_at = datetime.datetime.fromtimestamp(val)
        return new

class JobExecutionsChangedEvent(object):
    def __init__(self, jobs=None, timestamp=None):
        # type: (typing.Optional[JobExecutionsChangedJobs], typing.Optional[datetime.datetime]) -> None
        self.jobs = jobs # type: typing.Optional[JobExecutionsChangedJobs]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionsChangedEvent
        new = cls()
        val = payload.get('jobs')
        if val:
            new.jobs = JobExecutionsChangedJobs.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class JobExecutionsChangedEventsSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class JobExecutionsChangedJobs(object):
    def __init__(self, job_execution_state=None):
        # type: (typing.Optional[typing.List[JobExecutionSummary]]) -> None
        self.job_execution_state = job_execution_state # type: typing.Optional[typing.List[JobExecutionSummary]]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> JobExecutionsChangedJobs
        new = cls()
        val = payload.get('JobExecutionState')
        if val:
            new.job_execution_state = [JobExecutionSummary.from_payload(i) for i in val]
        return new

class NextJobExecutionChangedEvent(object):
    def __init__(self, execution=None, timestamp=None):
        # type: (typing.Optional[JobExecutionData], typing.Optional[datetime.datetime]) -> None
        self.execution = execution # type: typing.Optional[JobExecutionData]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> NextJobExecutionChangedEvent
        new = cls()
        val = payload.get('execution')
        if val:
            new.execution = JobExecutionData.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class NextJobExecutionChangedEventsSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class RejectedError(object):
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
        if val:
            new.client_token = val
        val = payload.get('code')
        if val:
            new.code = val
        val = payload.get('executionState')
        if val:
            new.execution_state = JobExecutionState.from_payload(val)
        val = payload.get('message')
        if val:
            new.message = val
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class StartDescribeJobExecutionResponse(object):
    def __init__(self, client_token=None, execution=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[JobExecutionData], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution = execution # type: typing.Optional[JobExecutionData]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> StartDescribeJobExecutionResponse
        new = cls()
        val = payload.get('clientToken')
        if val:
            new.client_token = val
        val = payload.get('execution')
        if val:
            new.execution = JobExecutionData.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class StartNextPendingJobExecutionRequest(object):
    def __init__(self, client_token=None, status_details=None, step_timeout_in_minutes=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[typing.Dict[str, str]], typing.Optional[int], typing.Optional[str]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.status_details = status_details # type: typing.Optional[typing.Dict[str, str]]
        self.step_timeout_in_minutes = step_timeout_in_minutes # type: typing.Optional[int]
        self.thing_name = thing_name # type: typing.Optional[str]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token:
            payload['clientToken'] = self.client_token
        if self.status_details:
            payload['statusDetails'] = self.status_details
        if self.step_timeout_in_minutes:
            payload['stepTimeoutInMinutes'] = self.step_timeout_in_minutes
        return payload

class StartNextPendingJobExecutionSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class UpdateJobExecutionRequest(object):
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
        if self.client_token:
            payload['clientToken'] = self.client_token
        if self.execution_number:
            payload['executionNumber'] = self.execution_number
        if self.expected_version:
            payload['expectedVersion'] = self.expected_version
        if self.include_job_document:
            payload['includeJobDocument'] = self.include_job_document
        if self.include_job_execution_state:
            payload['includeJobExecutionState'] = self.include_job_execution_state
        if self.status:
            payload['status'] = self.status
        if self.status_details:
            payload['statusDetails'] = self.status_details
        return payload

class UpdateJobExecutionResponse(object):
    def __init__(self, client_token=None, execution_state=None, job_document=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[JobExecutionState], typing.Optional[str], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.execution_state = execution_state # type: typing.Optional[JobExecutionState]
        self.job_document = job_document # type: typing.Optional[str]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> UpdateJobExecutionResponse
        new = cls()
        val = payload.get('clientToken')
        if val:
            new.client_token = val
        val = payload.get('executionState')
        if val:
            new.execution_state = JobExecutionState.from_payload(val)
        val = payload.get('jobDocument')
        if val:
            new.job_document = val
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class UpdateJobExecutionSubscriptionRequest(object):
    def __init__(self, job_id=None, thing_name=None):
        # type: (typing.Optional[str], typing.Optional[str]) -> None
        self.job_id = job_id # type: typing.Optional[str]
        self.thing_name = thing_name # type: typing.Optional[str]

