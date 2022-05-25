# Copyright Amazon.com, Inc. or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot
import concurrent.futures
import datetime
import typing

class IotShadowClient(awsiot.MqttServiceClient):
    """

    The AWS IoT Device Shadow service adds shadows to AWS IoT thing objects. Shadows are a simple data store for device properties and state.  Shadows can make a device’s state available to apps and other services whether the device is connected to AWS IoT or not.

    AWS Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html

    """

    def publish_delete_named_shadow(self, request, qos):
        # type: (DeleteNamedShadowRequest, int) -> concurrent.futures.Future
        """

        Deletes a named shadow for an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-pub-sub-topic

        Args:
            request: `DeleteNamedShadowRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Deletes the (classic) shadow for an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-pub-sub-topic

        Args:
            request: `DeleteShadowRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Gets a named shadow for an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-pub-sub-topic

        Args:
            request: `GetNamedShadowRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Gets the (classic) shadow for an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-pub-sub-topic

        Args:
            request: `GetShadowRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Update a named shadow for a device.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-pub-sub-topic

        Args:
            request: `UpdateNamedShadowRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Update a device's (classic) shadow.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-pub-sub-topic

        Args:
            request: `UpdateShadowRequest` instance.
            qos: The Quality of Service guarantee of this message

        Returns:
            A Future whose result will be None if the
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

        Subscribes to the accepted topic for the DeleteNamedShadow operation.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-accepted-pub-sub-topic

        Args:
            request: `DeleteNamedShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `DeleteShadowResponse`.
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

        Subscribes to the rejected topic for the DeleteNamedShadow operation.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-rejected-pub-sub-topic

        Args:
            request: `DeleteNamedShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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

        Subscribes to the accepted topic for the DeleteShadow operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-accepted-pub-sub-topic

        Args:
            request: `DeleteShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `DeleteShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/delete/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=DeleteShadowResponse.from_payload)

    def subscribe_to_delete_shadow_rejected(self, request, qos, callback):
        # type: (DeleteShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribes to the rejected topic for the DeleteShadow operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#delete-rejected-pub-sub-topic

        Args:
            request: `DeleteShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/delete/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_get_named_shadow_accepted(self, request, qos, callback):
        # type: (GetNamedShadowSubscriptionRequest, int, typing.Callable[[GetShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribes to the accepted topic for the GetNamedShadow operation.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-accepted-pub-sub-topic

        Args:
            request: `GetNamedShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `GetShadowResponse`.
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

        Subscribes to the rejected topic for the GetNamedShadow operation.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-rejected-pub-sub-topic

        Args:
            request: `GetNamedShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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

        Subscribes to the accepted topic for the GetShadow operation.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-accepted-pub-sub-topic

        Args:
            request: `GetShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `GetShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/get/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=GetShadowResponse.from_payload)

    def subscribe_to_get_shadow_rejected(self, request, qos, callback):
        # type: (GetShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribes to the rejected topic for the GetShadow operation.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#get-rejected-pub-sub-topic

        Args:
            request: `GetShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/get/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_named_shadow_delta_updated_events(self, request, qos, callback):
        # type: (NamedShadowDeltaUpdatedSubscriptionRequest, int, typing.Callable[[ShadowDeltaUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribe to NamedShadowDelta events for a named shadow of an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-delta-pub-sub-topic

        Args:
            request: `NamedShadowDeltaUpdatedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ShadowDeltaUpdatedEvent`.
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

        Subscribe to ShadowUpdated events for a named shadow of an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-documents-pub-sub-topic

        Args:
            request: `NamedShadowUpdatedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ShadowUpdatedEvent`.
                The callback is not expected to return anything.

        Returns:
            Tuple with two values. The first is a `Future` whose result will be the
            `awscrt.mqtt.QoS` granted by the server, or an exception if the
            subscription fails. The second value is a topic which may be passed
            to `unsubscribe()` to stop receiving messages. Note that messages
            may arrive before the subscription is acknowledged.
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

        Subscribe to ShadowDelta events for the (classic) shadow of an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-delta-pub-sub-topic

        Args:
            request: `ShadowDeltaUpdatedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ShadowDeltaUpdatedEvent`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/delta'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ShadowDeltaUpdatedEvent.from_payload)

    def subscribe_to_shadow_updated_events(self, request, qos, callback):
        # type: (ShadowUpdatedSubscriptionRequest, int, typing.Callable[[ShadowUpdatedEvent], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribe to ShadowUpdated events for the (classic) shadow of an AWS IoT thing.

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-documents-pub-sub-topic

        Args:
            request: `ShadowUpdatedSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ShadowUpdatedEvent`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/documents'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ShadowUpdatedEvent.from_payload)

    def subscribe_to_update_named_shadow_accepted(self, request, qos, callback):
        # type: (UpdateNamedShadowSubscriptionRequest, int, typing.Callable[[UpdateShadowResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribes to the accepted topic for the UpdateNamedShadow operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-accepted-pub-sub-topic

        Args:
            request: `UpdateNamedShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `UpdateShadowResponse`.
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

        Subscribes to the rejected topic for the UpdateNamedShadow operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-rejected-pub-sub-topic

        Args:
            request: `UpdateNamedShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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

        Subscribes to the accepted topic for the UpdateShadow operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-accepted-pub-sub-topic

        Args:
            request: `UpdateShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `UpdateShadowResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=UpdateShadowResponse.from_payload)

    def subscribe_to_update_shadow_rejected(self, request, qos, callback):
        # type: (UpdateShadowSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """

        Subscribes to the rejected topic for the UpdateShadow operation

        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/device-shadow-mqtt.html#update-rejected-pub-sub-topic

        Args:
            request: `UpdateShadowSubscriptionRequest` instance.
            qos: The Quality of Service guarantee of this message
            callback: Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
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
            topic='$aws/things/{0.thing_name}/shadow/update/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

