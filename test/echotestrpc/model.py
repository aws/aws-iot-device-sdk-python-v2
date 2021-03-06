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


class Customer(rpc.Shape):
    """
    Customer

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        id: 
        first_name: 
        last_name: 

    Attributes:
        id: 
        first_name: 
        last_name: 
    """

    def __init__(self, *,
                 id: typing.Optional[int] = None,
                 first_name: typing.Optional[str] = None,
                 last_name: typing.Optional[str] = None):
        super().__init__()
        self.id = id  # type: typing.Optional[int]
        self.first_name = first_name  # type: typing.Optional[str]
        self.last_name = last_name  # type: typing.Optional[str]

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


class FruitEnum:
    """
    FruitEnum enum
    """

    APPLE = 'apl'
    ORANGE = 'org'
    BANANA = 'ban'
    PINEAPPLE = 'pin'


class Pair(rpc.Shape):
    """
    Pair

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        key: 
        value: 

    Attributes:
        key: 
        value: 
    """

    def __init__(self, *,
                 key: typing.Optional[str] = None,
                 value: typing.Optional[str] = None):
        super().__init__()
        self.key = key  # type: typing.Optional[str]
        self.value = value  # type: typing.Optional[str]

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


class Product(rpc.Shape):
    """
    Product

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        name: 
        price: 

    Attributes:
        name: 
        price: 
    """

    def __init__(self, *,
                 name: typing.Optional[str] = None,
                 price: typing.Optional[float] = None):
        super().__init__()
        self.name = name  # type: typing.Optional[str]
        self.price = price  # type: typing.Optional[float]

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


class MessageData(rpc.Shape):
    """
    MessageData

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        string_message: 
        boolean_message: 
        time_message: 
        document_message: 
        enum_message: FruitEnum enum value
        blob_message: 
        string_list_message: 
        key_value_pair_list: 

    Attributes:
        string_message: 
        boolean_message: 
        time_message: 
        document_message: 
        enum_message: FruitEnum enum value
        blob_message: 
        string_list_message: 
        key_value_pair_list: 
    """

    def __init__(self, *,
                 string_message: typing.Optional[str] = None,
                 boolean_message: typing.Optional[bool] = None,
                 time_message: typing.Optional[datetime.datetime] = None,
                 document_message: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 enum_message: typing.Optional[str] = None,
                 blob_message: typing.Optional[bytes] = None,
                 string_list_message: typing.Optional[typing.List[str]] = None,
                 key_value_pair_list: typing.Optional[typing.List[Pair]] = None):
        super().__init__()
        self.string_message = string_message  # type: typing.Optional[str]
        self.boolean_message = boolean_message  # type: typing.Optional[bool]
        self.time_message = time_message  # type: typing.Optional[datetime.datetime]
        self.document_message = document_message  # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.enum_message = enum_message  # type: typing.Optional[str]
        self.blob_message = blob_message  # type: typing.Optional[bytes]
        self.string_list_message = string_list_message  # type: typing.Optional[typing.List[str]]
        self.key_value_pair_list = key_value_pair_list  # type: typing.Optional[typing.List[Pair]]

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
    MessageData is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        stream_message: 
        key_value_pair: 

    Attributes:
        stream_message: 
        key_value_pair: 
    """

    def __init__(self, *,
                 stream_message: typing.Optional[MessageData] = None,
                 key_value_pair: typing.Optional[Pair] = None):
        super().__init__()
        self.stream_message = stream_message  # type: typing.Optional[MessageData]
        self.key_value_pair = key_value_pair  # type: typing.Optional[Pair]

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


class GetAllCustomersResponse(rpc.Shape):
    """
    GetAllCustomersResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        customers: 

    Attributes:
        customers: 
    """

    def __init__(self, *,
                 customers: typing.Optional[typing.List[Customer]] = None):
        super().__init__()
        self.customers = customers  # type: typing.Optional[typing.List[Customer]]

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

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[MessageData] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[MessageData]

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

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[MessageData] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[MessageData]

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


class ServiceError(EchoTestRPCError):
    """
    ServiceError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 
        value: 

    Attributes:
        message: 
        value: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None,
                 value: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]
        self.value = value  # type: typing.Optional[str]

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


class GetAllProductsResponse(rpc.Shape):
    """
    GetAllProductsResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        products: 

    Attributes:
        products: 
    """

    def __init__(self, *,
                 products: typing.Optional[typing.Dict[str, Product]] = None):
        super().__init__()
        self.products = products  # type: typing.Optional[typing.Dict[str, Product]]

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
    Customer,
    Pair,
    Product,
    MessageData,
    GetAllCustomersResponse,
    GetAllCustomersRequest,
    EchoMessageResponse,
    EchoMessageRequest,
    EchoStreamingResponse,
    EchoStreamingRequest,
    CauseServiceErrorResponse,
    CauseServiceErrorRequest,
    ServiceError,
    GetAllProductsResponse,
    GetAllProductsRequest,
])


class _GetAllProductsOperation(rpc.ClientOperation):
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


class _CauseServiceErrorOperation(rpc.ClientOperation):
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


class _EchoStreamMessagesOperation(rpc.ClientOperation):
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


class _EchoMessageOperation(rpc.ClientOperation):
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


class _GetAllCustomersOperation(rpc.ClientOperation):
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
