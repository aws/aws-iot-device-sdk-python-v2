# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot.eventstreamrpc as rpc
import base64
import datetime
import enum


class EchoTestRPCError(rpc.ErrorShape):

    def _get_error_type_string(self) -> str:
        # overridden in subclasses
        raise NotImplementedError

    def is_retryable(self) -> bool:
        return self._get_error_type_string() == 'server'

    def is_server_error(self) -> bool:
        return self._get_error_type_string() == 'server'

    def is_client_error(self) -> bool:
        return self._get_error_type_string() == 'client'


class _UnionMixin:
    """Mixin to make a "tagged union" class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setattr__('_active_union_attr', None)

    def __setattr__(self, name, value):
        """Set attr, and clear any previously active attr"""
        # Set value first, so we don't need to unwind if an exception happens.
        super().__setattr__(name, value)
        if not name.startswith('_'):
            if self._active_union_attr is not None and self._active_union_attr != name:
                super().__setattr__(self._active_union_attr, None)
            super().__setattr__('_active_union_attr', name)


class _ExplicitlyNullMixin:
    """Mixin to allow a class's attributes to be "explicitly null"."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setattr__('_explicitly_null_attrs', set())

    def __setattr__(self, name, value):
        """Set attr, attr is no longer explicitly null, even if value is None"""
        # set value first, so we don't need to unwind if an exception happens
        super().__setattr__(name, value)
        if not name.startswith('_'):
            if name in self._explicitly_null_attrs:
                self._explicitly_null_attrs.remove(name)

    def set_explicitly_null(self, attr_name: str):
        """
        Set named attribute to be "explicitly null".

        The attribute's value becomes None, and it will be written as null
        in JSON payloads If an attribute's value is None, but not set
        "explicitly null" then the attribute is omitted entirely from the
        JSON payload.

        (normally, an attribute whose value is None is
        omitted entirely from the payload).

        Any future assignments to the attribute will remove its
        "explicitly null" designation.
        """
        if attr_name.startswith('_'):
            raise AttributeError("cannot set private attribute '{}' explicitly null".format(attr_name))
        setattr(self, attr_name, None)
        self._explicitly_null_attrs.add(attr_name)

    def is_explicitly_null(self, attr_name: str) -> bool:
        """
        Return whether named attribute is "explicitly null".

        An "explicitly null" attribute is None, and was null in the JSON
        payload it came from. If an attribute is not present in the JSON
        payload it came from, it is None, but not "explicitly null".
        """
        return attr_name in self._explicitly_null_attrs


class FruitEnum(enum.Enum):
    APPLE = 'apl'
    ORANGE = 'org'
    BANANA = 'ban'
    PINEAPPLE = 'pin'

    def _to_payload(self):
        return self.value

    @classmethod
    def _from_payload(cls, value):
        try:
            return cls(value)
        except ValueError:
            unknown = object.__new__(cls)
            unknown._name_ = 'UNKNOWN'
            unknown._value_ = value
            return unknown


class Pair(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 key=None,
                 value=None):
        super().__init__()
        self.key = key
        self.value = value

    def _to_payload(self):
        payload = {}
        if self.key is None:
            if self.is_explicitly_null('key'):
                payload['key'] = None
        else:
            payload['key'] = self.key
        if self.value is None:
            if self.is_explicitly_null('value'):
                payload['value'] = None
        else:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'key' in payload:
            if payload['key'] is None:
                new.set_explicitly_null('key')
            else:
                new.key = payload['key']
        if 'value' in payload:
            if payload['value'] is None:
                new.set_explicitly_null('value')
            else:
                new.value = payload['value']
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#Pair'

    def __repr__(self):
        attrs = []
        for attr in ['key', 'value']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, Pair):
            return self.__dict__ == other.__dict__
        return False