class DeleteNamedShadowRequest(awsiot.ModeledClass):
    """

    Data needed to make a DeleteNamedShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        shadow_name (str): Name of the shadow to delete.
        thing_name (str): AWS IoT thing to delete a named shadow from.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        shadow_name (str): Name of the shadow to delete.
        thing_name (str): AWS IoT thing to delete a named shadow from.
    """

    __slots__ = ['client_token', 'shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'shadow_name', 'thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]

        if self.client_token is not None:
            payload['clientToken'] = self.client_token

        return payload

class DeleteNamedShadowSubscriptionRequest(awsiot.ModeledClass):
    """

    Data needed to subscribe to DeleteNamedShadow responses for an AWS IoT thing.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        shadow_name (str): Name of the shadow to subscribe to DeleteNamedShadow operations for.
        thing_name (str): AWS IoT thing to subscribe to DeleteNamedShadow operations for.

    Attributes:
        shadow_name (str): Name of the shadow to subscribe to DeleteNamedShadow operations for.
        thing_name (str): AWS IoT thing to subscribe to DeleteNamedShadow operations for.
    """

    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class DeleteShadowRequest(awsiot.ModeledClass):
    """

    Data needed to make a DeleteShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        thing_name (str): AWS IoT thing to delete the (classic) shadow of.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        thing_name (str): AWS IoT thing to delete the (classic) shadow of.
    """

    __slots__ = ['client_token', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]

        if self.client_token is not None:
            payload['clientToken'] = self.client_token

        return payload

