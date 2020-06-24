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

import awsiot
import concurrent.futures
import datetime
import typing

class IotShadowClient(awsiot.MqttServiceClient):

    def publish_delete_named_shadow(self, request, qos):
        # type: (DeleteNamedShadowRequest, int) -> concurrent.futures.Future
        """
        Parameters:
        request - `DeleteNamedShadowRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/delete'.format(request),
            qos=qos,
            payload=request.to_payload())

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
            payload=request.to_payload())

    def publish_get_named_shadow(self, request, qos):
        # type: (GetNamedShadowRequest, int) -> concurrent.futures.Future
        """
        Parameters:
        request - `GetNamedShadowRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/get'.format(request),
            qos=qos,
            payload=request.to_payload())

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
            payload=request.to_payload())

    def publish_update_named_shadow(self, request, qos):
        # type: (UpdateNamedShadowRequest, int) -> concurrent.futures.Future
        """
        Parameters:
        request - `UpdateNamedShadowRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        return self._publish_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/update'.format(request),
            qos=qos,
            payload=request.to_payload())

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

    def subscribe_to_delete_named_shadow_accepted(self, request, qos, callback):
        # type: (DeleteNamedShadowSubscriptionRequest, int, typing.Callable[[DeleteShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `DeleteNamedShadowSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/delete/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=DeleteShadowResponse.from_payload)

    def subscribe_to_delete_named_shadow_rejected(self, request, qos, callback):
        # type: (DeleteNamedShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `DeleteNamedShadowSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/delete/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

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

    def subscribe_to_get_named_shadow_accepted(self, request, qos, callback):
        # type: (GetNamedShadowSubscriptionRequest, int, typing.Callable[[GetShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `GetNamedShadowSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/get/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=GetShadowResponse.from_payload)

    def subscribe_to_get_named_shadow_rejected(self, request, qos, callback):
        # type: (GetNamedShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `GetNamedShadowSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/get/rejected'.format(request),
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

    def subscribe_to_named_shadow_delta_updated_events(self, request, qos, callback):
        # type: (NamedShadowDeltaUpdatedSubscriptionRequest, int, typing.Callable[[ShadowDeltaUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `NamedShadowDeltaUpdatedSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/update/delta'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ShadowDeltaUpdatedEvent.from_payload)

    def subscribe_to_named_shadow_updated_events(self, request, qos, callback):
        # type: (NamedShadowUpdatedSubscriptionRequest, int, typing.Callable[[ShadowUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `NamedShadowUpdatedSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")
        if not request.thing_name:
            raise ValueError("request.thing_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/update/documents'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ShadowUpdatedEvent.from_payload)

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

    def subscribe_to_update_named_shadow_accepted(self, request, qos, callback):
        # type: (UpdateNamedShadowSubscriptionRequest, int, typing.Callable[[UpdateShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `UpdateNamedShadowSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/update/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=UpdateShadowResponse.from_payload)

    def subscribe_to_update_named_shadow_rejected(self, request, qos, callback):
        # type: (UpdateNamedShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        Parameters:
        request - `UpdateNamedShadowSubscriptionRequest` instance.
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
        if not request.shadow_name:
            raise ValueError("request.shadow_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/things/{0.thing_name}/shadow/name/{0.shadow_name}/update/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

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

class DeleteNamedShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['client_token', 'shadow_name', 'thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        return payload

class DeleteNamedShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class DeleteShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        return payload

class DeleteShadowResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')
        for key, val in zip(['timestamp', 'version'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> DeleteShadowResponse
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
        val = payload.get('timestamp')
        if val is not None:
            new.timestamp = datetime.datetime.fromtimestamp(val)
        val = payload.get('version')
        if val is not None:
            new.version = val
        return new

class DeleteShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class ErrorResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'code', 'message', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.code = kwargs.get('code')
        self.message = kwargs.get('message')
        self.timestamp = kwargs.get('timestamp')
        for key, val in zip(['client_token', 'code', 'message', 'timestamp'], args):
            setattr(self, key, val)

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

class GetNamedShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['client_token', 'shadow_name', 'thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        return payload

class GetNamedShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class GetShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.client_token is not None:
            payload['clientToken'] = self.client_token
        return payload

class GetShadowResponse(awsiot.ModeledClass):
    __slots__ = ['client_token', 'metadata', 'state', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')
        for key, val in zip(['metadata', 'state', 'timestamp', 'version'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> GetShadowResponse
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
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

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class NamedShadowDeltaUpdatedSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class NamedShadowUpdatedSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class ShadowDeltaUpdatedEvent(awsiot.ModeledClass):
    __slots__ = ['metadata', 'state', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')
        for key, val in zip(['metadata', 'state', 'timestamp', 'version'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class ShadowMetadata(awsiot.ModeledClass):
    __slots__ = ['desired', 'reported']

    def __init__(self, *args, **kwargs):
        self.desired = kwargs.get('desired')
        self.reported = kwargs.get('reported')
        for key, val in zip(['desired', 'reported'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.desired = kwargs.get('desired')
        self.reported = kwargs.get('reported')
        for key, val in zip(['desired', 'reported'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.delta = kwargs.get('delta')
        self.desired = kwargs.get('desired')
        self.reported = kwargs.get('reported')
        for key, val in zip(['delta', 'desired', 'reported'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.current = kwargs.get('current')
        self.previous = kwargs.get('previous')
        self.timestamp = kwargs.get('timestamp')
        for key, val in zip(['current', 'previous', 'timestamp'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.version = kwargs.get('version')
        for key, val in zip(['metadata', 'state', 'version'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class UpdateNamedShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'shadow_name', 'state', 'thing_name', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.shadow_name = kwargs.get('shadow_name')
        self.state = kwargs.get('state')
        self.thing_name = kwargs.get('thing_name')
        self.version = kwargs.get('version')
        for key, val in zip(['client_token', 'shadow_name', 'state', 'thing_name', 'version'], args):
            setattr(self, key, val)

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

class UpdateNamedShadowSubscriptionRequest(awsiot.ModeledClass):
    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class UpdateShadowRequest(awsiot.ModeledClass):
    __slots__ = ['client_token', 'state', 'thing_name', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.state = kwargs.get('state')
        self.thing_name = kwargs.get('thing_name')
        self.version = kwargs.get('version')
        for key, val in zip(['client_token', 'state', 'thing_name', 'version'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')
        for key, val in zip(['client_token', 'metadata', 'state', 'timestamp', 'version'], args):
            setattr(self, key, val)

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

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

