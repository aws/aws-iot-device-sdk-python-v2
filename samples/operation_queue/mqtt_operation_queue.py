# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from threading import Thread, Lock
from enum import Enum
from time import sleep
from types import FunctionType

from awscrt import mqtt

#######################################################
# Enums
########################################################

class QueueResult(Enum):
    SUCCESS=0
    ERROR_QUEUE_FULL=1
    ERROR_INVALID_ARGUMENT=2
    UNKNOWN_QUEUE_LIMIT_BEHAVIOR=3
    UNKNOWN_QUEUE_INSERT_BEHAVIOR=4
    UNKNOWN_OPERATION=5
    UNKNOWN_ERROR=6

class QueueOperationType(Enum):
    NONE=0
    PUBLISH=1
    SUBSCRIBE=2
    UNSUBSCRIBE=3

class LimitBehavior(Enum):
    DROP_FRONT=0
    DROP_BACK=1
    RETURN_ERROR=2

class InsertBehavior(Enum):
    INSERT_FRONT=0
    INSERT_BACK=1

class QueueOperation():
    type : QueueOperationType = QueueOperationType.NONE
    topic : str = ""
    payload: any = None
    qos : mqtt.QoS = mqtt.QoS.AT_MOST_ONCE
    retain : bool = None
    subscribe_callback : FunctionType = None

#######################################################
# Classes
########################################################

class OperationQueueBuilder:
    _connection : mqtt.Connection = None
    _queue_limit_size : int = 10
    _queue_limit_behavior : LimitBehavior = LimitBehavior.DROP_BACK
    _queue_insert_behavior : InsertBehavior = InsertBehavior.INSERT_BACK
    _incomplete_limit : int = 1
    _inflight_limit : int = 1
    _on_operation_sent_callback : FunctionType = None
    _on_operation_sent_failure_callback : FunctionType = None
    _on_operation_dropped_callback : FunctionType = None
    _on_queue_full_callback : FunctionType = None
    _on_queue_empty_callback : FunctionType = None
    _queue_loop_time_ms : int = 1000
    _enable_logging : bool = False

    def with_connection(self, connection:mqtt.Connection):
        self._connection = connection
        return self

    def get_connection(self) -> mqtt.Connection:
        return self._connection

    def with_queue_limit_size(self, queue_limit_size:int):
        self._queue_limit_size = queue_limit_size
        return self

    def get_connection(self) -> int:
        return self._queue_limit_size

    def with_queue_limit_behavior(self, queue_limit_behavior:LimitBehavior):
        self._queue_limit_behavior = queue_limit_behavior
        return self

    def get_queue_limit_behavior(self) -> LimitBehavior:
        return self._queue_limit_behavior

    def with_queue_insert_behavior(self, queue_insert_behavior:InsertBehavior):
        self._queue_insert_behavior = queue_insert_behavior
        return self

    def get_queue_insert_behavior(self) -> InsertBehavior:
        return self._queue_insert_behavior

    def with_incomplete_limit(self, incomplete_limit:int):
        self._incomplete_limit = incomplete_limit
        return self

    def get_incomplete_limit(self) -> int:
        return self._incomplete_limit

    def with_inflight_limit(self, inflight_limit:int):
        self._inflight_limit = inflight_limit
        return self

    def get_inflight_limit(self) -> int:
        return self._inflight_limit

    def with_on_operation_sent_callback(self, on_operation_sent_callback: FunctionType):
        self._on_operation_sent_callback = on_operation_sent_callback
        return self

    def get_on_operation_sent_callback(self) -> FunctionType:
        return self._on_operation_sent_callback

    def with_on_operation_sent_failure_callback(self, on_operation_sent_failure_callback: FunctionType):
        self._on_operation_sent_failure_callback = on_operation_sent_failure_callback
        return self

    def get_on_operation_sent_failure_callback(self) -> FunctionType:
        return self._on_operation_sent_failure_callback

    def with_on_operation_dropped_callback(self, on_operation_dropped_callback: FunctionType):
        self._on_operation_dropped_callback = on_operation_dropped_callback
        return self

    def get_on_operation_dropped_callback(self) -> FunctionType:
        return self._on_operation_dropped_callback

    def with_on_queue_full_callback(self, on_queue_full_callback:FunctionType):
        self._on_queue_full_callback = on_queue_full_callback
        return self

    def get_on_queue_full_callback(self) -> FunctionType:
        return self._on_queue_full_callback

    def with_on_queue_empty_callback(self, on_queue_empty_callback:FunctionType):
        self._on_queue_empty_callback = on_queue_empty_callback
        return self

    def get_on_queue_empty_callback(self) -> FunctionType:
        return self._on_queue_empty_callback

    def with_queue_loop_time(self, queue_loop_time_ms:int):
        self._queue_loop_time_ms = queue_loop_time_ms
        return self

    def get_queue_loop_time(self) -> int:
        return self._queue_loop_time_ms

    def with_enable_logging(self, enable_logging:bool):
        self._enable_logging = enable_logging
        return self

    def get_enable_logging(self) -> bool:
        return self._enable_logging

    def build(self):
        return OperationQueue(self)