class DeleteShadowResponse(awsiot.ModeledClass):
    """

    Response payload to a DeleteShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): A client token used to correlate requests and responses.
        timestamp (datetime.datetime): The time the response was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow.

    Attributes:
        client_token (str): A client token used to correlate requests and responses.
        timestamp (datetime.datetime): The time the response was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow.
    """

    __slots__ = ['client_token', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Data needed to subscribe to DeleteShadow responses for an AWS IoT thing.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): AWS IoT thing to subscribe to DeleteShadow operations for.

    Attributes:
        thing_name (str): AWS IoT thing to subscribe to DeleteShadow operations for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class ErrorResponse(awsiot.ModeledClass):
    """

    Response document containing details about a failed request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Opaque request-response correlation data.  Present only if a client token was used in the request.
        code (int): An HTTP response code that indicates the type of error.
        message (str): A text message that provides additional information.
        timestamp (datetime.datetime): The date and time the response was generated by AWS IoT. This property is not present in all error response documents.

    Attributes:
        client_token (str): Opaque request-response correlation data.  Present only if a client token was used in the request.
        code (int): An HTTP response code that indicates the type of error.
        message (str): A text message that provides additional information.
        timestamp (datetime.datetime): The date and time the response was generated by AWS IoT. This property is not present in all error response documents.
    """

    __slots__ = ['client_token', 'code', 'message', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.code = kwargs.get('code')
        self.message = kwargs.get('message')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Data needed to make a GetNamedShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        shadow_name (str): Name of the shadow to get.
        thing_name (str): AWS IoT thing to get the named shadow for.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        shadow_name (str): Name of the shadow to get.
        thing_name (str): AWS IoT thing to get the named shadow for.
    """

    __slots__ = ['client_token', 'shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['client_token', 'shadow_name', 'thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]

        if self.client_token is not None:
            payload['clientToken'] = self.client_token

        return payload

class GetNamedShadowSubscriptionRequest(awsiot.ModeledClass):
    """

    Data needed to subscribe to GetNamedShadow responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        shadow_name (str): Name of the shadow to subscribe to GetNamedShadow responses for.
        thing_name (str): AWS IoT thing subscribe to GetNamedShadow responses for.

    Attributes:
        shadow_name (str): Name of the shadow to subscribe to GetNamedShadow responses for.
        thing_name (str): AWS IoT thing subscribe to GetNamedShadow responses for.
    """

    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class GetShadowRequest(awsiot.ModeledClass):
    """

    Data needed to make a GetShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        thing_name (str): AWS IoT thing to get the (classic) shadow for.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        thing_name (str): AWS IoT thing to get the (classic) shadow for.
    """

    __slots__ = ['client_token', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]

        if self.client_token is not None:
            payload['clientToken'] = self.client_token

        return payload

class GetShadowResponse(awsiot.ModeledClass):
    """

    Response payload to a GetShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): An opaque token used to correlate requests and responses.
        metadata (ShadowMetadata): Contains the timestamps for each attribute in the desired and reported sections of the state.
        state (ShadowStateWithDelta): The (classic) shadow state of the AWS IoT thing.
        timestamp (datetime.datetime): The time the response was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow shared in AWS IoT. It is increased by one over the previous version of the document.

    Attributes:
        client_token (str): An opaque token used to correlate requests and responses.
        metadata (ShadowMetadata): Contains the timestamps for each attribute in the desired and reported sections of the state.
        state (ShadowStateWithDelta): The (classic) shadow state of the AWS IoT thing.
        timestamp (datetime.datetime): The time the response was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow shared in AWS IoT. It is increased by one over the previous version of the document.
    """

    __slots__ = ['client_token', 'metadata', 'state', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Data needed to subscribe to GetShadow responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): AWS IoT thing subscribe to GetShadow responses for.

    Attributes:
        thing_name (str): AWS IoT thing subscribe to GetShadow responses for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class NamedShadowDeltaUpdatedSubscriptionRequest(awsiot.ModeledClass):
    """

    Data needed to subscribe to a device's NamedShadowDelta events.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        shadow_name (str): Name of the shadow to get ShadowDelta events for.
        thing_name (str): Name of the AWS IoT thing to get NamedShadowDelta events for.

    Attributes:
        shadow_name (str): Name of the shadow to get ShadowDelta events for.
        thing_name (str): Name of the AWS IoT thing to get NamedShadowDelta events for.
    """

    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class NamedShadowUpdatedSubscriptionRequest(awsiot.ModeledClass):
    """

    Data needed to subscribe to a device's NamedShadowUpdated events.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        shadow_name (str): Name of the shadow to get NamedShadowUpdated events for.
        thing_name (str): Name of the AWS IoT thing to get NamedShadowUpdated events for.

    Attributes:
        shadow_name (str): Name of the shadow to get NamedShadowUpdated events for.
        thing_name (str): Name of the AWS IoT thing to get NamedShadowUpdated events for.
    """

    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class ShadowDeltaUpdatedEvent(awsiot.ModeledClass):
    """

    An event generated when a shadow document was updated by a request to AWS IoT.  The event payload contains only the changes requested.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): An opaque token used to correlate requests and responses.  Present only if a client token was used in the request.
        metadata (typing.Dict[str, typing.Any]): Timestamps for the shadow properties that were updated.
        state (typing.Dict[str, typing.Any]): Shadow properties that were updated.
        timestamp (datetime.datetime): The time the event was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow.

    Attributes:
        client_token (str): An opaque token used to correlate requests and responses.  Present only if a client token was used in the request.
        metadata (typing.Dict[str, typing.Any]): Timestamps for the shadow properties that were updated.
        state (typing.Dict[str, typing.Any]): Shadow properties that were updated.
        timestamp (datetime.datetime): The time the event was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow.
    """

    __slots__ = ['client_token', 'metadata', 'state', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['metadata', 'state', 'timestamp', 'version'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowDeltaUpdatedEvent
        new = cls()
        val = payload.get('clientToken')
        if val is not None:
            new.client_token = val
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
    """

    Data needed to subscribe to a device's ShadowDelta events.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the AWS IoT thing to get ShadowDelta events for.

    Attributes:
        thing_name (str): Name of the AWS IoT thing to get ShadowDelta events for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class ShadowMetadata(awsiot.ModeledClass):
    """

    Contains the last-updated timestamps for each attribute in the desired and reported sections of the shadow state.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        desired (typing.Dict[str, typing.Any]): Contains the timestamps for each attribute in the desired section of a shadow's state.
        reported (typing.Dict[str, typing.Any]): Contains the timestamps for each attribute in the reported section of a shadow's state.

    Attributes:
        desired (typing.Dict[str, typing.Any]): Contains the timestamps for each attribute in the desired section of a shadow's state.
        reported (typing.Dict[str, typing.Any]): Contains the timestamps for each attribute in the reported section of a shadow's state.
    """

    __slots__ = ['desired', 'reported']

    def __init__(self, *args, **kwargs):
        self.desired = kwargs.get('desired')
        self.reported = kwargs.get('reported')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    (Potentially partial) state of an AWS IoT thing's shadow.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        desired (typing.Dict[str, typing.Any]): The desired shadow state (from external services and devices).
        reported (typing.Dict[str, typing.Any]): The (last) reported shadow state from the device.

    Attributes:
        desired (typing.Dict[str, typing.Any]): The desired shadow state (from external services and devices).
        desired_is_nullable (bool): Set to true to allow 'desired' to be None, clearing the data if sent.

        reported (typing.Dict[str, typing.Any]): The (last) reported shadow state from the device.
        reported_is_nullable (bool): Set to true to allow 'reported' to be None, clearing the data if sent.

    """

    __slots__ = ['desired', 'desired_is_nullable', 'reported', 'reported_is_nullable']

    def __init__(self, *args, **kwargs):
        self.desired = kwargs.get('desired')
        self.reported = kwargs.get('reported')

        self.desired_is_nullable = kwargs.get('desired_is_nullable', False)
        self.reported_is_nullable = kwargs.get('reported_is_nullable', False)

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['desired', 'reported'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ShadowState
        new = cls()
        if 'desired' in payload:
            new.desired = payload['desired']
            new.desired_is_nullable = new.desired is None

        if 'reported' in payload:
            new.reported = payload['reported']
            new.reported_is_nullable = new.reported is None

        return new

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]

        if self.desired_is_nullable is True:
            payload['desired'] = self.desired
        else:
            if self.desired is not None:
                payload['desired'] = self.desired

        if self.reported_is_nullable is True:
            payload['reported'] = self.reported
        else:
            if self.reported is not None:
                payload['reported'] = self.reported

        return payload

class ShadowStateWithDelta(awsiot.ModeledClass):
    """

    (Potentially partial) state of an AWS IoT thing's shadow.  Includes the delta between the reported and desired states.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        delta (typing.Dict[str, typing.Any]): The delta between the reported and desired states.
        desired (typing.Dict[str, typing.Any]): The desired shadow state (from external services and devices).
        reported (typing.Dict[str, typing.Any]): The (last) reported shadow state from the device.

    Attributes:
        delta (typing.Dict[str, typing.Any]): The delta between the reported and desired states.
        desired (typing.Dict[str, typing.Any]): The desired shadow state (from external services and devices).
        reported (typing.Dict[str, typing.Any]): The (last) reported shadow state from the device.
    """

    __slots__ = ['delta', 'desired', 'reported']

    def __init__(self, *args, **kwargs):
        self.delta = kwargs.get('delta')
        self.desired = kwargs.get('desired')
        self.reported = kwargs.get('reported')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    A description of the before and after states of a device shadow.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        current (ShadowUpdatedSnapshot): Contains the state of the object after the update.
        previous (ShadowUpdatedSnapshot): Contains the state of the object before the update.
        timestamp (datetime.datetime): The time the event was generated by AWS IoT.

    Attributes:
        current (ShadowUpdatedSnapshot): Contains the state of the object after the update.
        previous (ShadowUpdatedSnapshot): Contains the state of the object before the update.
        timestamp (datetime.datetime): The time the event was generated by AWS IoT.
    """

    __slots__ = ['current', 'previous', 'timestamp']

    def __init__(self, *args, **kwargs):
        self.current = kwargs.get('current')
        self.previous = kwargs.get('previous')
        self.timestamp = kwargs.get('timestamp')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Complete state of the (classic) shadow of an AWS IoT Thing.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        metadata (ShadowMetadata): Contains the timestamps for each attribute in the desired and reported sections of the state.
        state (ShadowState): Current shadow state.
        version (int): The current version of the document for the device's shadow.

    Attributes:
        metadata (ShadowMetadata): Contains the timestamps for each attribute in the desired and reported sections of the state.
        state (ShadowState): Current shadow state.
        version (int): The current version of the document for the device's shadow.
    """

    __slots__ = ['metadata', 'state', 'version']

    def __init__(self, *args, **kwargs):
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Data needed to subscribe to a device's ShadowUpdated events.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the AWS IoT thing to get ShadowUpdated events for.

    Attributes:
        thing_name (str): Name of the AWS IoT thing to get ShadowUpdated events for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)

class UpdateNamedShadowRequest(awsiot.ModeledClass):
    """

    Data needed to make an UpdateNamedShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        shadow_name (str): Name of the shadow to update.
        state (ShadowState): Requested changes to shadow state.  Updates affect only the fields specified.
        thing_name (str): Aws IoT thing to update a named shadow of.
        version (int): (Optional) The Device Shadow service applies the update only if the specified version matches the latest version.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        shadow_name (str): Name of the shadow to update.
        state (ShadowState): Requested changes to shadow state.  Updates affect only the fields specified.
        thing_name (str): Aws IoT thing to update a named shadow of.
        version (int): (Optional) The Device Shadow service applies the update only if the specified version matches the latest version.
    """

    __slots__ = ['client_token', 'shadow_name', 'state', 'thing_name', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.shadow_name = kwargs.get('shadow_name')
        self.state = kwargs.get('state')
        self.thing_name = kwargs.get('thing_name')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Data needed to subscribe to UpdateNamedShadow responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        shadow_name (str): Name of the shadow to listen to UpdateNamedShadow responses for.
        thing_name (str): Name of the AWS IoT thing to listen to UpdateNamedShadow responses for.

    Attributes:
        shadow_name (str): Name of the shadow to listen to UpdateNamedShadow responses for.
        thing_name (str): Name of the AWS IoT thing to listen to UpdateNamedShadow responses for.
    """

    __slots__ = ['shadow_name', 'thing_name']

    def __init__(self, *args, **kwargs):
        self.shadow_name = kwargs.get('shadow_name')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['shadow_name', 'thing_name'], args):
            setattr(self, key, val)

