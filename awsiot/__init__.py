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
from threading import RLock
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import uuid4

class MqttServiceClient(object):
    """
    Base class for an AWS MQTT Service Client
    """

    def __init__(self, mqtt_connection):
        # type: (mqtt.Connection) -> None
        self._mqtt_connection = mqtt_connection # type: mqtt.Connection
        self._nonce_rpc_topics = {} # type: Dict[str, _NonceRpcTopicEntry]
        self._nonce_rpc_lock = RLock() # type: RLock
        self._fifo_rpc_topics = {} # type: Dict[str, _FifoRpcTopicEntry]
        self._fifo_rpc_lock = RLock() # type: RLock

    @property
    def mqtt_connection(self):
        return self._mqtt_connection

    def _nonce_rpc_operation(self, request_topic, request_payload, nonce_value, subscriptions):
        # type: (str, PayloadObj, Optional[str], List[_NonceRpcSubscription]) -> Future
        """
        Performs a "Remote Procedure Call" style operation for an MQTT service,
        where a "nonce" token is used to correlate requests with responses.

        Parameters:
        request_topic - Topic for request message.
        request_payload - Input object to be sent as json string in request message.
        nonce_value - Unique token string used to correlate the response with this particular request.
                      If none is provided, a uniqe value will be generated for this operation.
        subscriptions - List of _NonceRpcSubscriptions, one for each possible response.

        Returns a Future that will contain the outcome of the operation.
        A response from a non-error topic becomes a valid result in the Future.
        A response from an error topic becomes an Exception in the Future.
        Any other exception that occurs as part of the RPC becomes an exception in the Future.
        """

        future = Future() # type: Future
        if not nonce_value:
            nonce_value = str(uuid4())

        operation = _NonceRpcOperation(future, request_topic, json.dumps(request_payload), nonce_value, subscriptions)

        # callback sends request when all subacks received
        suback_counter = [] # type: List
        def on_suback(packet_id):
            # count subacks by popping an entry out of this list
            if suback_counter:
                suback_counter.pop()
                if not suback_counter:
                    # all subscriptions succeeded
                    self.mqtt_connection.publish(operation.request_topic, operation.request_payload, 1)

        with self._nonce_rpc_lock:
            topics_to_subscribe_to = []
            for sub in operation.subscriptions:
                topic_entry = self._nonce_rpc_topics.get(sub.topic)
                if not topic_entry:
                    topics_to_subscribe_to.append(sub.topic)
                    topic_entry = _NonceRpcTopicEntry(sub.payload_nonce_field)
                    self._nonce_rpc_topics[sub.topic] = topic_entry

                topic_entry.outstanding_operations[operation.nonce_value] = operation

            if topics_to_subscribe_to:
                suback_counter.extend(['suback'] * len(topics_to_subscribe_to))
                for i in topics_to_subscribe_to:
                    self.mqtt_connection.subscribe(i, 1, self._nonce_response_callback, on_suback)
        # lock released

        # if we're not waiting on any subscribes to complete, publish the request immediately
        if not topics_to_subscribe_to:
            self.mqtt_connection.publish(operation.request_topic, operation.request_payload, 1)

        return future

    def _nonce_response_callback(self, topic, payload_str):
        # type: (str, str) -> None
        payload_obj = json.loads(payload_str)
        operation = None
        subscription = None
        try:
            with self._nonce_rpc_lock:
                # find the corresponding operation
                topic_entry = self._nonce_rpc_topics[topic]
                nonce_value = payload_obj[topic_entry.nonce_field_name_in_response]
                operation = topic_entry.outstanding_operations[nonce_value]

                # operation found.
                # remove it from all associated topics.
                # unsubscribe from any topic that has no more outstanding operations.
                topics_to_unsubscribe_from = [] # type: List

                for sub in operation.subscriptions:
                    if sub.topic == topic:
                        subscription = sub
                    topic_entry = self._nonce_rpc_topics[sub.topic]
                    del topic_entry.outstanding_operations[nonce_value]
                    if not topic_entry.outstanding_operations:
                        del self._nonce_rpc_topics[sub.topic]
                        topics_to_unsubscribe_from.append(sub.topic)

                for i in topics_to_unsubscribe_from:
                    self.mqtt_connection.unsubscribe(i)

            # lock released
            if subscription and operation:
                result = subscription.class_from_payload_fn(payload_obj)
                if isinstance(result, Exception):
                    operation.future.set_exception(result)
                else:
                    operation.future.set_result(result)
            else:
                raise RuntimeError("Cannot determine response type")

        except Exception as e:
            if operation:
                operation.future.set_exception(e)
            else:
                raise

    def _fifo_rpc_operation(self, request_topic, request_payload, subscriptions):
        # type: (str, Optional[PayloadObj], List[_FifoRpcSubscription]) -> Future
        """
        Performs a "Remote Procedure Call" style operation for an MQTT service,
        where responses are correlated to requests on a first-in-first-out basis.

        Parameters:
        request_topic - Topic for request message.
        request_payload - Input object to be sent as json string in request message.
        subscriptions - List of _FifoRpcSubscriptions, one for each possible response.

        Returns a Future that will contain the outcome of the operation.
        A response from a non-error topic becomes a valid result in the Future.
        A response from an error topic becomes an Exception in the Future.
        Any other exception that occurs as part of the RPC becomes an exception in the Future.
        """
        future = Future() # type: Future
        request_payload_str = json.dumps(request_payload) if request_payload else ""
        operation = _FifoRpcOperation(future, request_topic, request_payload_str, subscriptions)

        # callback sends request when all subacks received
        suback_counter = [] # type: List
        def on_suback(packet_id):
            # count subacks by popping an entry out of this list
            if suback_counter:
                suback_counter.pop()
                if not suback_counter:
                    # all subscriptions succeeded
                    self.mqtt_connection.publish(operation.request_topic, operation.request_payload, 1)

        with self._fifo_rpc_lock:
            topics_to_subscribe_to = []
            for sub in operation.subscriptions:
                topic_entry = self._fifo_rpc_topics.get(sub.topic)
                if not topic_entry:
                    topics_to_subscribe_to.append(sub.topic)
                    topic_entry = _FifoRpcTopicEntry()
                    self._fifo_rpc_topics[sub.topic] = topic_entry

                topic_entry.outstanding_operations.append(operation)

            if topics_to_subscribe_to:
                suback_counter.extend(['suback'] * len(topics_to_subscribe_to))
                for i in topics_to_subscribe_to:
                    self.mqtt_connection.subscribe(i, 1, self._fifo_callback, on_suback)
        # lock released.

        # if we're not waiting on any subscribes to complete, publish the request immediately
        if not topics_to_subscribe_to:
            self.mqtt_connection.publish(operation.request_topic, operation.request_payload, 1)

        return future

    def _fifo_callback(self, topic, payload_str):
        # type: (str, str) -> None
        operation = None
        subscription = None
        try:
            with self._fifo_rpc_lock:
                # find the corresponding operation
                topic_entry = self._fifo_rpc_topics[topic]
                operation = topic_entry.outstanding_operations[0]

                # operation found.
                # remove it from all associated topics.
                # unsubscribe from any topic that has no more outstanding operations.
                topics_to_unsubscribe_from = []

                for sub in operation.subscriptions:
                    if sub.topic == topic:
                        subscription = sub
                    topic_entry = self._fifo_rpc_topics[sub.topic]
                    topic_entry.outstanding_operations.remove(operation)
                    if not topic_entry.outstanding_operations:
                        del self._fifo_rpc_topics[sub.topic]
                        topics_to_unsubscribe_from.append(sub.topic)

                for i in topics_to_unsubscribe_from:
                    self.mqtt_connection.unsubscribe(i)
            # lock released

            # sometimes the response is an empty string
            try:
                payload_obj = json.loads(payload_str)
            except:
                payload_obj = {}

            if subscription and operation:
                result = subscription.class_from_payload_fn(payload_obj)
                if isinstance(result, Exception):
                    operation.future.set_exception(result)
                else:
                    operation.future.set_result(result)
            else:
                raise RuntimeError("Cannot determine response type")

        except Exception as e:
            if operation:
                operation.future.set_exception(e)
            else:
                raise

    def _subscribe_operation(self, subscriptions):
        # type: (List[_SubscriptionInfo]) -> Future
        """
        Performs a 'Subscribe' style operation for an MQTT service.

        Parameters:
        subscriptions - List of _SubscriptionInfos, one for each possible response.

        Returns a Future that will contain None when all subscriptions have been acknowledged by the server.
        """

        future = Future() # type: Future

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


