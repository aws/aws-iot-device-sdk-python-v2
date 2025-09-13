# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

__all__ = [
    'MqttServiceClient',
    'ModeledClass',
    'iotjobs',
    'iotshadow',
    'greengrass_discovery',
    'mqtt_connection_builder',
    'mqtt5_client_builder',
    'V2ServiceException',
    'V2DeserializationFailure',
    'ServiceStreamOptions'
]

import awscrt
from awscrt import mqtt, mqtt5, mqtt_request_response
from concurrent.futures import Future
from dataclasses import dataclass
import json
from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, Union

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

    def __init__(self, mqtt_connection: Union[mqtt.Connection, mqtt5.Client]):
        if isinstance(mqtt_connection, mqtt.Connection):
            self._mqtt_connection = mqtt_connection  # type: mqtt.Connection
        elif isinstance(mqtt_connection, mqtt5.Client):
            self._mqtt_connection = mqtt_connection.new_connection()
            self._mqtt5_client = mqtt_connection
        else:
            raise TypeError("The service client could only take mqtt.Connection and mqtt5.Client as argument")

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


class V2ServiceException(Exception):
    """
    Wrapper exception thrown by V2 service clients to indicate the failure of an operation

    Args:
        message (str): Description of the failure.
        inner_error (Optional[Exception]): Cause of the failure.
        modeled_error (Optional[Any]): Modeled error shape that contains additional information about the failure.
            The modeled type is specific to each individual service operation.
    """
    def __init__(self, message: str, inner_error: 'Optional[Exception]', modeled_error: 'Optional[Any]'):
        self.message = message
        self.inner_error = inner_error
        self.modeled_error = modeled_error

def create_v2_service_modeled_future(internal_unmodeled_future : Future, operation_name : str, accepted_topic : str, response_class, modeled_error_class):
    modeled_future = Future()

    # force a strong ref to the hidden/internal unmodeled future so that it can't be GCed prior to completion
    modeled_future.unmodeled_future = internal_unmodeled_future

    def complete_modeled_future(unmodeled_future):
        if unmodeled_future.exception():
            service_error = V2ServiceException(f"{operation_name} failure", unmodeled_future.exception(), None)
            modeled_future.set_exception(service_error)
        else:
            unmodeled_result = unmodeled_future.result()
            try:
                payload_as_json = json.loads(unmodeled_result.payload.decode())
                if unmodeled_result.topic == accepted_topic:
                    modeled_future.set_result(response_class.from_payload(payload_as_json))
                else:
                    modeled_error = modeled_error_class.from_payload(payload_as_json)
                    modeled_future.set_exception(V2ServiceException(f"{operation_name} failure", None, modeled_error))
            except Exception as e:
                modeled_future.set_exception(V2ServiceException(f"{operation_name} failure", e, None))

    internal_unmodeled_future.add_done_callback(lambda f: complete_modeled_future(f))

    return modeled_future

class V2DeserializationFailure(Exception):
    """
    An exception raised when deserialization from an MQTT message payload to a modeled type fails

    Args:
        message (str): description of the failure
        inner_error (Optional[Exception]): the underlying deserialization exception
        payload (Optional[bytes]): original MQTT message payload that could not be deserialized properly
    """
    def __init__(self, message: str, inner_error: 'Optional[Exception]', payload: Optional[bytes]):
        self.message = message
        self.inner_error = inner_error
        self.payload = payload


@dataclass
class ServiceStreamOptions(Generic[T]):
    """
    Configuration options for an MQTT-based service streaming operation.

    Args:
        incoming_event_listener (Callable[[T], None]): function object to invoke when a stream message is successfully deserialized
        subscription_status_listener (Optional[Callable[[awscrt.mqtt_request_response.SubscriptionStatusEvent], None]]): function object to invoke when the operation's subscription status changes
        deserialization_failure_listener (Optional[Callable[[V2DeserializationFailure], None]]): function object to invoke when a publish is received on the streaming subscription that cannot be deserialized into the stream's output type.  Should never happen.
    """
    incoming_event_listener: 'Callable[[T], None]'
    subscription_status_listener: 'Optional[Callable[[awscrt.mqtt_request_response.SubscriptionStatusEvent], None]]' = None
    deserialization_failure_listener: 'Optional[Callable[[V2DeserializationFailure], None]]' = None

    def _validate(self):
        """
        Stringently type-checks an instance's field values.
        """
        assert callable(self.incoming_event_listener)
        assert callable(self.subscription_status_listener) or self.subscription_status_listener is None
        assert callable(self.deserialization_failure_listener) or self.deserialization_failure_listener is None


def create_streaming_unmodeled_options(stream_options: ServiceStreamOptions[T], subscription_topic: str, event_name: str, event_class):
    def modeled_event_callback(unmodeled_event : mqtt_request_response.IncomingPublishEvent):
        try:
            payload_as_json = json.loads(unmodeled_event.payload.decode())
            modeled_event = event_class.from_payload(payload_as_json)
            stream_options.incoming_event_listener(modeled_event)
        except Exception as e:
            if stream_options.deserialization_failure_listener is not None:
                failure_event = V2DeserializationFailure(f"{event_name} stream deserialization failure", e, unmodeled_event.payload)
                stream_options.deserialization_failure_listener(failure_event)

    return mqtt_request_response.StreamingOperationOptions(subscription_topic, stream_options.subscription_status_listener, modeled_event_callback)
