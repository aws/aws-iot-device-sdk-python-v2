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
    """
    The result of attempting to perform an operation on the MqttOperationQueue.
    The value indicates either success or what type of issue was encountered.
    """
    SUCCESS=0
    ERROR_QUEUE_FULL=1
    ERROR_INVALID_ARGUMENT=2
    UNKNOWN_QUEUE_LIMIT_BEHAVIOR=3
    UNKNOWN_QUEUE_INSERT_BEHAVIOR=4
    UNKNOWN_OPERATION=5
    UNKNOWN_ERROR=6

class QueueOperationType(Enum):
    """
    An enum to indicate the type of data the QueueOperation contains. Used
    to differentiate between different operations in a common blob object.
    """
    NONE=0
    PUBLISH=1
    SUBSCRIBE=2
    UNSUBSCRIBE=3

class LimitBehavior(Enum):
    """
    An enum to indicate what happens when the MqttOperationQueue is completely full but new
    operations are requested to be added to the queue.
    """
    DROP_FRONT=0
    DROP_BACK=1
    RETURN_ERROR=2

class InsertBehavior(Enum):
    """
    An enum to indicate what happens when the MqttOperationQueue has a new operation it
    needs to add to the queue, configuring where the new operation is added.
    """
    INSERT_FRONT=0
    INSERT_BACK=1

class QueueOperation():
    """
    A blob class containing all of the data an operation can possibly possess, as well as
    an enum to indicate what type of operation should be stored within. Used to provide
    a common base that all operations can be derived from.
    """
    type : QueueOperationType = QueueOperationType.NONE
    topic : str = ""
    payload: any = None
    qos : mqtt.QoS = mqtt.QoS.AT_MOST_ONCE
    retain : bool = None
    subscribe_callback : FunctionType = None

#######################################################
# Classes
########################################################