class MessageData(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 string_message=None,
                 boolean_message=None,
                 time_message=None,
                 document_message=None,
                 enum_message=None,
                 blob_message=None,
                 string_list_message=None,
                 key_value_pair_list=None):
        super().__init__()
        self.string_message = string_message
        self.boolean_message = boolean_message
        self.time_message = time_message
        self.document_message = document_message
        self.enum_message = enum_message
        self.blob_message = blob_message
        self.string_list_message = string_list_message
        self.key_value_pair_list = key_value_pair_list

    def _to_payload(self):
        payload = {}
        if self.string_message is None:
            if self.is_explicitly_null('string_message'):
                payload['stringMessage'] = None
        else:
            payload['stringMessage'] = self.string_message
        if self.boolean_message is None:
            if self.is_explicitly_null('boolean_message'):
                payload['booleanMessage'] = None
        else:
            payload['booleanMessage'] = self.boolean_message
        if self.time_message is None:
            if self.is_explicitly_null('time_message'):
                payload['timeMessage'] = None
        else:
            payload['timeMessage'] = self.time_message.timestamp()
        if self.document_message is None:
            if self.is_explicitly_null('document_message'):
                payload['documentMessage'] = None
        else:
            payload['documentMessage'] = self.document_message
        if self.enum_message is None:
            if self.is_explicitly_null('enum_message'):
                payload['enumMessage'] = None
        else:
            payload['enumMessage'] = self.enum_message._to_payload()
        if self.blob_message is None:
            if self.is_explicitly_null('blob_message'):
                payload['blobMessage'] = None
        else:
            payload['blobMessage'] = base64.b64encode(self.blob_message).decode()
        if self.string_list_message is None:
            if self.is_explicitly_null('string_list_message'):
                payload['stringListMessage'] = None
        else:
            payload['stringListMessage'] = self.string_list_message
        if self.key_value_pair_list is None:
            if self.is_explicitly_null('key_value_pair_list'):
                payload['keyValuePairList'] = None
        else:
            payload['keyValuePairList'] = [i._to_payload() for i in self.key_value_pair_list]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'stringMessage' in payload:
            if payload['stringMessage'] is None:
                new.set_explicitly_null('string_message')
            else:
                new.string_message = payload['stringMessage']
        if 'booleanMessage' in payload:
            if payload['booleanMessage'] is None:
                new.set_explicitly_null('boolean_message')
            else:
                new.boolean_message = payload['booleanMessage']
        if 'timeMessage' in payload:
            if payload['timeMessage'] is None:
                new.set_explicitly_null('time_message')
            else:
                new.time_message = datetime.datetime.fromtimestamp(payload['timeMessage'], datetime.timezone.utc)
        if 'documentMessage' in payload:
            if payload['documentMessage'] is None:
                new.set_explicitly_null('document_message')
            else:
                new.document_message = payload['documentMessage']
        if 'enumMessage' in payload:
            if payload['enumMessage'] is None:
                new.set_explicitly_null('enum_message')
            else:
                new.enum_message = FruitEnum._from_payload(payload['enumMessage'])
        if 'blobMessage' in payload:
            if payload['blobMessage'] is None:
                new.set_explicitly_null('blob_message')
            else:
                new.blob_message = base64.b64decode(payload['blobMessage'])
        if 'stringListMessage' in payload:
            if payload['stringListMessage'] is None:
                new.set_explicitly_null('string_list_message')
            else:
                new.string_list_message = payload['stringListMessage']
        if 'keyValuePairList' in payload:
            if payload['keyValuePairList'] is None:
                new.set_explicitly_null('key_value_pair_list')
            else:
                new.key_value_pair_list = [Pair._from_payload(i) for i in payload['keyValuePairList']]
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#MessageData'

    def __repr__(self):
        attrs = []
        for attr in ['string_message', 'boolean_message', 'time_message', 'document_message', 'enum_message', 'blob_message', 'string_list_message', 'key_value_pair_list']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, MessageData):
            return self.__dict__ == other.__dict__
        return False