T = TypeVar('T')

PayloadObj = Dict[str, Any]
ClassFromPayloadFn = Callable[[PayloadObj], T]

class _NonceRpcSubscription(object):
    # type: Generic[T]
    def __init__(self, topic, class_from_payload_fn, payload_nonce_field):
        # type: (str, ClassFromPayloadFn, str) -> None
        self.topic = topic # type: str
        self.class_from_payload_fn = class_from_payload_fn # type: ClassFromPayloadFn
        self.payload_nonce_field = payload_nonce_field # type: str

class _NonceRpcOperation(object):
    def __init__(self, future, request_topic, request_payload, nonce_value, subscriptions):
        # type: (Future, str, str, str, List[_NonceRpcSubscription]) -> None
        self.future = future # type: Future
        self.request_topic = request_topic # type: str
        self.request_payload = request_payload # type: str
        self.nonce_value = nonce_value # type: str
        self.subscriptions = subscriptions # type: List[_NonceRpcSubscription]

class _FifoRpcSubscription(object):
    # type: Generic[T]
    def __init__(self, topic, class_from_payload_fn):
        # type: (str, ClassFromPayloadFn) -> None
        self.topic = topic # type: str
        self.class_from_payload_fn = class_from_payload_fn # type: ClassFromPayloadFn

class _FifoRpcOperation(object):
    def __init__(self, future, request_topic, request_payload, subscriptions):
        # type: (Future, str, str, List[_FifoRpcSubscription]) -> None
        self.future = future # type: Future
        self.request_topic = request_topic # type: str
        self.request_payload = request_payload # type: str
        self.subscriptions = subscriptions # type: List[_FifoRpcSubscription]

class _NonceRpcTopicEntry(object):
    def __init__(self, nonce_field_name_in_response):
        # type: (str) -> None
        self.nonce_field_name_in_response = nonce_field_name_in_response # type: str
        self.outstanding_operations = {} # type: Dict[str, _NonceRpcOperation]

class _FifoRpcTopicEntry(object):
    def __init__(self):
        # type() -> None
        self.outstanding_operations = [] # type: List[_FifoRpcOperation]

class _SubscriptionInfo(object):
    # type: Generic[T]
    def __init__(self, topic, callback, payload_class):
        # type: (str, Callable[[T], None], Type[T]) -> None
        self.topic = topic # type: str
        self.callback = callback # type: Callable[[T], None]
        self.payload_class = payload_class # Type[T]