class MqttOperationQueueBuilder:
    """
    A builder that contains all of the options of the MqttOperationQueue.
    This is where you can configure how the operations queue works prior to making the final
    MqttOperationQueue with the build() function.
    """

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
        """
        Sets the mqtt.Connection that will be used by the MqttOperationQueue.
        This is a REQUIRED argument that has to be set in order for the MqttOperationQueue to function.

        Keyword Args:
            connection (mqtt.Connection): The mqtt.Connection that will be used by the MqttOperationQueue.
        """
        self._connection = connection
        return self

    def get_connection(self) -> mqtt.Connection:
        """
        Returns the mqtt.Connection used by the MqttOperationQueue
        """
        return self._connection

    def with_queue_limit_size(self, queue_limit_size:int):
        """
        Sets the maximum size of the operation queue in the MqttOperationQueue.
        Default operation queue size is 10.

        If the number of operations exceeds this number, then the queue will be adjusted
        based on the queue_limit_behavior.

        Keyword Args:
            queue_limit_size (int): The maximum size of the operation queue in the MqttOperationQueue.
        """
        self._queue_limit_size = queue_limit_size
        return self

    def get_connection(self) -> int:
        """
        Returns the maximum size of the operation queue in the MqttOperationQueue.
        """
        return self._queue_limit_size

    def with_queue_limit_behavior(self, queue_limit_behavior:LimitBehavior):
        """
        Sets how the MqttOperationQueue will behave when the operation queue is full but a
        new operation is requested to be added to the queue.
        The default is DROP_BACK, which will drop the newest (but last to be executed) operation at the back of the queue.

        Keyword Args:
            queue_limit_behavior (LimitBehavior): How the MqttOperationQueue will behave when the operation queue is full.
        """
        self._queue_limit_behavior = queue_limit_behavior
        return self

    def get_queue_limit_behavior(self) -> LimitBehavior:
        """
        Returns how the MqttOperationQueue will behave when the operation queue is full.
        """
        return self._queue_limit_behavior

    def with_queue_insert_behavior(self, queue_insert_behavior:InsertBehavior):
        """
        Sets how the MqttOperationQueue will behave when inserting a new operation into the queue.
        The default is INSERT_BACK, which will add the new operation to the back (last to be executed) of the queue.

        Keyword Args:
            queue_insert_behavior (InsertBehavior): How the MqttOperationQueue will behave when inserting a new operation into the queue.
        """
        self._queue_insert_behavior = queue_insert_behavior
        return self

    def get_queue_insert_behavior(self) -> InsertBehavior:
        """
        Returns how the MqttOperationQueue will behave when inserting a new operation into the queue.
        """
        return self._queue_insert_behavior

    def with_incomplete_limit(self, incomplete_limit:int):
        """
        Sets the maximum number of incomplete operations that the MQTT connection can have before the
        MqttOperationQueue will wait for them to be complete. Incomplete operations are those that have been
        sent to the mqtt.Connection but have not been fully processed and responded to from the MQTT server/broker.

        Once the maximum number of incomplete operations is met, the MqttOperationQueue will wait until the number
        of incomplete operations is below the set maximum.

        Default is set to 1. Set to 0 for no limit.

        Keyword Args:
            incomplete_limit (int): The maximum number of incomplete operations before waiting.
        """
        self._incomplete_limit = incomplete_limit
        return self

    def get_incomplete_limit(self) -> int:
        """
        Returns the maximum number of incomplete operations before waiting.
        """
        return self._incomplete_limit

    def with_inflight_limit(self, inflight_limit:int):
        """
        Sets the maximum number of inflight operations that the MQTT connection can have before the
        MqttOperationQueue will wait for them to be complete. inflight operations are those that have been
        sent to the mqtt.Connection and sent out to the MQTT server/broker, but an acknowledgement from
        the MQTT server/broker has not yet been received.

        Once the maximum number of inflight operations is met, the MqttOperationQueue will wait until the number
        of inflight operations is below the set maximum.

        Default is set to 1. Set to 0 for no limit.

        Keyword Args:
            inflight_limit (int): The maximum number of inflight operations before waiting.
        """
        self._inflight_limit = inflight_limit
        return self

    def get_inflight_limit(self) -> int:
        """
        Returns the maximum number of inflight operations before waiting.
        """
        return self._inflight_limit

    def with_on_operation_sent_callback(self, on_operation_sent_callback: FunctionType):
        """
        Sets the callback that will be invoked when an operation is removed from the queue and sent successfully.

        The callback needs to have the following signature:
            callback_name(operation: QueueOperation, operation_result: tuple)
        * operation is the operation data that was just successfully sent
        * operation_result is a tuple containing the future and the packet ID returned from the MQTT connection

        Keyword Args:
            on_operation_sent_callback (FunctionType): The callback to invoke.
        """
        self._on_operation_sent_callback = on_operation_sent_callback
        return self

    def get_on_operation_sent_callback(self) -> FunctionType:
        """
        Returns the callback invoked when an operation is removed from the queue and sent successfully.
        """
        return self._on_operation_sent_callback

    def with_on_operation_sent_failure_callback(self, on_operation_sent_failure_callback: FunctionType):
        """
        Sets the callback that will be invoked when an operation is removed from the queue but failed to send.

        The callback needs to have the following signature:
            callback_name(operation: QueueOperation, error: QueueResult)
        * operation is the operation data that failed to be sent
        * error is a QueueResult containing the error code for why the operation was not successful.

        Keyword Args:
            on_operation_sent_failure_callback (FunctionType): The callback to invoke.
        """
        self._on_operation_sent_failure_callback = on_operation_sent_failure_callback
        return self

    def get_on_operation_sent_failure_callback(self) -> FunctionType:
        """
        Returns the callback that will be invoked when an operation is removed from the queue but failed to send.
        """
        return self._on_operation_sent_failure_callback

    def with_on_operation_dropped_callback(self, on_operation_dropped_callback: FunctionType):
        """
        Sets the callback that will be invoked when the operation queue is full, a new operation was added
        to the queue, and so an operation had to be removed/dropped from the queue.

        The callback needs to have the following signature:
            callback_name(operation: QueueOperation)
        * operation is the operation data that was just dropped from the queue

        Keyword Args:
            on_operation_dropped_callback (FunctionType): The callback to invoke.
        """
        self._on_operation_dropped_callback = on_operation_dropped_callback
        return self

    def get_on_operation_dropped_callback(self) -> FunctionType:
        """
        Returns the callback that will be invoked when an operation is dropped from the queue
        """
        return self._on_operation_dropped_callback

    def with_on_queue_full_callback(self, on_queue_full_callback:FunctionType):
        """
        Sets the callback that will be invoked when the operation queue is full.

        The callback needs to be a function that takes no arguments:
            callback_name()

        Keyword Args:
            on_queue_full_callback (FunctionType): The callback to invoke.
        """
        self._on_queue_full_callback = on_queue_full_callback
        return self

    def get_on_queue_full_callback(self) -> FunctionType:
        """
        Returns the callback that will be invoked when the operation queue is full.
        """
        return self._on_queue_full_callback

    def with_on_queue_empty_callback(self, on_queue_empty_callback:FunctionType):
        """
        Sets the callback that will be invoked when the operation queue is completely empty.

        The callback needs to be a function that takes no arguments:
            callback_name()

        Keyword Args:
            on_queue_empty_callback (FunctionType): The callback to invoke.
        """
        self._on_queue_empty_callback = on_queue_empty_callback
        return self

    def get_on_queue_empty_callback(self) -> FunctionType:
        """
        Returns the callback that will be invoked when the operation queue is completely empty.
        """
        return self._on_queue_empty_callback

    def with_queue_loop_time(self, queue_loop_time_ms:int):
        """
        Sets the interval, in milliseconds, that the MqttOperationQueue will wait before checking the queue and (possibly)
        processing an operation based on the statistics and state of the MqttClientConnection assigned to the MqttOperationQueue.
        The default is every second.

        Keyword Args:
            queue_loop_time_ms (int): The interval, in milliseconds, that the MqttOperationQueue will wait before checking the queue.
        """
        self._queue_loop_time_ms = queue_loop_time_ms
        return self

    def get_queue_loop_time(self) -> int:
        """
        Returns the interval, in milliseconds, that the MqttOperationQueue will wait before checking the queue.
        """
        return self._queue_loop_time_ms

    def with_enable_logging(self, enable_logging:bool):
        """
        Sets whether the MqttOperationQueue will print logging statements to help debug and determine how the
        MqttOperationQueue is functioning.

        Keyword Args:
            enable_logging (bool): Whether the MqttOperationQueue will print logging statements.
        """
        self._enable_logging = enable_logging
        return self

    def get_enable_logging(self) -> bool:
        """
        Returns whether the MqttOperationQueue will print logging statements.
        """
        return self._enable_logging

    def build(self):
        """
        Returns a new MqttOperationQueue with the options set in the builder
        """
        return MqttOperationQueue(self)


