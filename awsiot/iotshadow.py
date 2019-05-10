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

class IotShadowClient(awsiot.MqttServiceClient):

    def publish_delete_shadow(self, request, qos):
        # type: (DeleteShadowRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-pub-sub-topic

        Parameters:
        request - `DeleteShadowRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/delete'.format(request),
            qos=qos,
            payload=None)

    def publish_get_shadow(self, request, qos):
        # type: (GetShadowRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-pub-sub-topic

        Parameters:
        request - `GetShadowRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/get'.format(request),
            qos=qos,
            payload=None)

    def publish_update_shadow(self, request, qos):
        # type: (UpdateShadowRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-pub-sub-topic

        Parameters:
        request - `UpdateShadowRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/update'.format(request),
            qos=qos,
            payload=request.to_payload())

    def subscribe_to_delete_shadow_accepted(self, request, qos, callback):
        # type: (DeleteShadowSubscriptionRequest, int, typing.Callable[[DeleteShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-accepted-pub-sub-topic

        Parameters:
        request - `DeleteShadowSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `DeleteShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/delete/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=DeleteShadowResponse.from_payload)

    def subscribe_to_delete_shadow_rejected(self, request, qos, callback):
        # type: (DeleteShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-rejected-pub-sub-topic

        Parameters:
        request - `DeleteShadowSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/delete/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_get_shadow_accepted(self, request, qos, callback):
        # type: (GetShadowSubscriptionRequest, int, typing.Callable[[GetShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-accepted-pub-sub-topic

        Parameters:
        request - `GetShadowSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `GetShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/get/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=GetShadowResponse.from_payload)

    def subscribe_to_get_shadow_rejected(self, request, qos, callback):
        # type: (GetShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-rejected-pub-sub-topic

        Parameters:
        request - `GetShadowSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/get/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_shadow_delta_updated_events(self, request, qos, callback):
        # type: (ShadowDeltaUpdatedSubscriptionRequest, int, typing.Callable[[ShadowDeltaUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-delta-pub-sub-topic

        Parameters:
        request - `ShadowDeltaUpdatedSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ShadowDeltaUpdatedEvent`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/delta'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ShadowDeltaUpdatedEvent.from_payload)

    def subscribe_to_shadow_updated_events(self, request, qos, callback):
        # type: (ShadowUpdatedSubscriptionRequest, int, typing.Callable[[ShadowUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-documents-pub-sub-topic

        Parameters:
        request - `ShadowUpdatedSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ShadowUpdatedEvent`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/documents'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ShadowUpdatedEvent.from_payload)

    def subscribe_to_update_shadow_accepted(self, request, qos, callback):
        # type: (UpdateShadowSubscriptionRequest, int, typing.Callable[[UpdateShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-accepted-pub-sub-topic

        Parameters:
        request - `UpdateShadowSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `UpdateShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=UpdateShadowResponse.from_payload)

    def subscribe_to_update_shadow_rejected(self, request, qos, callback):
        # type: (UpdateShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-rejected-pub-sub-topic

        Parameters:
        request - `UpdateShadowSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

class DeleteShadowRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class DeleteShadowResponse(awsiot.ModeledClass):
    __slots__ = ['timestamp', 'version']

    def __init__(self, timestamp=None, version=None):
        # type: (typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> DeleteShadowResponse
        new = cls()
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val is not None:
            new.version = val
        return new

class DeleteShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ErrorResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'code', 'message', 'timestamp']

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
        if val is not None:
            new.client_token = val
        val = payload.get('code')
        if val is not None:
            new.code = val
        val = payload.get('message')
        if val is not None:
            new.message = val
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class GetShadowRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class GetShadowResponse(awsiot.ModeledClass):
    __slots__ = ['metadata', 'state', 'timestamp', 'version']

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
        if val is not None:
            new.metadata = ShadowMetadata.from_payload(val)
        val = payload.get('state')
        if val is not None:
            new.state = ShadowStateWithDelta.from_payload(val)
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val is not None:
            new.version = val
        return new

class GetShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ShadowDeltaUpdatedEvent(awsiot.ModeledClass):
    __slots__ = ['metadata', 'state', 'timestamp', 'version']

    def __init__(self, metadata=None, state=None, timestamp=None, version=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[datetime.datetime], typing.Optional[int]) -> None
        self.metadata = metadata # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.state = state # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowDeltaUpdatedEvent
        new = cls()
        val = payload.get('metadata')
        if val is not None:
            new.metadata = val
        val = payload.get('state')
        if val is not None:
            new.state = val
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val is not None:
            new.version = val
        return new

class ShadowDeltaUpdatedSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class ShadowMetadata(awsiot.ModeledClass):
    __slots__ = ['desired', 'reported']

    def __init__(self, desired=None, reported=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]]) -> None
        self.desired = desired # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.reported = reported # type: typing.Optional[typing.Dict[str, typing.Any]]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowMetadata
        new = cls()
        val = payload.get('desired')
        if val is not None:
            new.desired = val
        val = payload.get('reported')
        if val is not None:
            new.reported = val
        return new

class ShadowState(awsiot.ModeledClass):
    __slots__ = ['desired', 'reported']

    def __init__(self, desired=None, reported=None):
        # type: (typing.Optional[typing.Dict[str, typing.Any]], typing.Optional[typing.Dict[str, typing.Any]]) -> None
        self.desired = desired # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.reported = reported # type: typing.Optional[typing.Dict[str, typing.Any]]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowState
        new = cls()
        val = payload.get('desired')
        if val is not None:
            new.desired = val
        val = payload.get('reported')
        if val is not None:
            new.reported = val
        return new

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.desired is not None:
            payload['desired'] = self.desired
        if self.reported is not None:
            payload['reported'] = self.reported
        return payload

class ShadowStateWithDelta(awsiot.ModeledClass):
    __slots__ = ['delta', 'desired', 'reported']

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
        if val is not None:
            new.delta = val
        val = payload.get('desired')
        if val is not None:
            new.desired = val
        val = payload.get('reported')
        if val is not None:
            new.reported = val
        return new

class ShadowUpdatedEvent(awsiot.ModeledClass):
    __slots__ = ['current', 'previous', 'timestamp']

    def __init__(self, current=None, previous=None, timestamp=None):
        # type: (typing.Optional[ShadowUpdatedSnapshot], typing.Optional[ShadowUpdatedSnapshot], typing.Optional[datetime.datetime]) -> None
        self.current = current # type: typing.Optional[ShadowUpdatedSnapshot]
        self.previous = previous # type: typing.Optional[ShadowUpdatedSnapshot]
        self.timestamp = timestamp # type: typing.Optional[datetime.datetime]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowUpdatedEvent
        new = cls()
        val = payload.get('current')
        if val is not None:
            new.current = ShadowUpdatedSnapshot.from_payload(val)
        val = payload.get('previous')
        if val is not None:
            new.previous = ShadowUpdatedSnapshot.from_payload(val)
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        return new

class ShadowUpdatedSnapshot(awsiot.ModeledClass):
    __slots__ = ['metadata', 'state', 'version']

    def __init__(self, metadata=None, state=None, version=None):
        # type: (typing.Optional[ShadowMetadata], typing.Optional[ShadowState], typing.Optional[int]) -> None
        self.metadata = metadata # type: typing.Optional[ShadowMetadata]
        self.state = state # type: typing.Optional[ShadowState]
        self.version = version # type: typing.Optional[int]

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowUpdatedSnapshot
        new = cls()
        val = payload.get('metadata')
        if val is not None:
            new.metadata = ShadowMetadata.from_payload(val)
        val = payload.get('state')
        if val is not None:
            new.state = ShadowState.from_payload(val)
        val = payload.get('version')
        if val is not None:
            new.version = val
        return new

class ShadowUpdatedSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class UpdateShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'state', 'thing_name', 'version']

    def __init__(self, client_token=None, state=None, thing_name=None, version=None):
        # type: (typing.Optional[str], typing.Optional[ShadowState], typing.Optional[str], typing.Optional[int]) -> None
        self.client_token = client_token # type: typing.Optional[str]
        self.state = state # type: typing.Optional[ShadowState]
        self.thing_name = thing_name # type: typing.Optional[str]
        self.version = version # type: typing.Optional[int]

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        if self.state is not None:
            payload['state'] = self.state.to_payload()
        if self.version is not None:
            payload['version'] = self.version
        return payload

class UpdateShadowResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'metadata', 'state', 'timestamp', 'version']

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
        if val is not None:
            new.client_token = val
        val = payload.get('metadata')
        if val is not None:
            new.metadata = ShadowMetadata.from_payload(val)
        val = payload.get('state')
        if val is not None:
            new.state = ShadowState.from_payload(val)
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val is not None:
            new.version = val
        return new

class UpdateShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

