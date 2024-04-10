# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot.eventstreamrpc as rpc
import base64
import datetime
import typing


class EchoTestRPCError(rpc.ErrorShape):
    """
    Base for all error messages sent by server.
    """

    def _get_error_type_string(self) -> str:
        # overridden in subclasses
        raise NotImplementedError

    def is_retryable(self) -> bool:
        return self._get_error_type_string() == 'server'

    def is_server_error(self) -> bool:
        return self._get_error_type_string() == 'server'

    def is_client_error(self) -> bool:
        return self._get_error_type_string() == 'client'


class Product(rpc.Shape):
    """
    Product

    A simple product definition

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        name: The product's name
        price: How much the product costs

    Attributes:
        name: The product's name
        price: How much the product costs
    """

    def __init__(self, *,
                 name: typing.Optional[str] = None,
                 price: typing.Optional[float] = None):
        super().__init__()
        self.name = name  # type: typing.Optional[str]
        self.price = price  # type: typing.Optional[float]

    def set_name(self, name: str):
        self.name = name
        return self

    def set_price(self, price: float):
        self.price = price
        return self


    def _to_payload(self):
        payload = {}
        if self.name is not None:
            payload['name'] = self.name
        if self.price is not None:
            payload['price'] = self.price
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'name' in payload:
            new.name = payload['name']
        if 'price' in payload:
            new.price = float(payload['price'])
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#Product'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class Pair(rpc.Shape):
    """
    Pair

    Shape representing a pair of values

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        key: Pair.key as a string
        value: Pair.value also a string!

    Attributes:
        key: Pair.key as a string
        value: Pair.value also a string!
    """

    def __init__(self, *,
                 key: typing.Optional[str] = None,
                 value: typing.Optional[str] = None):
        super().__init__()
        self.key = key  # type: typing.Optional[str]
        self.value = value  # type: typing.Optional[str]

    def set_key(self, key: str):
        self.key = key
        return self

    def set_value(self, value: str):
        self.value = value
        return self


    def _to_payload(self):
        payload = {}
        if self.key is not None:
            payload['key'] = self.key
        if self.value is not None:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'key' in payload:
            new.key = payload['key']
        if 'value' in payload:
            new.value = payload['value']
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#Pair'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class FruitEnum:
    """
    FruitEnum enum
    """

    APPLE = 'apl'
    ORANGE = 'org'
    BANANA = 'ban'
    PINEAPPLE = 'pin'


