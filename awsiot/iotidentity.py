# Copyright Amazon.com, Inc. or its affiliates.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot
import concurrent.futures
import typing

class IotIdentityClient(awsiot.MqttServiceClient):

    def publish_create_certificate_from_csr(self, request, qos):
        # type: (CreateCertificateFromCsrRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `CreateCertificateFromCsrRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """

        return self._publish_operation(
            topic='$aws/certificates/create-from-csr/json',
            qos=qos,
            payload=request.to_payload())

    def publish_create_keys_and_certificate(self, request, qos):
        # type: (CreateKeysAndCertificateRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `CreateKeysAndCertificateRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """

        return self._publish_operation(
            topic='$aws/certificates/create/json',
            qos=qos,
            payload=None)

    def publish_register_thing(self, request, qos):
        # type: (RegisterThingRequest, int) -> concurrent.futures.Future
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `RegisterThingRequest` instance.
        qos     - The Quality of Service guarantee of this message

        Returns a concurrent.futures.Future, whose result will be None if the
        request is successfully published. The Future's result will be an
        exception if the request cannot be published.
        """
        if not request.template_name:
            raise ValueError("request.template_name is required")

        return self._publish_operation(
            topic='$aws/provisioning-templates/{0.template_name}/provision/json'.format(request),
            qos=qos,
            payload=request.to_payload())

    def subscribe_to_create_certificate_from_csr_accepted(self, request, qos, callback):
        # type: (CreateCertificateFromCsrSubscriptionRequest, int, typing.Callable[[CreateCertificateFromCsrResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `CreateCertificateFromCsrSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `CreateCertificateFromCsrResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/certificates/create-from-csr/json/accepted',
            qos=qos,
            callback=callback,
            payload_to_class_fn=CreateCertificateFromCsrResponse.from_payload)

    def subscribe_to_create_certificate_from_csr_rejected(self, request, qos, callback):
        # type: (CreateCertificateFromCsrSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `CreateCertificateFromCsrSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/certificates/create-from-csr/json/rejected',
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_create_keys_and_certificate_accepted(self, request, qos, callback):
        # type: (CreateKeysAndCertificateSubscriptionRequest, int, typing.Callable[[CreateKeysAndCertificateResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `CreateKeysAndCertificateSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `CreateKeysAndCertificateResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/certificates/create/json/accepted',
            qos=qos,
            callback=callback,
            payload_to_class_fn=CreateKeysAndCertificateResponse.from_payload)

    def subscribe_to_create_keys_and_certificate_rejected(self, request, qos, callback):
        # type: (CreateKeysAndCertificateSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `CreateKeysAndCertificateSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/certificates/create/json/rejected',
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

    def subscribe_to_register_thing_accepted(self, request, qos, callback):
        # type: (RegisterThingSubscriptionRequest, int, typing.Callable[[RegisterThingResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `RegisterThingSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `RegisterThingResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.template_name:
            raise ValueError("request.template_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/provisioning-templates/{0.template_name}/provision/json/accepted'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=RegisterThingResponse.from_payload)

    def subscribe_to_register_thing_rejected(self, request, qos, callback):
        # type: (RegisterThingSubscriptionRequest, int, typing.Callable[[ErrorResponse], None]) -> typing.Tuple[concurrent.futures.Future, str]
        """
        API Docs: https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#fleet-provision-api

        Parameters:
        request - `RegisterThingSubscriptionRequest` instance.
        qos     - The Quality of Service guarantee of this message
        callback - Callback to invoke each time the event is received.
                The callback should take 1 argument of type `ErrorResponse`.
                The callback is not expected to return anything.

        Returns two values immediately. The first is a `concurrent.futures.Future`
        which will contain a result of `None` when the server has acknowledged
        the subscription, or an exception if the subscription fails. The second
        value is a topic which may be passed to `unsubscribe()` to stop
        receiving messages. Note that messages may arrive before the
        subscription is acknowledged.
        """
        if not request.template_name:
            raise ValueError("request.template_name is required")

        if not callable(callback):
            raise ValueError("callback is required")

        return self._subscribe_operation(
            topic='$aws/provisioning-templates/{0.template_name}/provision/json/rejected'.format(request),
            qos=qos,
            callback=callback,
            payload_to_class_fn=ErrorResponse.from_payload)

class CreateCertificateFromCsrRequest(awsiot.ModeledClass):
    r"""
    Attributes:
        * *certificate_signing_request* (``str``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['certificate_signing_request']

    def __init__(self, *args, **kwargs):
        r"""Initializes a CreateCertificateFromCsrRequest instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *certificate_signing_request* (``str``)
        """

        self.certificate_signing_request = kwargs.get('certificate_signing_request')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['certificate_signing_request'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.certificate_signing_request is not None:
            payload['certificateSigningRequest'] = self.certificate_signing_request
        return payload

class CreateCertificateFromCsrResponse(awsiot.ModeledClass):
    r"""
    Attributes:
        * *certificate_id* (``str``)
        * *certificate_ownership_token* (``str``)
        * *certificate_pem* (``str``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['certificate_id', 'certificate_ownership_token', 'certificate_pem']

    def __init__(self, *args, **kwargs):
        r"""Initializes a CreateCertificateFromCsrResponse instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *certificate_id* (``str``)
            * *certificate_ownership_token* (``str``)
            * *certificate_pem* (``str``)
        """

        self.certificate_id = kwargs.get('certificate_id')
        self.certificate_ownership_token = kwargs.get('certificate_ownership_token')
        self.certificate_pem = kwargs.get('certificate_pem')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['certificate_id', 'certificate_ownership_token', 'certificate_pem'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> CreateCertificateFromCsrResponse
        new = cls()
        val = payload.get('certificateId')
        if val is not None:
            new.certificate_id = val
        val = payload.get('certificateOwnershipToken')
        if val is not None:
            new.certificate_ownership_token = val
        val = payload.get('certificatePem')
        if val is not None:
            new.certificate_pem = val
        return new

class CreateCertificateFromCsrSubscriptionRequest(awsiot.ModeledClass):
    r"""
    Attributes:

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = []

    def __init__(self, *args, **kwargs):
        r"""Initializes a CreateCertificateFromCsrSubscriptionRequest instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
        """

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip([], args):
            setattr(self, key, val)

class CreateKeysAndCertificateRequest(awsiot.ModeledClass):
    r"""
    Attributes:

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = []

    def __init__(self, *args, **kwargs):
        r"""Initializes a CreateKeysAndCertificateRequest instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
        """

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip([], args):
            setattr(self, key, val)

class CreateKeysAndCertificateResponse(awsiot.ModeledClass):
    r"""
    Attributes:
        * *certificate_id* (``str``)
        * *certificate_ownership_token* (``str``)
        * *certificate_pem* (``str``)
        * *private_key* (``str``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['certificate_id', 'certificate_ownership_token', 'certificate_pem', 'private_key']

    def __init__(self, *args, **kwargs):
        r"""Initializes a CreateKeysAndCertificateResponse instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *certificate_id* (``str``)
            * *certificate_ownership_token* (``str``)
            * *certificate_pem* (``str``)
            * *private_key* (``str``)
        """

        self.certificate_id = kwargs.get('certificate_id')
        self.certificate_ownership_token = kwargs.get('certificate_ownership_token')
        self.certificate_pem = kwargs.get('certificate_pem')
        self.private_key = kwargs.get('private_key')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['certificate_id', 'certificate_ownership_token', 'certificate_pem', 'private_key'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> CreateKeysAndCertificateResponse
        new = cls()
        val = payload.get('certificateId')
        if val is not None:
            new.certificate_id = val
        val = payload.get('certificateOwnershipToken')
        if val is not None:
            new.certificate_ownership_token = val
        val = payload.get('certificatePem')
        if val is not None:
            new.certificate_pem = val
        val = payload.get('privateKey')
        if val is not None:
            new.private_key = val
        return new

class CreateKeysAndCertificateSubscriptionRequest(awsiot.ModeledClass):
    r"""
    Attributes:

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = []

    def __init__(self, *args, **kwargs):
        r"""Initializes a CreateKeysAndCertificateSubscriptionRequest instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
        """

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip([], args):
            setattr(self, key, val)

class ErrorResponse(awsiot.ModeledClass):
    r"""
    Attributes:
        * *error_code* (``str``)
        * *error_message* (``str``)
        * *status_code* (``int``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['error_code', 'error_message', 'status_code']

    def __init__(self, *args, **kwargs):
        r"""Initializes a ErrorResponse instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *error_code* (``str``)
            * *error_message* (``str``)
            * *status_code* (``int``)
        """

        self.error_code = kwargs.get('error_code')
        self.error_message = kwargs.get('error_message')
        self.status_code = kwargs.get('status_code')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['error_code', 'error_message', 'status_code'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> ErrorResponse
        new = cls()
        val = payload.get('errorCode')
        if val is not None:
            new.error_code = val
        val = payload.get('errorMessage')
        if val is not None:
            new.error_message = val
        val = payload.get('statusCode')
        if val is not None:
            new.status_code = val
        return new

class RegisterThingRequest(awsiot.ModeledClass):
    r"""
    Attributes:
        * *certificate_ownership_token* (``str``)
        * *parameters* (``typing.Dict[str, str]``)
        * *template_name* (``str``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['certificate_ownership_token', 'parameters', 'template_name']

    def __init__(self, *args, **kwargs):
        r"""Initializes a RegisterThingRequest instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *certificate_ownership_token* (``str``)
            * *parameters* (``typing.Dict[str, str]``)
            * *template_name* (``str``)
        """

        self.certificate_ownership_token = kwargs.get('certificate_ownership_token')
        self.parameters = kwargs.get('parameters')
        self.template_name = kwargs.get('template_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['certificate_ownership_token', 'parameters', 'template_name'], args):
            setattr(self, key, val)

    def to_payload(self):
        # type: () -> typing.Dict[str, typing.Any]
        payload = {} # type: typing.Dict[str, typing.Any]
        if self.certificate_ownership_token is not None:
            payload['certificateOwnershipToken'] = self.certificate_ownership_token
        if self.parameters is not None:
            payload['parameters'] = self.parameters
        return payload

class RegisterThingResponse(awsiot.ModeledClass):
    r"""
    Attributes:
        * *device_configuration* (``typing.Dict[str, str]``)
        * *thing_name* (``str``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['device_configuration', 'thing_name']

    def __init__(self, *args, **kwargs):
        r"""Initializes a RegisterThingResponse instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *device_configuration* (``typing.Dict[str, str]``)
            * *thing_name* (``str``)
        """

        self.device_configuration = kwargs.get('device_configuration')
        self.thing_name = kwargs.get('thing_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['device_configuration', 'thing_name'], args):
            setattr(self, key, val)

    @classmethod
    def from_payload(cls, payload):
        # type: (typing.Dict[str, typing.Any]) -> RegisterThingResponse
        new = cls()
        val = payload.get('deviceConfiguration')
        if val is not None:
            new.device_configuration = val
        val = payload.get('thingName')
        if val is not None:
            new.thing_name = val
        return new

class RegisterThingSubscriptionRequest(awsiot.ModeledClass):
    r"""
    Attributes:
        * *template_name* (``str``)

    All attributes are None by default, and may be set by keyword in the constructor.
    """

    __slots__ = ['template_name']

    def __init__(self, *args, **kwargs):
        r"""Initializes a RegisterThingSubscriptionRequest instance

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *template_name* (``str``)
        """

        self.template_name = kwargs.get('template_name')

        # for backwards compatibility, read any arguments that used to be accepted by position
        for key, val in zip(['template_name'], args):
            setattr(self, key, val)

