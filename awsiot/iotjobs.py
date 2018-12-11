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

    def describe_job_execution(self, input):
        # type: (DescribeJobExecutionRequest) -> concurrent.futures.Future
        if not input.job_id:
            raise ValueError("input.job_id is required")
        if not input.thing_name:
            raise ValueError("input.thing_name is required")

        request_topic = '$aws/things/{0.thing_name}/jobs/{0.job_id}/get'.format(input)
        request_payload = input.to_payload()
        request_payload_nonce_field = 'clientToken'

        response_subscriptions = [
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get/accepted'.format(input),
                response_payload_to_class_fn=DescribeJobExecutionResponse.from_payload,
                response_payload_nonce_field='clientToken',
            ),
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/get/rejected'.format(input),
                response_payload_to_class_fn=RejectedError.from_payload,
                response_payload_nonce_field='clientToken',
            ),
        ]

        return self._nonce_rpc_operation(request_topic, request_payload, request_payload_nonce_field, response_subscriptions)

    def get_job_executions_changed(self, input, handler):
        # type: (GetJobExecutionsChangedRequest, JobExecutionsChangedEventsHandler) -> concurrent.futures.Future
        if not input.thing_name:
            raise ValueError("input.thing_name is required")

        if not handler.on_job_executions_changed:
            raise ValueError("handler.on_job_executions_changed is required")

        subscriptions = [
            awsiot._SubscriptionInfo(
                topic='$aws/things/{0.thing_name}/jobs/notify'.format(input),
                callback=handler.on_job_executions_changed,
                payload_class=JobExecutionsChangedEvent,
            ),
        ]

        return self._subscribe_operation(subscriptions)

    def get_next_job_execution_changed(self, input, handler):
        # type: (GetNextJobExecutionChangedRequest, NextJobExecutionChangedEventsHandler) -> concurrent.futures.Future
        if not input.thing_name:
            raise ValueError("input.thing_name is required")

        if not handler.on_next_job_execution_changed:
            raise ValueError("handler.on_next_job_execution_changed is required")

        subscriptions = [
            awsiot._SubscriptionInfo(
                topic='$aws/things/{0.thing_name}/jobs/notify-next'.format(input),
                callback=handler.on_next_job_execution_changed,
                payload_class=NextJobExecutionChangedEvent,
            ),
        ]

        return self._subscribe_operation(subscriptions)

    def get_pending_job_executions(self, input):
        # type: (GetPendingJobExecutionsRequest) -> concurrent.futures.Future
        if not input.thing_name:
            raise ValueError("input.thing_name is required")

        request_topic = '$aws/things/{0.thing_name}/jobs/get'.format(input)
        request_payload = input.to_payload()
        request_payload_nonce_field = 'clientToken'

        response_subscriptions = [
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/get/accepted'.format(input),
                response_payload_to_class_fn=GetPendingJobExecutionsResponse.from_payload,
                response_payload_nonce_field='clientToken',
            ),
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/get/rejected'.format(input),
                response_payload_to_class_fn=RejectedError.from_payload,
                response_payload_nonce_field='clientToken',
            ),
        ]

        return self._nonce_rpc_operation(request_topic, request_payload, request_payload_nonce_field, response_subscriptions)

    def start_next_pending_job_execution(self, input):
        # type: (StartNextPendingJobExecutionRequest) -> concurrent.futures.Future
        if not input.thing_name:
            raise ValueError("input.thing_name is required")

        request_topic = '$aws/things/{0.thing_name}/jobs/start-next'.format(input)
        request_payload = input.to_payload()
        request_payload_nonce_field = 'clientToken'

        response_subscriptions = [
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/start-next/accepted'.format(input),
                response_payload_to_class_fn=StartDescribeJobExecutionResponse.from_payload,
                response_payload_nonce_field='clientToken',
            ),
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/start-next/rejected'.format(input),
                response_payload_to_class_fn=RejectedError.from_payload,
                response_payload_nonce_field='clientToken',
            ),
        ]

        return self._nonce_rpc_operation(request_topic, request_payload, request_payload_nonce_field, response_subscriptions)

    def update_job_execution(self, input):
        # type: (UpdateJobExecutionRequest) -> concurrent.futures.Future
        if not input.thing_name:
            raise ValueError("input.thing_name is required")
        if not input.job_id:
            raise ValueError("input.job_id is required")

        request_topic = '$aws/things/{0.thing_name}/jobs/{0.job_id}/update'.format(input)
        request_payload = input.to_payload()
        request_payload_nonce_field = 'clientToken'

        response_subscriptions = [
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/accepted'.format(input),
                response_payload_to_class_fn=UpdateJobExecutionResponse.from_payload,
                response_payload_nonce_field='clientToken',
            ),
            awsiot._NonceRpcSubscription(
                topic='$aws/things/{0.thing_name}/jobs/{0.job_id}/update/rejected'.format(input),
                response_payload_to_class_fn=RejectedError.from_payload,
                response_payload_nonce_field='clientToken',
            ),
        ]

        return self._nonce_rpc_operation(request_topic, request_payload, request_payload_nonce_field, response_subscriptions)

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

class GetJobExecutionsChangedRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class GetNextJobExecutionChangedRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
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

class JobExecutionsChangedEventsHandler:
    def __init__(self):
        self.on_job_executions_changed = None # type: typing.Callable[[JobExecutionsChangedEvent], None]

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

class NextJobExecutionChangedEventsHandler:
    def __init__(self):
        self.on_next_job_execution_changed = None # type: typing.Callable[[NextJobExecutionChangedEvent], None]

class RejectedError(Exception):
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