class Customer(rpc.Shape):
    """
    Customer

    A simple customer definition

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        id: Opaque customer identifier
        first_name: First name of the customer
        last_name: Last name of the customer

    Attributes:
        id: Opaque customer identifier
        first_name: First name of the customer
        last_name: Last name of the customer
    """

    def __init__(self, *,
                 id: typing.Optional[int] = None,
                 first_name: typing.Optional[str] = None,
                 last_name: typing.Optional[str] = None):
        super().__init__()
        self.id = id  # type: typing.Optional[int]
        self.first_name = first_name  # type: typing.Optional[str]
        self.last_name = last_name  # type: typing.Optional[str]

    def set_id(self, id: int):
        self.id = id
        return self

    def set_first_name(self, first_name: str):
        self.first_name = first_name
        return self

    def set_last_name(self, last_name: str):
        self.last_name = last_name
        return self


    def _to_payload(self):
        payload = {}
        if self.id is not None:
            payload['id'] = self.id
        if self.first_name is not None:
            payload['firstName'] = self.first_name
        if self.last_name is not None:
            payload['lastName'] = self.last_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'id' in payload:
            new.id = int(payload['id'])
        if 'firstName' in payload:
            new.first_name = payload['firstName']
        if 'lastName' in payload:
            new.last_name = payload['lastName']
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#Customer'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class MessageData(rpc.Shape):
    """
    MessageData

    Data associated with some notion of a message

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        string_message: Some string data
        boolean_message: Some boolean data
        time_message: Some timestamp data
        document_message: Some document data
        enum_message: FruitEnum enum value. Some FruitEnum data
        blob_message: Some blob data
        string_list_message: Some list of strings data
        key_value_pair_list: A list of key-value pairs
        string_to_value: A map from strings to Product shapes

    Attributes:
        string_message: Some string data
        boolean_message: Some boolean data
        time_message: Some timestamp data
        document_message: Some document data
        enum_message: FruitEnum enum value. Some FruitEnum data
        blob_message: Some blob data
        string_list_message: Some list of strings data
        key_value_pair_list: A list of key-value pairs
        string_to_value: A map from strings to Product shapes
    """

    def __init__(self, *,
                 string_message: typing.Optional[str] = None,
                 boolean_message: typing.Optional[bool] = None,
                 time_message: typing.Optional[datetime.datetime] = None,
                 document_message: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 enum_message: typing.Optional[str] = None,
                 blob_message: typing.Optional[typing.Union[bytes, str]] = None,
                 string_list_message: typing.Optional[typing.List[str]] = None,
                 key_value_pair_list: typing.Optional[typing.List[Pair]] = None,
                 string_to_value: typing.Optional[typing.Dict[str, Product]] = None):
        super().__init__()
        self.string_message = string_message  # type: typing.Optional[str]
        self.boolean_message = boolean_message  # type: typing.Optional[bool]
        self.time_message = time_message  # type: typing.Optional[datetime.datetime]
        self.document_message = document_message  # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.enum_message = enum_message  # type: typing.Optional[str]
        if blob_message is not None and isinstance(blob_message, str):
            blob_message = blob_message.encode('utf-8')
        self.blob_message = blob_message  # type: typing.Optional[bytes]
        self.string_list_message = string_list_message  # type: typing.Optional[typing.List[str]]
        self.key_value_pair_list = key_value_pair_list  # type: typing.Optional[typing.List[Pair]]
        self.string_to_value = string_to_value  # type: typing.Optional[typing.Dict[str, Product]]

    def set_string_message(self, string_message: str):
        self.string_message = string_message
        return self

    def set_boolean_message(self, boolean_message: bool):
        self.boolean_message = boolean_message
        return self

    def set_time_message(self, time_message: datetime.datetime):
        self.time_message = time_message
        return self

    def set_document_message(self, document_message: typing.Dict[str, typing.Any]):
        self.document_message = document_message
        return self

    def set_enum_message(self, enum_message: str):
        self.enum_message = enum_message
        return self

    def set_blob_message(self, blob_message: typing.Union[bytes, str]):
        if blob_message is not None and isinstance(blob_message, str):
            blob_message = blob_message.encode('utf-8')
        self.blob_message = blob_message
        return self

    def set_string_list_message(self, string_list_message: typing.List[str]):
        self.string_list_message = string_list_message
        return self

    def set_key_value_pair_list(self, key_value_pair_list: typing.List[Pair]):
        self.key_value_pair_list = key_value_pair_list
        return self

    def set_string_to_value(self, string_to_value: typing.Dict[str, Product]):
        self.string_to_value = string_to_value
        return self


    def _to_payload(self):
        payload = {}
        if self.string_message is not None:
            payload['stringMessage'] = self.string_message
        if self.boolean_message is not None:
            payload['booleanMessage'] = self.boolean_message
        if self.time_message is not None:
            payload['timeMessage'] = self.time_message.timestamp()
        if self.document_message is not None:
            payload['documentMessage'] = self.document_message
        if self.enum_message is not None:
            payload['enumMessage'] = self.enum_message
        if self.blob_message is not None:
            payload['blobMessage'] = base64.b64encode(self.blob_message).decode()
        if self.string_list_message is not None:
            payload['stringListMessage'] = self.string_list_message
        if self.key_value_pair_list is not None:
            payload['keyValuePairList'] = [i._to_payload() for i in self.key_value_pair_list]
        if self.string_to_value is not None:
            payload['stringToValue'] = {k: v._to_payload() for k, v in self.string_to_value.items()}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'stringMessage' in payload:
            new.string_message = payload['stringMessage']
        if 'booleanMessage' in payload:
            new.boolean_message = payload['booleanMessage']
        if 'timeMessage' in payload:
            new.time_message = datetime.datetime.fromtimestamp(payload['timeMessage'], datetime.timezone.utc)
        if 'documentMessage' in payload:
            new.document_message = payload['documentMessage']
        if 'enumMessage' in payload:
            new.enum_message = payload['enumMessage']
        if 'blobMessage' in payload:
            new.blob_message = base64.b64decode(payload['blobMessage'])
        if 'stringListMessage' in payload:
            new.string_list_message = payload['stringListMessage']
        if 'keyValuePairList' in payload:
            new.key_value_pair_list = [Pair._from_payload(i) for i in payload['keyValuePairList']]
        if 'stringToValue' in payload:
            new.string_to_value = {k: Product._from_payload(v) for k,v in payload['stringToValue'].items()}
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#MessageData'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class EchoStreamingMessage(rpc.Shape):
    """
    EchoStreamingMessage is a "tagged union" class.

    A union of values related to a streaming message.  Only one field may bet set.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        stream_message: A message data record
        key_value_pair: A key value pair

    Attributes:
        stream_message: A message data record
        key_value_pair: A key value pair
    """

    def __init__(self, *,
                 stream_message: typing.Optional[MessageData] = None,
                 key_value_pair: typing.Optional[Pair] = None):
        super().__init__()
        self.stream_message = stream_message  # type: typing.Optional[MessageData]
        self.key_value_pair = key_value_pair  # type: typing.Optional[Pair]

    def set_stream_message(self, stream_message: MessageData):
        self.stream_message = stream_message
        return self

    def set_key_value_pair(self, key_value_pair: Pair):
        self.key_value_pair = key_value_pair
        return self


    def _to_payload(self):
        payload = {}
        if self.stream_message is not None:
            payload['streamMessage'] = self.stream_message._to_payload()
        if self.key_value_pair is not None:
            payload['keyValuePair'] = self.key_value_pair._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'streamMessage' in payload:
            new.stream_message = MessageData._from_payload(payload['streamMessage'])
        if 'keyValuePair' in payload:
            new.key_value_pair = Pair._from_payload(payload['keyValuePair'])
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoStreamingMessage'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class ServiceError(EchoTestRPCError):
    """
    ServiceError

    A sample error shape

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: An error message
        value: Some auxiliary value

    Attributes:
        message: An error message
        value: Some auxiliary value
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None,
                 value: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]
        self.value = value  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self

    def set_value(self, value: str):
        self.value = value
        return self


    def _get_error_type_string(self):
        return 'server'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        if self.value is not None:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        if 'value' in payload:
            new.value = payload['value']
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#ServiceError'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class GetAllCustomersResponse(rpc.Shape):
    """
    GetAllCustomersResponse

    All data associated with the result of a GetAllCustomers operation

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        customers: A list of all known customers

    Attributes:
        customers: A list of all known customers
    """

    def __init__(self, *,
                 customers: typing.Optional[typing.List[Customer]] = None):
        super().__init__()
        self.customers = customers  # type: typing.Optional[typing.List[Customer]]

    def set_customers(self, customers: typing.List[Customer]):
        self.customers = customers
        return self


    def _to_payload(self):
        payload = {}
        if self.customers is not None:
            payload['customers'] = [i._to_payload() for i in self.customers]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'customers' in payload:
            new.customers = [Customer._from_payload(i) for i in payload['customers']]
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllCustomersResponse'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class GetAllCustomersRequest(rpc.Shape):
    """
    GetAllCustomersRequest

    Data needed to perform a GetAllCustomers operation
    """

    def __init__(self):
        super().__init__()


    def _to_payload(self):
        payload = {}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllCustomersRequest'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class EchoMessageResponse(rpc.Shape):
    """
    EchoMessageResponse

    All data associated with the result of an EchoMessage operation

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: Some message data

    Attributes:
        message: Some message data
    """

    def __init__(self, *,
                 message: typing.Optional[MessageData] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[MessageData]

    def set_message(self, message: MessageData):
        self.message = message
        return self


    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = MessageData._from_payload(payload['message'])
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoMessageResponse'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class EchoMessageRequest(rpc.Shape):
    """
    EchoMessageRequest

    Data needed to perform an EchoMessage operation

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: Some message data

    Attributes:
        message: Some message data
    """

    def __init__(self, *,
                 message: typing.Optional[MessageData] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[MessageData]

    def set_message(self, message: MessageData):
        self.message = message
        return self


    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = MessageData._from_payload(payload['message'])
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoMessageRequest'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class EchoStreamingResponse(rpc.Shape):
    """
    EchoStreamingResponse

    Data associated with the response to starting an EchoStreaming streaming operation
    """

    def __init__(self):
        super().__init__()


    def _to_payload(self):
        payload = {}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoStreamingResponse'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class EchoStreamingRequest(rpc.Shape):
    """
    EchoStreamingRequest

    Data needed to start an EchoStreaming streaming operation
    """

    def __init__(self):
        super().__init__()


    def _to_payload(self):
        payload = {}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoStreamingRequest'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class CauseServiceErrorResponse(rpc.Shape):
    """
    CauseServiceErrorResponse

    All data associated with the result of an EchoMessage operation
    """

    def __init__(self):
        super().__init__()


    def _to_payload(self):
        payload = {}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#CauseServiceErrorResponse'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class CauseServiceErrorRequest(rpc.Shape):
    """
    CauseServiceErrorRequest

    Data needed to perform a CauseServiceError operation
    """

    def __init__(self):
        super().__init__()


    def _to_payload(self):
        payload = {}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#CauseServiceErrorRequest'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class GetAllProductsResponse(rpc.Shape):
    """
    GetAllProductsResponse

    All data associated with the result of a GetAllProducts operation

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        products: A map from strings to products

    Attributes:
        products: A map from strings to products
    """

    def __init__(self, *,
                 products: typing.Optional[typing.Dict[str, Product]] = None):
        super().__init__()
        self.products = products  # type: typing.Optional[typing.Dict[str, Product]]

    def set_products(self, products: typing.Dict[str, Product]):
        self.products = products
        return self


    def _to_payload(self):
        payload = {}
        if self.products is not None:
            payload['products'] = {k: v._to_payload() for k, v in self.products.items()}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'products' in payload:
            new.products = {k: Product._from_payload(v) for k,v in payload['products'].items()}
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllProductsResponse'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class GetAllProductsRequest(rpc.Shape):
    """
    GetAllProductsRequest

    Data needed to perform a GetAllProducts operation
    """

    def __init__(self):
        super().__init__()


    def _to_payload(self):
        payload = {}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllProductsRequest'

    def __repr__(self):
        attrs = []
        for attr, val in self.__dict__.items():
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


SHAPE_INDEX = rpc.ShapeIndex([
    Product,
    Pair,
    Customer,
    MessageData,
    ServiceError,
    GetAllCustomersResponse,
    GetAllCustomersRequest,
    EchoMessageResponse,
    EchoMessageRequest,
    EchoStreamingResponse,
    EchoStreamingRequest,
    CauseServiceErrorResponse,
    CauseServiceErrorRequest,
    GetAllProductsResponse,
    GetAllProductsRequest,
])


class _CauseServiceErrorOperation(rpc.ClientOperation):
    """
    Throws a ServiceError instead of returning a response.
    """

    @classmethod
    def _model_name(cls):
        return 'awstest#CauseServiceError'

    @classmethod
    def _request_type(cls):
        return CauseServiceErrorRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return CauseServiceErrorResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _CauseStreamServiceToErrorOperation(rpc.ClientOperation):
    """
    Responds to initial request normally then throws a ServiceError on stream response
    """

    @classmethod
    def _model_name(cls):
        return 'awstest#CauseStreamServiceToError'

    @classmethod
    def _request_type(cls):
        return EchoStreamingRequest

    @classmethod
    def _request_stream_type(cls):
        return EchoStreamingMessage

    @classmethod
    def _response_type(cls):
        return EchoStreamingResponse

    @classmethod
    def _response_stream_type(cls):
        return EchoStreamingMessage


class _EchoMessageOperation(rpc.ClientOperation):
    """
    Returns the same data sent in the request to the response
    """

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoMessage'

    @classmethod
    def _request_type(cls):
        return EchoMessageRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return EchoMessageResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _EchoStreamMessagesOperation(rpc.ClientOperation):
    """
    Initial request and response are empty, but echos streaming messages sent by client
    """

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoStreamMessages'

    @classmethod
    def _request_type(cls):
        return EchoStreamingRequest

    @classmethod
    def _request_stream_type(cls):
        return EchoStreamingMessage

    @classmethod
    def _response_type(cls):
        return EchoStreamingResponse

    @classmethod
    def _response_stream_type(cls):
        return EchoStreamingMessage


class _GetAllCustomersOperation(rpc.ClientOperation):
    """
    Fetches all customers
    """

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllCustomers'

    @classmethod
    def _request_type(cls):
        return GetAllCustomersRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetAllCustomersResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetAllProductsOperation(rpc.ClientOperation):
    """
    Fetches all products, indexed by SKU
    """

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllProducts'

    @classmethod
    def _request_type(cls):
        return GetAllProductsRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetAllProductsResponse

    @classmethod
    def _response_stream_type(cls):
        return None
