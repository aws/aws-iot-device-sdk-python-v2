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

__all__ = [
    'iotjobs',
    'iotshadow',
]

from aws_crt import mqtt
from concurrent.futures import Future
import json
from typing import Any, Callable, Dict, Optional, TypeVar

T = TypeVar('T')

PayloadObj = Dict[str, Any]
PayloadToClassFn = Callable[[PayloadObj], T]

class MqttServiceClient(object):
    """
    Base class for an AWS MQTT Service Client
    """

    def __init__(self, mqtt_connection):
        # type: (mqtt.Connection) -> None
        self._mqtt_connection = mqtt_connection # type: mqtt.Connection

    @property
    def mqtt_connection(self):
        return self._mqtt_connection

    def _publish_operation(self, topic, payload):
        # type(str, Optional[PayloadObj]) -> Future
        """
        Performs a 'Publish' style operation for an MQTT service.

        Parameters:
        topic - The topic to publish this message to.
        payload - (Optional) If set, the message will be a string of JSON, built from this object.
                If unset, an empty message is sent.
        """
        future = Future() # type: Future
        try:
            def on_puback(packet_id):
                future.set_result(None)

            if payload is None:
                payload_str = ""
            else:
                payload_str = json.dumps(payload)

            self.mqtt_connection.publish(
                topic=topic,
                payload=payload_str,
                qos=mqtt.QoS.AtLeastOnce,
                puback_callback=on_puback)

        except Exception as e:
            future.set_exception(e)

        return future

    def _subscribe_operation(self, topic, callback, payload_to_class_fn):
        # type: (str, Callable[[T], None], PayloadToClassFn) -> Future
        """
        Performs a 'Subscribe' style operation for an MQTT service.
        Messages received from this topic are processed as JSON,
        converted to the desired class by `payload_to_class_fn`,
        then passed to `callback`.

        Parameters:
        topic - The topic to subscribe to.
        callback - The callback to invoke when a message is received.
                The callback should take one argument of the type
                returned by payload_to_class_fn. The callback
                is not expected to return a value.
        payload_to_class_fn - A function which takes one argument,
                a dict, and returns a class of the type expected by
                `callback`. The dict comes from parsing the received
                message as JSON.

        Returns a Future whose result will be None when the subscription
        is accepted by the server. If the subscription cannot be established,
        the Future's result will be an exception.
        """

        future = Future() # type: Future
        try:
            def on_suback(packet_id, topic, qos):
                future.set_result(None)

            def callback_wrapper(topic, payload_str):
                try:
                    payload_obj = json.loads(payload_str)
                    event = payload_to_class_fn(payload_obj)
                except:
                    # can't deliver payload, invoke callback with None
                    event = None
                callback(event)

            self.mqtt_connection.subscribe(
                topic=topic,
                qos=mqtt.QoS.AtLeastOnce,
                callback=callback_wrapper,
                suback_callback=on_suback)

        except Exception as e:
            future.set_exception(e)

        return future

class ModeledClass(object):
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
