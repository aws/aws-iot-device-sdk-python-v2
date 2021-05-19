# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

__all__ = [
    'MqttServiceClient',
    'ModeledClass',
    'iotjobs',
    'iotshadow',
    'greengrass_discovery',
    'mqtt_connection_builder',
]

from awscrt import mqtt
from concurrent.futures import Future
import json
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar

__version__ = '1.0.0-dev'

T = TypeVar('T')

PayloadObj = Dict[str, Any]
PayloadToClassFn = Callable[[PayloadObj], T]


class MqttServiceClient:
    """
    Base class for an AWS MQTT Service Client

    Args:
        mqtt_connection: MQTT connection to use
    """

    def __init__(self, mqtt_connection: mqtt.Connection):
        self._mqtt_connection = mqtt_connection  # type: mqtt.Connection

    @property
    def mqtt_connection(self) -> mqtt.Connection:
        """
        MQTT connection used by this client
        """
        return self._mqtt_connection

    def unsubscribe(self, topic: str) -> Future:
        """
        Tell the MQTT server to stop sending messages to this topic.

        Args:
            topic: Topic to unsubscribe from

        Returns:
            `Future` whose result will be `None` when the server
            has acknowledged the unsubscribe.
        """
        future = Future()  # type: Future
        try:
            def on_unsuback(unsuback_future):
                if unsuback_future.exception():
                    future.set_exception(unsuback_future.exception())
                else:
                    future.set_result(None)

            unsub_future, _ = self.mqtt_connection.unsubscribe(topic)
            unsub_future.add_done_callback(on_unsuback)

        except Exception as e:
            future.set_exception(e)

        return future

    def _publish_operation(self, topic: str, qos: int, payload: Optional[PayloadObj]) -> Future:
        """
        Performs a 'Publish' style operation for an MQTT service.

        Parameters:
        topic - The topic to publish this message to.
        qos   - The Quality of Service guarantee of this message
        payload - (Optional) If set, the message will be a string of JSON, built from this object.
                If unset, an empty message is sent.

        Returns a `Future` which will contain a result of `None` when the
        server has acknowledged the message, or an exception if the
        publish fails.
        """
        future = Future()  # type: Future
        try:
            def on_puback(puback_future):
                if puback_future.exception():
                    future.set_exception(puback_future.exception())
                else:
                    future.set_result(None)

            if payload is None:
                payload_str = ""
            else:
                payload_str = json.dumps(payload)

            pub_future, _ = self.mqtt_connection.publish(
                topic=topic,
                payload=payload_str,
                qos=qos,
            )
            pub_future.add_done_callback(on_puback)

        except Exception as e:
            future.set_exception(e)

        return future

    def _subscribe_operation(self,
                             topic: str,
                             qos: int,
                             callback: Callable[[T], None],
                             payload_to_class_fn: PayloadToClassFn) -> Tuple[Future, str]:
        """
        Performs a 'Subscribe' style operation for an MQTT service.
        Messages received from this topic are processed as JSON,
        converted to the desired class by `payload_to_class_fn`,
        then passed to `callback`.

        Parameters:
        topic - The topic to subscribe to.
        qos   - The Quality of Service guarantee of this message
        callback - The callback to invoke when a message is received.
                The callback should take one argument of the type
                returned by payload_to_class_fn. The callback
                is not expected to return a value.
        payload_to_class_fn - A function which takes one argument,
                a dict, and returns a class of the type expected by
                `callback`. The dict comes from parsing the received
                message as JSON.

        Returns two values. The first is a `Future` whose result will be the
        `awscrt.mqtt.QoS` granted by the server, or an exception if the
        subscription fails. The second value is a topic which may be passed to
        `unsubscribe()` to stop receiving messages.
        Note that messages may arrive before the subscription is acknowledged.
        """

        future = Future()  # type: Future
        try:
            def on_suback(suback_future):
                try:
                    suback_result = suback_future.result()
                    future.set_result(suback_result['qos'])
                except Exception as e:
                    future.set_exception(e)

            def callback_wrapper(topic, payload, dup, qos, retain, **kwargs):
                try:
                    payload_obj = json.loads(payload.decode())
                    event = payload_to_class_fn(payload_obj)
                except BaseException:
                    # can't deliver payload, invoke callback with None
                    event = None
                callback(event)

            sub_future, _ = self.mqtt_connection.subscribe(
                topic=topic,
                qos=qos,
                callback=callback_wrapper,
            )
            sub_future.add_done_callback(on_suback)

        except Exception as e:
            future.set_exception(e)

        return future, topic


class ModeledClass:
    """
    Base for input/output classes generated from an AWS service model.
    """

    __slots__ = ()

    def __repr__(self):
        properties = []
        for slot in self.__slots__:
            value = getattr(self, slot, None)
            properties.append("{}={}".format(slot, repr(value)))

        return '{}.{}({})'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            ', '.join(properties))