class UpdateShadowRequest(awsiot.ModeledClass):
    """

    Data needed to make an UpdateShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        state (ShadowState): Requested changes to the shadow state.  Updates affect only the fields specified.
        thing_name (str): Aws IoT thing to update the (classic) shadow of.
        version (int): (Optional) The Device Shadow service processes the update only if the specified version matches the latest version.

    Attributes:
        client_token (str): Optional. A client token used to correlate requests and responses. Enter an arbitrary value here and it is reflected in the response.
        state (ShadowState): Requested changes to the shadow state.  Updates affect only the fields specified.
        thing_name (str): Aws IoT thing to update the (classic) shadow of.
        version (int): (Optional) The Device Shadow service processes the update only if the specified version matches the latest version.
    """

    __slots__ = ['client_token', 'state', 'thing_name', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.state = kwargs.get('state')
        self.thing_name = kwargs.get('thing_name')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Response payload to an UpdateShadow request.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_token (str): An opaque token used to correlate requests and responses.  Present only if a client token was used in the request.
        metadata (ShadowMetadata): Contains the timestamps for each attribute in the desired and reported sections so that you can determine when the state was updated.
        state (ShadowState): Updated device shadow state.
        timestamp (datetime.datetime): The time the response was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow shared in AWS IoT. It is increased by one over the previous version of the document.

    Attributes:
        client_token (str): An opaque token used to correlate requests and responses.  Present only if a client token was used in the request.
        metadata (ShadowMetadata): Contains the timestamps for each attribute in the desired and reported sections so that you can determine when the state was updated.
        state (ShadowState): Updated device shadow state.
        timestamp (datetime.datetime): The time the response was generated by AWS IoT.
        version (int): The current version of the document for the device's shadow shared in AWS IoT. It is increased by one over the previous version of the document.
    """

    __slots__ = ['client_token', 'metadata', 'state', 'timestamp', 'version']

    def __init__(self, *args, **kwargs):
        self.client_token = kwargs.get('client_token')
        self.metadata = kwargs.get('metadata')
        self.state = kwargs.get('state')
        self.timestamp = kwargs.get('timestamp')
        self.version = kwargs.get('version')

        # for backwards compatibility, read any arguments that used to be accepted by position
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
    """

    Data needed to subscribe to UpdateShadow responses.

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name (str): Name of the AWS IoT thing to listen to UpdateShadow responses for.

    Attributes:
        thing_name (str): Name of the AWS IoT thing to listen to UpdateShadow responses for.
    """

    __slots__ = ['thing_name']

    def __init__(self, *args, **kwargs):
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['thing_name'], args):
            setattr(self, key, val)
