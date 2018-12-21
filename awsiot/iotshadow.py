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

class IotShadowClient(awsiot.MqttServiceClient):

    def publish_delete(self, request):
        # type: (DeleteShadowRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-pub-sub-topic

        Parameters:
        request - `DeleteShadowRequest` instance.

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/delete'.format(request),
            payload=None)

    def publish_get(self, request):
        # type: (GetShadowRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-pub-sub-topic

        Parameters:
        request - `GetShadowRequest` instance.

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/get'.format(request),
            payload=None)

    def publish_update(self, request):
        # type: (UpdateShadowRequest) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-pub-sub-topic

        Parameters:
        request - `UpdateShadowRequest` instance.

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/update'.format(request),
            payload=request.to_payload())

    def subscribe_to_delete_accepted(self, request, on_accepted):
        # type: (DeleteShadowSubscriptionRequest, typing.Callable[[DeleteShadowResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-accepted-pub-sub-topic

        Parameters:
        request - `DeleteShadowSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `DeleteShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/delete/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=DeleteShadowResponse.from_payload)

    def subscribe_to_delete_rejected(self, request, on_rejected):
        # type: (DeleteShadowSubscriptionRequest, typing.Callable[[ErrorResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-rejected-pub-sub-topic

        Parameters:
        request - `DeleteShadowSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/delete/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_delta_events(self, request, on_delta):
        # type: (ShadowDeltaEventsSubscriptionRequest, typing.Callable[[ShadowDeltaEvent], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-delta-pub-sub-topic

        Parameters:
        request - `ShadowDeltaEventsSubscriptionRequest` instance.
        on_delta - Callback to invoke each time the on_delta event is received.
                The callback should take 1 argument of type `ShadowDeltaEvent`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_delta:
            raise ValueError("on_delta is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/update/delta'.format(request),
            callback=on_delta,
            payload_to_class_fn=ShadowDeltaEvent.from_payload)

    def subscribe_to_get_accepted(self, request, on_accepted):
        # type: (GetShadowSubscriptionRequest, typing.Callable[[GetShadowResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-accepted-pub-sub-topic

        Parameters:
        request - `GetShadowSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `GetShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/get/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=GetShadowResponse.from_payload)

    def subscribe_to_get_rejected(self, request, on_rejected):
        # type: (GetShadowSubscriptionRequest, typing.Callable[[ErrorResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-rejected-pub-sub-topic

        Parameters:
        request - `GetShadowSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/get/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_update_accepted(self, request, on_accepted):
        # type: (UpdateShadowSubscriptionRequest, typing.Callable[[UpdateShadowResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-accepted-pub-sub-topic

        Parameters:
        request - `UpdateShadowSubscriptionRequest` instance.
        on_accepted - Callback to invoke each time the on_accepted event is received.
                The callback should take 1 argument of type `UpdateShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/accepted'.format(request),
            callback=on_accepted,
            payload_to_class_fn=UpdateShadowResponse.from_payload)

    def subscribe_to_update_events(self, request, on_updated):
        # type: (ShadowUpdateEventsSubscriptionRequest, typing.Callable[[ShadowUpdateEvent], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-documents-pub-sub-topic

        Parameters:
        request - `ShadowUpdateEventsSubscriptionRequest` instance.
        on_updated - Callback to invoke each time the on_updated event is received.
                The callback should take 1 argument of type `ShadowUpdateEvent`.
                The callback is not expected to return anything.

        Returns a concurrent.futures.Future, whose result will be None if the
        subscription is successful. The Future's result will be an exception
        if the subscription is unsuccessful.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not on_updated:
            raise ValueError("on_updated is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/update/documents'.format(request),
            callback=on_updated,
            payload_to_class_fn=ShadowUpdateEvent.from_payload)

    def subscribe_to_update_rejected(self, request, on_rejected):
        # type: (UpdateShadowSubscriptionRequest, typing.Callable[[ErrorResponse], None]) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-rejected-pub-sub-topic

        Parameters:
        request - `UpdateShadowSubscriptionRequest` instance.
        on_rejected - Callback to invoke each time the on_rejected event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/rejected'.format(request),
            callback=on_rejected,
            payload_to_class_fn=ErrorResponse.from_payload)

class DeleteShadowRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class DeleteShadowResponse(object):
    def __init__(self, timestamp=None, version=None):
        # type: (typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> DeleteShadowResponse
        new = cls()
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val:
            new.version = val
        return new

class DeleteShadowSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ErrorResponse(object):
    def __init__(self, client_token=None, code=None, message=None, timestamp=None):
        # type: (typing.Optional[str], typing.Optional[int], typing.Optional[str], typing.Optional[datetime.datetime]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.code = code # type: typing.Optional[int]
        self.message = message # type: typing.Optional[str]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ErrorResponse
        new = cls()
        val = payload.get('clientToken')
        if val:
            new.client_token = val
        val = payload.get('code')
        if val:
            new.code = val
        val = payload.get('message')
        if val:
            new.message = val
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class GetShadowRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class GetShadowResponse(object):
    def __init__(self, metadata=None, state=None, timestamp=None, version=None):
        # type: (typing.Optional[ShadowMetadata], typing.Optional[ShadowStateWithDelta], typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.metadata = metadata # type: typing.Optional[ShadowMetadata]
        self.state = state # type: typing.Optional[ShadowStateWithDelta]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> GetShadowResponse
        new = cls()
        val = payload.get('metadata')
        if val:
            new.metadata = ShadowMetadata.from_payload(val)
        val = payload.get('state')
        if val:
            new.state = ShadowStateWithDelta.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val:
            new.version = val
        return new

class GetShadowSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ShadowDeltaEvent(object):
    def __init__(self, metadata=None, state=None, timestamp=None, version=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.metadata = metadata # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.state = state # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowDeltaEvent
        new = cls()
        val = payload.get('metadata')
        if val:
            new.metadata = val
        val = payload.get('state')
        if val:
            new.state = val
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val:
            new.version = val
        return new

class ShadowDeltaEventsSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ShadowMetadata(object):
    def __init__(self, desired=None, reported=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]]) -> None
        self.desired = desired # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.reported = reported # type: typing.Optional[typing.Dict[str, typing.Any]]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowMetadata
        new = cls()
        val = payload.get('desired')
        if val:
            new.desired = val
        val = payload.get('reported')
        if val:
            new.reported = val
        return new

class ShadowState(object):
    def __init__(self, desired=None, reported=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]]) -> None
        self.desired = desired # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.reported = reported # type: typing.Optional[typing.Dict[str, typing.Any]]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowState
        new = cls()
        val = payload.get('desired')
        if val:
            new.desired = val
        val = payload.get('reported')
        if val:
            new.reported = val
        return new

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.desired:
            payload['desired'] = self.desired
        if self.reported:
            payload['reported'] = self.reported
        return payload

class ShadowStateWithDelta(object):
    def __init__(self, delta=None, desired=None, reported=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]]) -> None
        self.delta = delta # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.desired = desired # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.reported = reported # type: typing.Optional[typing.Dict[str, typing.Any]]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowStateWithDelta
        new = cls()
        val = payload.get('delta')
        if val:
            new.delta = val
        val = payload.get('desired')
        if val:
            new.desired = val
        val = payload.get('reported')
        if val:
            new.reported = val
        return new

class ShadowUpdateEvent(object):
    def __init__(self, current=None, previous=None, timestamp=None):
        # type: (typing.Optional[ShadowUpdateSnapshot], typing.Optional[ShadowUpdateSnapshot], typing.Optional[datetime.datetime]) -> None
        self.current = current # type: typing.Optional[ShadowUpdateSnapshot]
        self.previous = previous # type: typing.Optional[ShadowUpdateSnapshot]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowUpdateEvent
        new = cls()
        val = payload.get('current')
        if val:
            new.current = ShadowUpdateSnapshot.from_payload(val)
        val = payload.get('previous')
        if val:
            new.previous = ShadowUpdateSnapshot.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class ShadowUpdateEventsSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ShadowUpdateSnapshot(object):
    def __init__(self, metadata=None, state=None, version=None):
        # type: (typing.Optional[ShadowMetadata], typing.Optional[ShadowState], typing.Optional[int]) -> None
        self.metadata = metadata # type: typing.Optional[ShadowMetadata]
        self.state = state # type: typing.Optional[ShadowState]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowUpdateSnapshot
        new = cls()
        val = payload.get('metadata')
        if val:
            new.metadata = ShadowMetadata.from_payload(val)
        val = payload.get('state')
        if val:
            new.state = ShadowState.from_payload(val)
        val = payload.get('version')
        if val:
            new.version = val
        return new

class UpdateShadowRequest(object):
    def __init__(self, client_token=None, state=None, thing_name=None, version=None):
        # type: (typing.Optional[str], typing.Optional[ShadowState], typing.Optional[str], typing.Optional[int]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.state = state # type: typing.Optional[ShadowState]
        self.thing_name = thing_name # type: typing.Optional[str]
        self.version = version # type: typing.Optional[int]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token:
            payload['clientToken'] = self.client_token
        if self.state:
            payload['state'] = self.state.to_payload()
        if self.version:
            payload['version'] = self.version
        return payload

class UpdateShadowResponse(object):
    def __init__(self, client_token=None, metadata=None, state=None, timestamp=None, version=None):
        # type: (typing.Optional[str], typing.Optional[ShadowMetadata], typing.Optional[ShadowState], typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.metadata = metadata # type: typing.Optional[ShadowMetadata]
        self.state = state # type: typing.Optional[ShadowState]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> UpdateShadowResponse
        new = cls()
        val = payload.get('clientToken')
        if val:
            new.client_token = val
        val = payload.get('metadata')
        if val:
            new.metadata = ShadowMetadata.from_payload(val)
        val = payload.get('state')
        if val:
            new.state = ShadowState.from_payload(val)
        val = payload.get('timestamp')
        if val:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val:
            new.version = val
        return new

class UpdateShadowSubscriptionRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

