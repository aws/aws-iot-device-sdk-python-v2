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

# TODO:
# - handle required fields from model differently?
# - better type-checking of callback signatures (or even better remove callbacks from API)
# - comments
# - unsubscribe
# - python2/3 compatibility https://docs.python.org/3/howto/pyporting.html

import aws_crt.mqtt
import concurrent.futures
import datetime
import json
import typing
import uuid

class IotShadowClient(object):
    def __init__(self, mqtt_connection):
        # type: (aws_crt.mqtt.Connection) -> None
        self.mqtt_connection = mqtt_connection # type: aws_crt.mqtt.Connection

    def delete_shadow(self, input):
        # type: (DeleteShadowRequest) -> concurrent.futures.Future
        request_topic = '$aws/things/{0.thing_name}/shadow/delete'.format(input)
        subscriptions = [
            _RpcSubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/delete/accepted'.format(input),
                payload_class=DeleteShadowResponse,
                is_error=False,
            ),
            _RpcSubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/delete/rejected'.format(input),
                payload_class=ErrorResponse,
                is_error=True,
            ),
        ]

        return self._rpc_operation(request_topic, input, subscriptions)

    def get_shadow(self, input):
        # type: (GetShadowRequest) -> concurrent.futures.Future
        request_topic = '$aws/things/{0.thing_name}/shadow/get'.format(input)
        subscriptions = [
            _RpcSubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/get/accepted'.format(input),
                payload_class=GetShadowResponse,
                is_error=False,
            ),
            _RpcSubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/get/rejected'.format(input),
                payload_class=ErrorResponse,
                is_error=True,
            ),
        ]

        return self._rpc_operation(request_topic, input, subscriptions)

    def subscribe_to_shadow_deltas(self, input, handler):
        # type: (SubscribeToShadowDeltasRequest, ShadowDeltaEventsHandler) -> concurrent.futures.Future

        if not handler.on_delta:
            raise ValueError("handler.on_delta is required")

        subscriptions = [
            _SubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/update/delta'.format(input),
                callback=handler.on_delta,
                payload_class=ShadowDeltaEvent,
            ),
        ]

        return self._subscribe_operation(subscriptions)

    def subscribe_to_shadow_updates(self, input, handler):
        # type: (SubscribeToShadowUpdatesRequest, ShadowUpdateEventsHandler) -> concurrent.futures.Future

        if not handler.on_updated:
            raise ValueError("handler.on_updated is required")

        subscriptions = [
            _SubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/update/documents'.format(input),
                callback=handler.on_updated,
                payload_class=ShadowUpdateEvent,
            ),
        ]

        return self._subscribe_operation(subscriptions)

    def update_shadow(self, input):
        # type: (UpdateShadowRequest) -> concurrent.futures.Future
        request_topic = '$aws/things/{0.thing_name}/shadow/update'.format(input)
        subscriptions = [
            _RpcSubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/update/accepted'.format(input),
                payload_class=UpdateShadowResponse,
                is_error=False,
            ),
            _RpcSubscriptionInfo(
                topic='$aws/things/{0.thing_name}/shadow/update/rejected'.format(input),
                payload_class=ErrorResponse,
                is_error=True,
            ),
        ]

        return self._rpc_operation(request_topic, input, subscriptions)

    def _rpc_operation(self, pub_topic, input, subscriptions):
        # type: (str, typing.Any, typing.List[_RpcSubscriptionInfo]) -> concurrent.futures.Future
        """
        Performs a 'Remote Procedure Call' style operation for an MQTT service.

        Parameters:
        pub_topic - Topic for request message.
        input - Input object for request message.
        subscriptions - List of _RpcSubscriptionInfos, one for each possible response.

        Returns a Future that will contain the outcome of the operation.
        A response from a non-error topic becomes a valid result in the Future.
        A response from an error topic becomes an Exception in the Future.
        Any other exception that occurs as part of the RPC becomes an exception in the Future.
        """
        if not input.client_token:
            input.client_token = str(uuid.uuid4())
        input_payload = input.to_payload()
        input_json_payload = json.dumps(input_payload)

        future = concurrent.futures.Future() # type: concurrent.futures.Future

        suback_counter = ['suback'] * len(subscriptions)

        # callback counts subacks, when last one is received the request is published.
        def on_suback(packet_id):
            try:
                # count supacks by popping an entry out of this list
                if suback_counter:
                    suback_counter.pop()
                    if not suback_counter:
                        # all subscriptions succeeded, publish request
                        self.mqtt_connection.publish(pub_topic, input_json_payload, 1, False, None)
            except Exception as e:
                future.set_exception(e)

        for sub in subscriptions:
            # callback transforms payload into appropriate class and delivers it to the future
            def on_response(topic, json_payload):
                try:
                    payload = json.loads(json_payload)
                    result = sub.payload_class.from_payload(payload)
                    if sub.is_error:
                        future.set_exception(result)
                    else:
                        future.set_result(result)
                except Exception as e:
                    future.set_exception(e)

            self.mqtt_connection.subscribe(sub.topic, 1, on_response, on_suback)

        return future

    def _subscribe_operation(self, subscriptions):
        # type: (typing.List[_SubscriptionInfo]) -> concurrent.futures.Future
        """
        Performs a 'Subscribe' style operation for an MQTT service.

        Parameters:
        subscriptions - List of _SubscriptionInfos, one for each possible response.

        Returns a Future that will contain None when all subscriptions have been acknowledged by the server.
        """

        future = concurrent.futures.Future() # type: concurrent.futures.Future

        # callback informs Future when all subacks received
        suback_counter = ['suback'] * len(subscriptions)
        def on_suback(packet_id):
            # count supacks by popping an entry out of this list
            if suback_counter:
                suback_counter.pop()
                if not suback_counter:
                    # all subscriptions succeeded
                    future.set_result(None)

        for sub in subscriptions:
            def callback_wrapper(topic, json_payload):
                try:
                    payload = json.loads(json_payload)
                    event = sub.payload_class.from_payload(payload)
                    sub.callback(event)
                except:
                    # can't deliver payload, invoke callback with None
                    sub.callback(None)

            self.mqtt_connection.subscribe(sub.topic, 1, callback_wrapper, on_suback)

        return future

T = typing.TypeVar('T')

class _RpcSubscriptionInfo(object):
    # type: typing.Generic[T]

    def __init__(self, topic, payload_class, is_error):
        # type: (str, typing.Type[T], bool) -> None
        self.topic = topic # type: str
        self.payload_class = payload_class # type: typing.Type[T]
        self.is_error = is_error # type: bool

class _SubscriptionInfo(object):
    # type: typing.Generic[T]

    def __init__(self, topic, callback, payload_class):
        # type: (str, typing.Callable[[T], None], typing.Type[T]) -> None
        self.topic = topic # type: str
        self.callback = callback # type: typing.Callable[[T], None]
        self.payload_class = payload_class # typing.Type[T]

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

class ErrorResponse(Exception):
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

class ShadowDeltaEventsHandler:
    def __init__(self):
        self.on_delta = None # type: typing.Callable[[ShadowDeltaEvent], None]

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

class ShadowUpdateEventsHandler:
    def __init__(self):
        self.on_updated = None # type: typing.Callable[[ShadowUpdateEvent], None]

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

class SubscribeToShadowDeltasRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

class SubscribeToShadowUpdatesRequest(object):
    def __init__(self, thing_name=None):
        # type: (typing.Optional[str]) -> None
        self.thing_name = thing_name # type: typing.Optional[str]

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