class OperationQueue:
    _operation_queue : list[QueueOperation] = []
    _operation_queue_lock : Lock = Lock()
    _operation_queue_thread : Thread = None
    _operation_queue_thread_running : bool = False
    # configuration options/settings
    _connection : mqtt.Connection = None
    _queue_limit_size : int = 10
    _queue_limit_behavior : LimitBehavior = LimitBehavior.DROP_BACK
    _queue_insert_behavior : InsertBehavior = InsertBehavior.INSERT_BACK
    _incomplete_limit : int = 1
    _inflight_limit : int = 1
    _on_operation_sent_callback : FunctionType = None
    _on_operation_sent_failure_callback : FunctionType = None
    _on_operation_dropped_callback : FunctionType = None
    _on_queue_full_callback : FunctionType = None
    _on_queue_empty_callback : FunctionType = None
    _queue_loop_time_ms : int = 1000
    _enable_logging : bool = False

    def __init__(self, builder:OperationQueueBuilder) -> None:
        self._connection = builder._connection
        self._queue_limit_size = builder._queue_limit_size
        self._queue_limit_behavior = builder._queue_limit_behavior
        self._queue_insert_behavior = builder._queue_insert_behavior
        self._incomplete_limit = builder._incomplete_limit
        self._inflight_limit = builder._inflight_limit
        self._on_operation_sent_callback = builder._on_operation_sent_callback
        self._on_operation_sent_failure_callback = builder._on_operation_sent_failure_callback
        self._on_operation_dropped_callback = builder._on_operation_dropped_callback
        self._on_queue_full_callback = builder._on_queue_full_callback
        self._on_queue_empty_callback = builder._on_queue_empty_callback
        self._queue_loop_time_ms = builder._queue_loop_time_ms
        self._enable_logging = builder._enable_logging

    ####################
    # HELPER FUNCTIONS
    ####################

    def _add_operation_to_queue_insert(self, operation: QueueOperation) -> QueueResult:
        result : QueueResult = QueueResult.SUCCESS
        if (self._queue_insert_behavior == InsertBehavior.INSERT_FRONT):
            self._operation_queue.insert(0, operation)
        elif (self._queue_insert_behavior == InsertBehavior.INSERT_BACK):
            self._operation_queue.insert(len(self._operation_queue), operation)
        else:
            result = QueueResult.UNKNOWN_QUEUE_INSERT_BEHAVIOR
        return result

    def _add_operation_to_queue_overflow(self, operation: QueueOperation) -> tuple:
        result = [QueueResult.SUCCESS, None]
        if (self._queue_limit_behavior == LimitBehavior.RETURN_ERROR):
            self._print_log_message("Did not drop any operation, instead returning error...")
            result[0] = QueueResult.ERROR_QUEUE_FULL
        elif (self._queue_limit_behavior == LimitBehavior.DROP_FRONT):
            result[1] = self._operation_queue[0]
            del self._operation_queue[0]
            self._print_log_message(f"Dropped operation of type {result[1].type} from the front...")
            result[0] =  self._add_operation_to_queue_insert(operation)
        elif (self._queue_limit_behavior == LimitBehavior.DROP_BACK):
            end_of_queue = len(self._operation_queue)-1
            result[1] = self._operation_queue[end_of_queue]
            del self._operation_queue[end_of_queue]
            self._print_log_message(f"Dropped operation of type {result[1].type} from the back...")
            result[0] = self._add_operation_to_queue_insert(operation)
        else:
            result[0] = QueueResult.UNKNOWN_QUEUE_LIMIT_BEHAVIOR
        return result

    def _add_operation_to_queue(self, operation: QueueOperation) -> QueueResult:
        result : QueueResult = QueueResult.SUCCESS
        dropped_operation : QueueOperation = None

        if (operation == None):
            return QueueResult.ERROR_INVALID_ARGUMENT

        # CRITICAL SECTION
        self._operation_queue_lock.acquire()

        try:
            if (self._queue_limit_size <= 0):
                result = self._add_operation_to_queue_insert(operation)
            else:
                if (len(self._operation_queue)+1 <= self._queue_limit_size):
                    result = self._add_operation_to_queue_insert(operation)
                else:
                    return_data = self._add_operation_to_queue_overflow(operation)
                    dropped_operation = return_data[0]
                    result = return_data[1]
        except Exception as exception:
            self._print_log_message(f"Exception ocurred adding operation to queue. Exception: {exception}")

        self._operation_queue_lock.release()
        # END CRITICAL SECTION

        if (result == QueueResult.SUCCESS):
            self._print_log_message(f"Added operation of type {operation.type} successfully to queue")
            if (len(self._operation_queue) == self._queue_limit_size and dropped_operation == None):
                if (self._on_queue_full_callback != None):
                    self._on_queue_full_callback()

        # Note: We invoke the dropped callback outside of the critical section to avoid deadlocks
        if (dropped_operation != None):
            if (self._on_operation_dropped_callback != None):
                self._on_operation_dropped_callback(dropped_operation)

        return result

    def _print_log_message(self, message:str) -> None:
        if self._enable_logging == True:
            print("[MqttOperationQueue] " + message)

    ####################
    # LOOP FUNCTIONS
    ####################

    def _perform_operation_publish(self, operation: QueueOperation) -> None:
        result = self._connection.publish(operation.topic, operation.payload, operation.qos, operation.retain)
        if (self._on_operation_sent_callback != None):
            self._on_operation_sent_callback(operation, result)

    def _perform_operation_subscribe(self, operation: QueueOperation) -> None:
        result = self._connection.subscribe(operation.topic, operation.qos, operation.subscribe_callback)
        if (self._on_operation_sent_callback != None):
            self._on_operation_sent_callback(operation, result)

    def _perform_operation_unsubscribe(self, operation: QueueOperation) -> None:
        result = self._connection.unsubscribe(operation.topic)
        if (self._on_operation_sent_callback != None):
            self._on_operation_sent_callback(operation, result)

    def _perform_operation_unknown(self, operation: QueueOperation) -> None:
        if (operation == None):
            self._print_log_message("ERROR - got empty/none operation to perform")
        else:
            self._print_log_message("ERROR - got unknown operation to perform")
            if (self._on_operation_sent_failure_callback != None):
                self._on_operation_sent_failure_callback(operation, QueueResult.UNKNOWN_OPERATION)

    def _perform_operation(self, operation: QueueOperation) -> None:
        if (operation == None):
            self._perform_operation_unknown(operation)
        elif (operation.type == QueueOperationType.PUBLISH):
            self._perform_operation_publish(operation)
        elif (operation.type == QueueOperationType.SUBSCRIBE):
            self._perform_operation_subscribe(operation)
        elif (operation.type == QueueOperationType.UNSUBSCRIBE):
            self._perform_operation_unsubscribe(operation)
        else:
            self._perform_operation_unknown(operation)

    def _check_operation_statistics(self) -> bool:
        statistics: mqtt.OperationStatisticsData = self._connection.get_stats()
        if (statistics.incomplete_operation_count >= self._incomplete_limit):
            if (self._incomplete_limit > 0):
                self._print_log_message("Skipping running operation due to incomplete operation count being equal or higher than maximum")
                return False
        if (statistics.unacked_operation_count >= self._inflight_limit):
            if (self._inflight_limit > 0):
                self._print_log_message("Skipping running operation due to inflight operation count being equal or higher than maximum")
                return False
        return True

    def _run_operation(self) -> None:
        # CRITICAL SECTION
        self._operation_queue_lock.acquire()

        try:
            if (len(self._operation_queue) > 0):
                operation : QueueOperation = self._operation_queue[0]
                del self._operation_queue[0]

                self._print_log_message(f"Starting to perform operation of type {operation.type}")
                self._perform_operation(operation)

                if (len(self._operation_queue) <= 0):
                    if (self._on_queue_empty_callback != None):
                        self._on_queue_empty_callback()

                pass
            else:
                self._print_log_message("No operations to perform")
        except Exception as exception:
            self._print_log_message(f"Exception ocurred performing operation! Exception: {exception}")

        self._operation_queue_lock.release()
        # END CRITICAL SECTION

    def _queue_loop(self) -> None:
        while self._operation_queue_thread_running == True:
            self._print_log_message("Performing operation loop...")
            if (self._check_operation_statistics()):
                self._run_operation()
            sleep(self._queue_loop_time_ms / 1000.0)
        pass

    ####################
    # OPERATIONS
    ####################

    def start(self) -> None:
        if (self._operation_queue_thread != None):
            self._print_log_message("Cannot start because queue is already started!")
            return
        self._operation_queue_thread = Thread(target=self._queue_loop)
        self._operation_queue_thread_running = True
        self._operation_queue_thread.start()
        self._print_log_message("Started successfully")

    def stop(self) -> None:
        if (self._operation_queue_thread == None):
            self._print_log_message("Cannot stop because queue is already stopped!")
            return
        self._operation_queue_thread_running = False

        # wait for the thread to finish
        self._print_log_message("Waiting for thread to stop...")
        self._operation_queue_thread.join()
        self._operation_queue_thread = None
        self._print_log_message("Stopped successfully")

    def publish(self, topic, payload, qos, retain=False) -> QueueResult:
        new_operation = QueueOperation()
        new_operation.type = QueueOperationType.PUBLISH
        new_operation.topic = topic
        new_operation.payload = payload
        new_operation.qos = qos
        new_operation.retain = retain
        return self._add_operation_to_queue(new_operation)

    def subscribe(self, topic, qos, callback=None) -> QueueResult:
        new_operation = QueueOperation()
        new_operation.type = QueueOperationType.SUBSCRIBE
        new_operation.topic = topic
        new_operation.qos = qos
        new_operation.subscribe_callback = callback
        return self._add_operation_to_queue(new_operation)

    def unsubscribe(self, topic) -> QueueResult:
        new_operation = QueueOperation()
        new_operation.type = QueueOperationType.UNSUBSCRIBE
        new_operation.topic = topic
        return self._add_operation_to_queue(new_operation)

    def add_queue_operation(self, operation: QueueOperation) -> QueueResult:
        # Basic validation
        if (operation.type == QueueOperationType.NONE):
            return QueueResult.ERROR_INVALID_ARGUMENT
        elif (operation.type == QueueOperationType.PUBLISH):
            if (operation.topic == None or operation.qos == None):
                return QueueResult.ERROR_INVALID_ARGUMENT
        elif (operation.type == QueueOperationType.SUBSCRIBE):
            if (operation.topic == None or operation.qos == None):
                return QueueResult.ERROR_INVALID_ARGUMENT
        elif (operation.type == QueueOperationType.UNSUBSCRIBE):
            if (operation.topic == None):
                return QueueResult.ERROR_INVALID_ARGUMENT
        else:
            return QueueResult.UNKNOWN_ERROR
        return self._add_operation_to_queue(operation)

    def get_queue_size(self) -> int:
        # CRITICAL SECTION
        self._operation_queue_lock.acquire()
        size : int = len(self._operation_queue)
        self._operation_queue_lock.release()
        # END CRITICAL SECTION
        return size

    def get_queue_limit(self) -> int:
        return self._queue_limit_size