class MqttOperationQueue:
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
    _queue_loop_time_sec : int = 1
    _enable_logging : bool = False

    def __init__(self, builder:MqttOperationQueueBuilder) -> None:
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
        self._queue_loop_time_sec = builder._queue_loop_time_ms / 1000.0 # convert to seconds since that is what sleep uses
        self._enable_logging = builder._enable_logging

    ####################
    # HELPER FUNCTIONS
    ####################

    def _add_operation_to_queue_insert(self, operation: QueueOperation) -> QueueResult:
        """
        Helper function: Inserts the given QueueOperation into the queue/list directly.
        Used to simplify inserting in front/back based on configuration options.
        Called by both _add_operation_to_queue and _add_operation_to_queue_overflow.

        Keyword Args:
            operation (QueueOperation): The operation to add.
        """
        result : QueueResult = QueueResult.SUCCESS
        if (self._queue_insert_behavior == InsertBehavior.INSERT_FRONT):
            self._operation_queue.insert(0, operation)
        elif (self._queue_insert_behavior == InsertBehavior.INSERT_BACK):
            self._operation_queue.insert(len(self._operation_queue), operation)
        else:
            result = QueueResult.UNKNOWN_QUEUE_INSERT_BEHAVIOR
        return result

    def _add_operation_to_queue_overflow(self, operation: QueueOperation) -> tuple:
        """
        Helper function: Adds the given QueueOperation to the queue when the queue is full.
        Used to make separate the logic for when the queue is full from when it is not yet full.
        Called by _add_operation_to_queue.

        Keyword Args:
            operation (QueueOperation): The operation to add.
        """
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
        """
        Helper function: Adds the given QueueOperation to the queue of operations to be processed.

        Keyword Args:
            operation (QueueOperation): The operation to add.
        """
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
        """
        Helper function: Prints to the console if logging is enabled.
        Just makes code a little cleaner and easier to process.

        Keyword Args:
            message (str): The message to print.
        """
        if self._enable_logging == True:
            print("[MqttOperationQueue] " + message)

    ####################
    # LOOP FUNCTIONS
    ####################

    def _perform_operation_publish(self, operation: QueueOperation) -> None:
        """
        Helper function: Takes the publish operation and passes it to the MQTT connection.
        """
        result = self._connection.publish(operation.topic, operation.payload, operation.qos, operation.retain)
        if (self._on_operation_sent_callback != None):
            self._on_operation_sent_callback(operation, result)

    def _perform_operation_subscribe(self, operation: QueueOperation) -> None:
        """
        Helper function: Takes the subscribe operation and passes it to the MQTT connection.
        """
        result = self._connection.subscribe(operation.topic, operation.qos, operation.subscribe_callback)
        if (self._on_operation_sent_callback != None):
            self._on_operation_sent_callback(operation, result)

    def _perform_operation_unsubscribe(self, operation: QueueOperation) -> None:
        """
        Helper function: Takes the unsubscribe operation and passes it to the MQTT connection.
        """
        result = self._connection.unsubscribe(operation.topic)
        if (self._on_operation_sent_callback != None):
            self._on_operation_sent_callback(operation, result)

    def _perform_operation_unknown(self, operation: QueueOperation) -> None:
        """
        Helper function: Takes the operation if it is unknown and sends it as a failure to the callback.
        """
        if (operation == None):
            self._print_log_message("ERROR - got empty/none operation to perform")
        else:
            self._print_log_message("ERROR - got unknown operation to perform")
            if (self._on_operation_sent_failure_callback != None):
                self._on_operation_sent_failure_callback(operation, QueueResult.UNKNOWN_OPERATION)

    def _perform_operation(self, operation: QueueOperation) -> None:
        """
        Helper function: Based on the operation type, calls the appropriate helper function.
        """
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
        """
        Helper function: Checks the MQTT connection operation statistics to see if their values are higher than the maximum
        values set in MqttOperationQueue. If the value is higher than the maximum in MqttOperationQueue, then it returns false
        so an operation on the queue will not be processed.
        Called by the _queue_loop() function
        """
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
        """
        Helper function: Takes the operation off the queue, checks what operation it is, and passes
        it to the MQTT connection to be run.
        Called by the _queue_loop() function
        """
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
        """
        This function is called every queue_loop_time_ms milliseconds. This is where the logic for handling
        the queue resides.
        """
        while self._operation_queue_thread_running == True:
            self._print_log_message("Performing operation loop...")
            if (self._check_operation_statistics()):
                self._run_operation()
            sleep(self._queue_loop_time_sec)
        pass

    ####################
    # OPERATIONS
    ####################

    def start(self) -> None:
        """
        Starts the MqttOperationQueue running so it can process the queue.
        Every queue_loop_time_ms milliseconds it will check the queue to see if there is at least a single
        operation waiting. If there is, it will check the MQTT client statistics to determine if
        the MQTT connection has the bandwidth for the next operation (based on incomplete_limit and inflight_limit)
        and, if the MQTT connection has bandwidth, will start a next operation from the queue.
        """
        if (self._operation_queue_thread != None):
            self._print_log_message("Cannot start because queue is already started!")
            return
        self._operation_queue_thread = Thread(target=self._queue_loop)
        self._operation_queue_thread_running = True
        self._operation_queue_thread.start()
        self._print_log_message("Started successfully")

    def stop(self) -> None:
        """
        Stops the MqttOperationQueue from running and processing operations that may be left in the queue.
        Once stopped, the MqttOperationQueue can be restarted by calling start() again.

        Note: calling stop() will block the thread temporarily as it waits for the operation queue thread to finish
        """
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
        """
        Creates a new Publish operation and adds it to the queue to be run.

        Note that the inputs to this function are exactly the same as the publish() function in
        the mqtt.connection, but instead of executing the operation as soon as possible, it
        will be added to the queue based on the queue_insert_behavior and processed accordingly.

        The on_operation_sent callback function will be invoked when the operation is
        processed and sent by the client.

        Keyword Args:
            topic (str): The topic to send the publish to
            payload (any): The payload to send
            qos (mqtt.QoS): The Quality of Service (QoS) to send the publish with
            retain (bool): Whether the publish should be retained on the server
        """
        new_operation = QueueOperation()
        new_operation.type = QueueOperationType.PUBLISH
        new_operation.topic = topic
        new_operation.payload = payload
        new_operation.qos = qos
        new_operation.retain = retain
        return self._add_operation_to_queue(new_operation)

    def subscribe(self, topic, qos, callback=None) -> QueueResult:
        """
        Creates a new subscribe operation and adds it to the queue to be run.

        Note that the inputs to this function are exactly the same as the subscribe() function in
        the mqtt.connection, but instead of executing the operation as soon as possible, it
        will be added to the queue based on the queue_insert_behavior and processed accordingly.

        The on_operation_sent callback function will be invoked when the operation is
        processed and sent by the client.

        Keyword Args:
            topic (str): The topic to subscribe to
            qos (mqtt.QoS): The Quality of Service (QoS) to send the subscribe with
            callback (function): The function to invoke when a publish is sent to the subscribed topic
        """
        new_operation = QueueOperation()
        new_operation.type = QueueOperationType.SUBSCRIBE
        new_operation.topic = topic
        new_operation.qos = qos
        new_operation.subscribe_callback = callback
        return self._add_operation_to_queue(new_operation)

    def unsubscribe(self, topic) -> QueueResult:
        """
        Creates a new unsubscribe operation and adds it to the queue to be run.

        Note that the inputs to this function are exactly the same as the unsubscribe() function in
        the mqtt.connection, but instead of executing the operation as soon as possible, it
        will be added to the queue based on the queue_insert_behavior and processed accordingly.

        The on_operation_sent callback function will be invoked when the operation is
        processed and sent by the client.

        Keyword Args:
            topic (str): The topic to unsubscribe to
        """
        new_operation = QueueOperation()
        new_operation.type = QueueOperationType.UNSUBSCRIBE
        new_operation.topic = topic
        return self._add_operation_to_queue(new_operation)

    def add_queue_operation(self, operation: QueueOperation) -> QueueResult:
        """
        Adds a new queue operation (publish, subscribe, unsubscribe) to the queue to be run.

        Note: This function provides only basic validation of the operation data. It is primarily
        intended to be used with the on_operation_dropped callback for when you may want to
        add a dropped message back to the queue.
        (for example, say it's an important message you know you want to send)

        Keyword Args:
            operation (QueueOperation): The operation to add to the queue
        """
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
        """
        Returns the current size of the operation queue.
        """
        # CRITICAL SECTION
        self._operation_queue_lock.acquire()
        size : int = len(self._operation_queue)
        self._operation_queue_lock.release()
        # END CRITICAL SECTION
        return size

    def get_queue_limit(self) -> int:
        """
        Returns the maximum size of this operation queue.
        """
        return self._queue_limit_size