class EchoStreamingMessage(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 stream_message=None,
                 key_value_pair=None):
        super().__init__()
        self.stream_message = None
        self.key_value_pair = None
        if stream_message is not None:
            self.stream_message = stream_message
        if key_value_pair is not None:
            self.key_value_pair = key_value_pair

    def _to_payload(self):
        payload = {}
        if self.stream_message is not None and self._active_union_attr == 'stream_message':
            payload['streamMessage'] = self.stream_message._to_payload()
        if self.key_value_pair is not None and self._active_union_attr == 'key_value_pair':
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
        for attr in ['stream_message', 'key_value_pair']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, EchoStreamingMessage):
            return self.__dict__ == other.__dict__
        return False


class GetAllCustomersResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 customers=None):
        super().__init__()
        self.customers = customers

    def _to_payload(self):
        payload = {}
        if self.customers is None:
            if self.is_explicitly_null('customers'):
                payload['customers'] = None
        else:
            payload['customers'] = [i._to_payload() for i in self.customers]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'customers' in payload:
            if payload['customers'] is None:
                new.set_explicitly_null('customers')
            else:
                new.customers = [Customer._from_payload(i) for i in payload['customers']]
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllCustomersResponse'

    def __repr__(self):
        attrs = []
        for attr in ['customers']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetAllCustomersResponse):
            return self.__dict__ == other.__dict__
        return False


class GetAllCustomersRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetAllCustomersRequest):
            return self.__dict__ == other.__dict__
        return False


class EchoMessageResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = MessageData._from_payload(payload['message'])
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoMessageResponse'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, EchoMessageResponse):
            return self.__dict__ == other.__dict__
        return False


class EchoMessageRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = MessageData._from_payload(payload['message'])
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#EchoMessageRequest'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, EchoMessageRequest):
            return self.__dict__ == other.__dict__
        return False


class EchoStreamingResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, EchoStreamingResponse):
            return self.__dict__ == other.__dict__
        return False


class EchoStreamingRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, EchoStreamingRequest):
            return self.__dict__ == other.__dict__
        return False


class CauseServiceErrorResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, CauseServiceErrorResponse):
            return self.__dict__ == other.__dict__
        return False


class CauseServiceErrorRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, CauseServiceErrorRequest):
            return self.__dict__ == other.__dict__
        return False


class ServiceError(EchoTestRPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None,
                 value=None):
        super().__init__()
        self.message = message
        self.value = value

    def _get_error_type_string(self):
        return 'server'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        if self.value is None:
            if self.is_explicitly_null('value'):
                payload['value'] = None
        else:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        if 'value' in payload:
            if payload['value'] is None:
                new.set_explicitly_null('value')
            else:
                new.value = payload['value']
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#ServiceError'

    def __repr__(self):
        attrs = []
        for attr in ['message', 'value']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ServiceError):
            return self.__dict__ == other.__dict__
        return False


class GetAllProductsResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 products=None):
        super().__init__()
        self.products = products

    def _to_payload(self):
        payload = {}
        if self.products is None:
            if self.is_explicitly_null('products'):
                payload['products'] = None
        else:
            payload['products'] = {k: v._to_payload() for k, v in self.products.items()}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'products' in payload:
            if payload['products'] is None:
                new.set_explicitly_null('products')
            else:
                new.products = {k: Product._from_payload(v) for k,v in payload['products'].items()}
        return new

    @classmethod
    def _model_name(cls):
        return 'awstest#GetAllProductsResponse'

    def __repr__(self):
        attrs = []
        for attr in ['products']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetAllProductsResponse):
            return self.__dict__ == other.__dict__
        return False


class GetAllProductsRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetAllProductsRequest):
            return self.__dict__ == other.__dict__
        return False


SHAPE_INDEX = rpc.ShapeIndex([
    Pair,
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


