# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot.eventstreamrpc as rpc
import base64
import datetime
import typing


class GreengrassCoreIPCError(rpc.ErrorShape):
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


class SystemResourceLimits(rpc.Shape):
    """
    SystemResourceLimits

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        memory: 
        cpus: 

    Attributes:
        memory: 
        cpus: 
    """

    def __init__(self, *,
                 memory: typing.Optional[int] = None,
                 cpus: typing.Optional[float] = None):
        super().__init__()
        self.memory = memory  # type: typing.Optional[int]
        self.cpus = cpus  # type: typing.Optional[float]

    def set_memory(self, memory: int):
        self.memory = memory
        return self

    def set_cpus(self, cpus: float):
        self.cpus = cpus
        return self


    def _to_payload(self):
        payload = {}
        if self.memory is not None:
            payload['memory'] = self.memory
        if self.cpus is not None:
            payload['cpus'] = self.cpus
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'memory' in payload:
            new.memory = int(payload['memory'])
        if 'cpus' in payload:
            new.cpus = float(payload['cpus'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SystemResourceLimits'

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


class MetricUnitType:
    """
    MetricUnitType enum
    """

    BYTES = 'BYTES'
    BYTES_PER_SECOND = 'BYTES_PER_SECOND'
    COUNT = 'COUNT'
    COUNT_PER_SECOND = 'COUNT_PER_SECOND'
    MEGABYTES = 'MEGABYTES'
    SECONDS = 'SECONDS'


class MessageContext(rpc.Shape):
    """
    MessageContext

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic: 

    Attributes:
        topic: 
    """

    def __init__(self, *,
                 topic: typing.Optional[str] = None):
        super().__init__()
        self.topic = topic  # type: typing.Optional[str]

    def set_topic(self, topic: str):
        self.topic = topic
        return self


    def _to_payload(self):
        payload = {}
        if self.topic is not None:
            payload['topic'] = self.topic
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topic' in payload:
            new.topic = payload['topic']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#MessageContext'

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


class ValidateConfigurationUpdateEvent(rpc.Shape):
    """
    ValidateConfigurationUpdateEvent

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        configuration: 
        deployment_id: 

    Attributes:
        configuration: 
        deployment_id: 
    """

    def __init__(self, *,
                 configuration: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 deployment_id: typing.Optional[str] = None):
        super().__init__()
        self.configuration = configuration  # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.deployment_id = deployment_id  # type: typing.Optional[str]

    def set_configuration(self, configuration: typing.Dict[str, typing.Any]):
        self.configuration = configuration
        return self

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self


    def _to_payload(self):
        payload = {}
        if self.configuration is not None:
            payload['configuration'] = self.configuration
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'configuration' in payload:
            new.configuration = payload['configuration']
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateConfigurationUpdateEvent'

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


class RunWithInfo(rpc.Shape):
    """
    RunWithInfo

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        posix_user: 
        windows_user: 
        system_resource_limits: 

    Attributes:
        posix_user: 
        windows_user: 
        system_resource_limits: 
    """

    def __init__(self, *,
                 posix_user: typing.Optional[str] = None,
                 windows_user: typing.Optional[str] = None,
                 system_resource_limits: typing.Optional[SystemResourceLimits] = None):
        super().__init__()
        self.posix_user = posix_user  # type: typing.Optional[str]
        self.windows_user = windows_user  # type: typing.Optional[str]
        self.system_resource_limits = system_resource_limits  # type: typing.Optional[SystemResourceLimits]

    def set_posix_user(self, posix_user: str):
        self.posix_user = posix_user
        return self

    def set_windows_user(self, windows_user: str):
        self.windows_user = windows_user
        return self

    def set_system_resource_limits(self, system_resource_limits: SystemResourceLimits):
        self.system_resource_limits = system_resource_limits
        return self


    def _to_payload(self):
        payload = {}
        if self.posix_user is not None:
            payload['posixUser'] = self.posix_user
        if self.windows_user is not None:
            payload['windowsUser'] = self.windows_user
        if self.system_resource_limits is not None:
            payload['systemResourceLimits'] = self.system_resource_limits._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'posixUser' in payload:
            new.posix_user = payload['posixUser']
        if 'windowsUser' in payload:
            new.windows_user = payload['windowsUser']
        if 'systemResourceLimits' in payload:
            new.system_resource_limits = SystemResourceLimits._from_payload(payload['systemResourceLimits'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#RunWithInfo'

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


class PreComponentUpdateEvent(rpc.Shape):
    """
    PreComponentUpdateEvent

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment_id: 
        is_ggc_restarting: 

    Attributes:
        deployment_id: 
        is_ggc_restarting: 
    """

    def __init__(self, *,
                 deployment_id: typing.Optional[str] = None,
                 is_ggc_restarting: typing.Optional[bool] = None):
        super().__init__()
        self.deployment_id = deployment_id  # type: typing.Optional[str]
        self.is_ggc_restarting = is_ggc_restarting  # type: typing.Optional[bool]

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self

    def set_is_ggc_restarting(self, is_ggc_restarting: bool):
        self.is_ggc_restarting = is_ggc_restarting
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        if self.is_ggc_restarting is not None:
            payload['isGgcRestarting'] = self.is_ggc_restarting
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        if 'isGgcRestarting' in payload:
            new.is_ggc_restarting = payload['isGgcRestarting']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PreComponentUpdateEvent'

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


class PostComponentUpdateEvent(rpc.Shape):
    """
    PostComponentUpdateEvent

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment_id: 

    Attributes:
        deployment_id: 
    """

    def __init__(self, *,
                 deployment_id: typing.Optional[str] = None):
        super().__init__()
        self.deployment_id = deployment_id  # type: typing.Optional[str]

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PostComponentUpdateEvent'

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


class MQTTMessage(rpc.Shape):
    """
    MQTTMessage

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic_name: 
        payload: 

    Attributes:
        topic_name: 
        payload: 
    """

    def __init__(self, *,
                 topic_name: typing.Optional[str] = None,
                 payload: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        self.topic_name = topic_name  # type: typing.Optional[str]
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload  # type: typing.Optional[bytes]

    def set_topic_name(self, topic_name: str):
        self.topic_name = topic_name
        return self

    def set_payload(self, payload: typing.Union[bytes, str]):
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload
        return self


    def _to_payload(self):
        payload = {}
        if self.topic_name is not None:
            payload['topicName'] = self.topic_name
        if self.payload is not None:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            new.topic_name = payload['topicName']
        if 'payload' in payload:
            new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#MQTTMessage'

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


class MQTTCredential(rpc.Shape):
    """
    MQTTCredential

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_id: 
        certificate_pem: 
        username: 
        password: 

    Attributes:
        client_id: 
        certificate_pem: 
        username: 
        password: 
    """

    def __init__(self, *,
                 client_id: typing.Optional[str] = None,
                 certificate_pem: typing.Optional[str] = None,
                 username: typing.Optional[str] = None,
                 password: typing.Optional[str] = None):
        super().__init__()
        self.client_id = client_id  # type: typing.Optional[str]
        self.certificate_pem = certificate_pem  # type: typing.Optional[str]
        self.username = username  # type: typing.Optional[str]
        self.password = password  # type: typing.Optional[str]

    def set_client_id(self, client_id: str):
        self.client_id = client_id
        return self

    def set_certificate_pem(self, certificate_pem: str):
        self.certificate_pem = certificate_pem
        return self

    def set_username(self, username: str):
        self.username = username
        return self

    def set_password(self, password: str):
        self.password = password
        return self


    def _to_payload(self):
        payload = {}
        if self.client_id is not None:
            payload['clientId'] = self.client_id
        if self.certificate_pem is not None:
            payload['certificatePem'] = self.certificate_pem
        if self.username is not None:
            payload['username'] = self.username
        if self.password is not None:
            payload['password'] = self.password
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'clientId' in payload:
            new.client_id = payload['clientId']
        if 'certificatePem' in payload:
            new.certificate_pem = payload['certificatePem']
        if 'username' in payload:
            new.username = payload['username']
        if 'password' in payload:
            new.password = payload['password']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#MQTTCredential'

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


class Metric(rpc.Shape):
    """
    Metric

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        name: 
        unit: MetricUnitType enum value
        value: 

    Attributes:
        name: 
        unit: MetricUnitType enum value
        value: 
    """

    def __init__(self, *,
                 name: typing.Optional[str] = None,
                 unit: typing.Optional[str] = None,
                 value: typing.Optional[float] = None):
        super().__init__()
        self.name = name  # type: typing.Optional[str]
        self.unit = unit  # type: typing.Optional[str]
        self.value = value  # type: typing.Optional[float]

    def set_name(self, name: str):
        self.name = name
        return self

    def set_unit(self, unit: str):
        self.unit = unit
        return self

    def set_value(self, value: float):
        self.value = value
        return self


    def _to_payload(self):
        payload = {}
        if self.name is not None:
            payload['name'] = self.name
        if self.unit is not None:
            payload['unit'] = self.unit
        if self.value is not None:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'name' in payload:
            new.name = payload['name']
        if 'unit' in payload:
            new.unit = payload['unit']
        if 'value' in payload:
            new.value = float(payload['value'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#Metric'

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


class LifecycleState:
    """
    LifecycleState enum
    """

    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'
    NEW = 'NEW'
    FINISHED = 'FINISHED'
    INSTALLED = 'INSTALLED'
    BROKEN = 'BROKEN'
    STARTING = 'STARTING'
    STOPPING = 'STOPPING'


class JsonMessage(rpc.Shape):
    """
    JsonMessage

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 
        context: The context is ignored if used in PublishMessage.

    Attributes:
        message: 
        context: The context is ignored if used in PublishMessage.
    """

    def __init__(self, *,
                 message: typing.Optional[typing.Dict[str, typing.Any]] = None,
                 context: typing.Optional[MessageContext] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[typing.Dict[str, typing.Any]]
        self.context = context  # type: typing.Optional[MessageContext]

    def set_message(self, message: typing.Dict[str, typing.Any]):
        self.message = message
        return self

    def set_context(self, context: MessageContext):
        self.context = context
        return self


    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        if self.context is not None:
            payload['context'] = self.context._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        if 'context' in payload:
            new.context = MessageContext._from_payload(payload['context'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#JsonMessage'

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


class DeploymentStatus:
    """
    DeploymentStatus enum
    """

    QUEUED = 'QUEUED'
    IN_PROGRESS = 'IN_PROGRESS'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class ConfigurationValidityStatus:
    """
    ConfigurationValidityStatus enum
    """

    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'


class ConfigurationUpdateEvent(rpc.Shape):
    """
    ConfigurationUpdateEvent

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 
        key_path: 

    Attributes:
        component_name: 
        key_path: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None,
                 key_path: typing.Optional[typing.List[str]] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]
        self.key_path = key_path  # type: typing.Optional[typing.List[str]]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self

    def set_key_path(self, key_path: typing.List[str]):
        self.key_path = key_path
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        if self.key_path is not None:
            payload['keyPath'] = self.key_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        if 'keyPath' in payload:
            new.key_path = payload['keyPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConfigurationUpdateEvent'

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


class CertificateUpdate(rpc.Shape):
    """
    CertificateUpdate

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        private_key: 
        public_key: 
        certificate: 
        ca_certificates: 

    Attributes:
        private_key: 
        public_key: 
        certificate: 
        ca_certificates: 
    """

    def __init__(self, *,
                 private_key: typing.Optional[str] = None,
                 public_key: typing.Optional[str] = None,
                 certificate: typing.Optional[str] = None,
                 ca_certificates: typing.Optional[typing.List[str]] = None):
        super().__init__()
        self.private_key = private_key  # type: typing.Optional[str]
        self.public_key = public_key  # type: typing.Optional[str]
        self.certificate = certificate  # type: typing.Optional[str]
        self.ca_certificates = ca_certificates  # type: typing.Optional[typing.List[str]]

    def set_private_key(self, private_key: str):
        self.private_key = private_key
        return self

    def set_public_key(self, public_key: str):
        self.public_key = public_key
        return self

    def set_certificate(self, certificate: str):
        self.certificate = certificate
        return self

    def set_ca_certificates(self, ca_certificates: typing.List[str]):
        self.ca_certificates = ca_certificates
        return self


    def _to_payload(self):
        payload = {}
        if self.private_key is not None:
            payload['privateKey'] = self.private_key
        if self.public_key is not None:
            payload['publicKey'] = self.public_key
        if self.certificate is not None:
            payload['certificate'] = self.certificate
        if self.ca_certificates is not None:
            payload['caCertificates'] = self.ca_certificates
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'privateKey' in payload:
            new.private_key = payload['privateKey']
        if 'publicKey' in payload:
            new.public_key = payload['publicKey']
        if 'certificate' in payload:
            new.certificate = payload['certificate']
        if 'caCertificates' in payload:
            new.ca_certificates = payload['caCertificates']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CertificateUpdate'

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


class CertificateType:
    """
    CertificateType enum
    """

    SERVER = 'SERVER'


class BinaryMessage(rpc.Shape):
    """
    BinaryMessage

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 
        context: The context is ignored if used in PublishMessage.

    Attributes:
        message: 
        context: The context is ignored if used in PublishMessage.
    """

    def __init__(self, *,
                 message: typing.Optional[typing.Union[bytes, str]] = None,
                 context: typing.Optional[MessageContext] = None):
        super().__init__()
        if message is not None and isinstance(message, str):
            message = message.encode('utf-8')
        self.message = message  # type: typing.Optional[bytes]
        self.context = context  # type: typing.Optional[MessageContext]

    def set_message(self, message: typing.Union[bytes, str]):
        if message is not None and isinstance(message, str):
            message = message.encode('utf-8')
        self.message = message
        return self

    def set_context(self, context: MessageContext):
        self.context = context
        return self


    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = base64.b64encode(self.message).decode()
        if self.context is not None:
            payload['context'] = self.context._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = base64.b64decode(payload['message'])
        if 'context' in payload:
            new.context = MessageContext._from_payload(payload['context'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#BinaryMessage'

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


class ValidateConfigurationUpdateEvents(rpc.Shape):
    """
    ValidateConfigurationUpdateEvents is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        validate_configuration_update_event: 

    Attributes:
        validate_configuration_update_event: 
    """

    def __init__(self, *,
                 validate_configuration_update_event: typing.Optional[ValidateConfigurationUpdateEvent] = None):
        super().__init__()
        self.validate_configuration_update_event = validate_configuration_update_event  # type: typing.Optional[ValidateConfigurationUpdateEvent]

    def set_validate_configuration_update_event(self, validate_configuration_update_event: ValidateConfigurationUpdateEvent):
        self.validate_configuration_update_event = validate_configuration_update_event
        return self


    def _to_payload(self):
        payload = {}
        if self.validate_configuration_update_event is not None:
            payload['validateConfigurationUpdateEvent'] = self.validate_configuration_update_event._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'validateConfigurationUpdateEvent' in payload:
            new.validate_configuration_update_event = ValidateConfigurationUpdateEvent._from_payload(payload['validateConfigurationUpdateEvent'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateConfigurationUpdateEvents'

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


class SubscriptionResponseMessage(rpc.Shape):
    """
    SubscriptionResponseMessage is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        json_message: 
        binary_message: 

    Attributes:
        json_message: 
        binary_message: 
    """

    def __init__(self, *,
                 json_message: typing.Optional[JsonMessage] = None,
                 binary_message: typing.Optional[BinaryMessage] = None):
        super().__init__()
        self.json_message = json_message  # type: typing.Optional[JsonMessage]
        self.binary_message = binary_message  # type: typing.Optional[BinaryMessage]

    def set_json_message(self, json_message: JsonMessage):
        self.json_message = json_message
        return self

    def set_binary_message(self, binary_message: BinaryMessage):
        self.binary_message = binary_message
        return self


    def _to_payload(self):
        payload = {}
        if self.json_message is not None:
            payload['jsonMessage'] = self.json_message._to_payload()
        if self.binary_message is not None:
            payload['binaryMessage'] = self.binary_message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'jsonMessage' in payload:
            new.json_message = JsonMessage._from_payload(payload['jsonMessage'])
        if 'binaryMessage' in payload:
            new.binary_message = BinaryMessage._from_payload(payload['binaryMessage'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscriptionResponseMessage'

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


class SecretValue(rpc.Shape):
    """
    SecretValue is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        secret_string: 
        secret_binary: 

    Attributes:
        secret_string: 
        secret_binary: 
    """

    def __init__(self, *,
                 secret_string: typing.Optional[str] = None,
                 secret_binary: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        self.secret_string = secret_string  # type: typing.Optional[str]
        if secret_binary is not None and isinstance(secret_binary, str):
            secret_binary = secret_binary.encode('utf-8')
        self.secret_binary = secret_binary  # type: typing.Optional[bytes]

    def set_secret_string(self, secret_string: str):
        self.secret_string = secret_string
        return self

    def set_secret_binary(self, secret_binary: typing.Union[bytes, str]):
        if secret_binary is not None and isinstance(secret_binary, str):
            secret_binary = secret_binary.encode('utf-8')
        self.secret_binary = secret_binary
        return self


    def _to_payload(self):
        payload = {}
        if self.secret_string is not None:
            payload['secretString'] = self.secret_string
        if self.secret_binary is not None:
            payload['secretBinary'] = base64.b64encode(self.secret_binary).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'secretString' in payload:
            new.secret_string = payload['secretString']
        if 'secretBinary' in payload:
            new.secret_binary = base64.b64decode(payload['secretBinary'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SecretValue'

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


class RequestStatus:
    """
    RequestStatus enum
    """

    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class ReportedLifecycleState:
    """
    ReportedLifecycleState enum
    """

    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'


class ReceiveMode:
    """
    ReceiveMode enum
    """

    RECEIVE_ALL_MESSAGES = 'RECEIVE_ALL_MESSAGES'
    RECEIVE_MESSAGES_FROM_OTHERS = 'RECEIVE_MESSAGES_FROM_OTHERS'


class QOS:
    """
    QOS enum
    """

    AT_MOST_ONCE = '0'
    AT_LEAST_ONCE = '1'


class PublishMessage(rpc.Shape):
    """
    PublishMessage is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        json_message: 
        binary_message: 

    Attributes:
        json_message: 
        binary_message: 
    """

    def __init__(self, *,
                 json_message: typing.Optional[JsonMessage] = None,
                 binary_message: typing.Optional[BinaryMessage] = None):
        super().__init__()
        self.json_message = json_message  # type: typing.Optional[JsonMessage]
        self.binary_message = binary_message  # type: typing.Optional[BinaryMessage]

    def set_json_message(self, json_message: JsonMessage):
        self.json_message = json_message
        return self

    def set_binary_message(self, binary_message: BinaryMessage):
        self.binary_message = binary_message
        return self


    def _to_payload(self):
        payload = {}
        if self.json_message is not None:
            payload['jsonMessage'] = self.json_message._to_payload()
        if self.binary_message is not None:
            payload['binaryMessage'] = self.binary_message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'jsonMessage' in payload:
            new.json_message = JsonMessage._from_payload(payload['jsonMessage'])
        if 'binaryMessage' in payload:
            new.binary_message = BinaryMessage._from_payload(payload['binaryMessage'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishMessage'

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


class LocalDeployment(rpc.Shape):
    """
    LocalDeployment

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment_id: 
        status: DeploymentStatus enum value

    Attributes:
        deployment_id: 
        status: DeploymentStatus enum value
    """

    def __init__(self, *,
                 deployment_id: typing.Optional[str] = None,
                 status: typing.Optional[str] = None):
        super().__init__()
        self.deployment_id = deployment_id  # type: typing.Optional[str]
        self.status = status  # type: typing.Optional[str]

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self

    def set_status(self, status: str):
        self.status = status
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        if self.status is not None:
            payload['status'] = self.status
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        if 'status' in payload:
            new.status = payload['status']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#LocalDeployment'

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


class IoTCoreMessage(rpc.Shape):
    """
    IoTCoreMessage is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[MQTTMessage] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[MQTTMessage]

    def set_message(self, message: MQTTMessage):
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
            new.message = MQTTMessage._from_payload(payload['message'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#IoTCoreMessage'

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


class CredentialDocument(rpc.Shape):
    """
    CredentialDocument is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        mqtt_credential: 

    Attributes:
        mqtt_credential: 
    """

    def __init__(self, *,
                 mqtt_credential: typing.Optional[MQTTCredential] = None):
        super().__init__()
        self.mqtt_credential = mqtt_credential  # type: typing.Optional[MQTTCredential]

    def set_mqtt_credential(self, mqtt_credential: MQTTCredential):
        self.mqtt_credential = mqtt_credential
        return self


    def _to_payload(self):
        payload = {}
        if self.mqtt_credential is not None:
            payload['mqttCredential'] = self.mqtt_credential._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'mqttCredential' in payload:
            new.mqtt_credential = MQTTCredential._from_payload(payload['mqttCredential'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CredentialDocument'

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


class ConfigurationValidityReport(rpc.Shape):
    """
    ConfigurationValidityReport

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        status: ConfigurationValidityStatus enum value
        deployment_id: 
        message: 

    Attributes:
        status: ConfigurationValidityStatus enum value
        deployment_id: 
        message: 
    """

    def __init__(self, *,
                 status: typing.Optional[str] = None,
                 deployment_id: typing.Optional[str] = None,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.status = status  # type: typing.Optional[str]
        self.deployment_id = deployment_id  # type: typing.Optional[str]
        self.message = message  # type: typing.Optional[str]

    def set_status(self, status: str):
        self.status = status
        return self

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self

    def set_message(self, message: str):
        self.message = message
        return self


    def _to_payload(self):
        payload = {}
        if self.status is not None:
            payload['status'] = self.status
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'status' in payload:
            new.status = payload['status']
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConfigurationValidityReport'

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


class ConfigurationUpdateEvents(rpc.Shape):
    """
    ConfigurationUpdateEvents is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        configuration_update_event: 

    Attributes:
        configuration_update_event: 
    """

    def __init__(self, *,
                 configuration_update_event: typing.Optional[ConfigurationUpdateEvent] = None):
        super().__init__()
        self.configuration_update_event = configuration_update_event  # type: typing.Optional[ConfigurationUpdateEvent]

    def set_configuration_update_event(self, configuration_update_event: ConfigurationUpdateEvent):
        self.configuration_update_event = configuration_update_event
        return self


    def _to_payload(self):
        payload = {}
        if self.configuration_update_event is not None:
            payload['configurationUpdateEvent'] = self.configuration_update_event._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'configurationUpdateEvent' in payload:
            new.configuration_update_event = ConfigurationUpdateEvent._from_payload(payload['configurationUpdateEvent'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConfigurationUpdateEvents'

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


class ComponentUpdatePolicyEvents(rpc.Shape):
    """
    ComponentUpdatePolicyEvents is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        pre_update_event: 
        post_update_event: 

    Attributes:
        pre_update_event: 
        post_update_event: 
    """

    def __init__(self, *,
                 pre_update_event: typing.Optional[PreComponentUpdateEvent] = None,
                 post_update_event: typing.Optional[PostComponentUpdateEvent] = None):
        super().__init__()
        self.pre_update_event = pre_update_event  # type: typing.Optional[PreComponentUpdateEvent]
        self.post_update_event = post_update_event  # type: typing.Optional[PostComponentUpdateEvent]

    def set_pre_update_event(self, pre_update_event: PreComponentUpdateEvent):
        self.pre_update_event = pre_update_event
        return self

    def set_post_update_event(self, post_update_event: PostComponentUpdateEvent):
        self.post_update_event = post_update_event
        return self


    def _to_payload(self):
        payload = {}
        if self.pre_update_event is not None:
            payload['preUpdateEvent'] = self.pre_update_event._to_payload()
        if self.post_update_event is not None:
            payload['postUpdateEvent'] = self.post_update_event._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'preUpdateEvent' in payload:
            new.pre_update_event = PreComponentUpdateEvent._from_payload(payload['preUpdateEvent'])
        if 'postUpdateEvent' in payload:
            new.post_update_event = PostComponentUpdateEvent._from_payload(payload['postUpdateEvent'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ComponentUpdatePolicyEvents'

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


class ComponentDetails(rpc.Shape):
    """
    ComponentDetails

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 
        version: 
        state: LifecycleState enum value
        configuration: 

    Attributes:
        component_name: 
        version: 
        state: LifecycleState enum value
        configuration: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None,
                 version: typing.Optional[str] = None,
                 state: typing.Optional[str] = None,
                 configuration: typing.Optional[typing.Dict[str, typing.Any]] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]
        self.version = version  # type: typing.Optional[str]
        self.state = state  # type: typing.Optional[str]
        self.configuration = configuration  # type: typing.Optional[typing.Dict[str, typing.Any]]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self

    def set_version(self, version: str):
        self.version = version
        return self

    def set_state(self, state: str):
        self.state = state
        return self

    def set_configuration(self, configuration: typing.Dict[str, typing.Any]):
        self.configuration = configuration
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        if self.version is not None:
            payload['version'] = self.version
        if self.state is not None:
            payload['state'] = self.state
        if self.configuration is not None:
            payload['configuration'] = self.configuration
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        if 'version' in payload:
            new.version = payload['version']
        if 'state' in payload:
            new.state = payload['state']
        if 'configuration' in payload:
            new.configuration = payload['configuration']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ComponentDetails'

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


class ClientDeviceCredential(rpc.Shape):
    """
    ClientDeviceCredential is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        client_device_certificate: 

    Attributes:
        client_device_certificate: 
    """

    def __init__(self, *,
                 client_device_certificate: typing.Optional[str] = None):
        super().__init__()
        self.client_device_certificate = client_device_certificate  # type: typing.Optional[str]

    def set_client_device_certificate(self, client_device_certificate: str):
        self.client_device_certificate = client_device_certificate
        return self


    def _to_payload(self):
        payload = {}
        if self.client_device_certificate is not None:
            payload['clientDeviceCertificate'] = self.client_device_certificate
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'clientDeviceCertificate' in payload:
            new.client_device_certificate = payload['clientDeviceCertificate']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ClientDeviceCredential'

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


class CertificateUpdateEvent(rpc.Shape):
    """
    CertificateUpdateEvent is a "tagged union" class.

    When sending, only one of the attributes may be set.
    When receiving, only one of the attributes will be set.
    All other attributes will be None.

    Keyword Args:
        certificate_update: 

    Attributes:
        certificate_update: 
    """

    def __init__(self, *,
                 certificate_update: typing.Optional[CertificateUpdate] = None):
        super().__init__()
        self.certificate_update = certificate_update  # type: typing.Optional[CertificateUpdate]

    def set_certificate_update(self, certificate_update: CertificateUpdate):
        self.certificate_update = certificate_update
        return self


    def _to_payload(self):
        payload = {}
        if self.certificate_update is not None:
            payload['certificateUpdate'] = self.certificate_update._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'certificateUpdate' in payload:
            new.certificate_update = CertificateUpdate._from_payload(payload['certificateUpdate'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CertificateUpdateEvent'

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


class CertificateOptions(rpc.Shape):
    """
    CertificateOptions

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        certificate_type: CertificateType enum value

    Attributes:
        certificate_type: CertificateType enum value
    """

    def __init__(self, *,
                 certificate_type: typing.Optional[str] = None):
        super().__init__()
        self.certificate_type = certificate_type  # type: typing.Optional[str]

    def set_certificate_type(self, certificate_type: str):
        self.certificate_type = certificate_type
        return self


    def _to_payload(self):
        payload = {}
        if self.certificate_type is not None:
            payload['certificateType'] = self.certificate_type
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'certificateType' in payload:
            new.certificate_type = payload['certificateType']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CertificateOptions'

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


class InvalidArtifactsDirectoryPathError(GreengrassCoreIPCError):
    """
    InvalidArtifactsDirectoryPathError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidArtifactsDirectoryPathError'

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


class InvalidRecipeDirectoryPathError(GreengrassCoreIPCError):
    """
    InvalidRecipeDirectoryPathError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidRecipeDirectoryPathError'

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


class CreateLocalDeploymentResponse(rpc.Shape):
    """
    CreateLocalDeploymentResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment_id: 

    Attributes:
        deployment_id: 
    """

    def __init__(self, *,
                 deployment_id: typing.Optional[str] = None):
        super().__init__()
        self.deployment_id = deployment_id  # type: typing.Optional[str]

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateLocalDeploymentResponse'

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


class CreateLocalDeploymentRequest(rpc.Shape):
    """
    CreateLocalDeploymentRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        group_name: 
        root_component_versions_to_add: 
        root_components_to_remove: 
        component_to_configuration: 
        component_to_run_with_info: 
        recipe_directory_path: 
        artifacts_directory_path: 

    Attributes:
        group_name: 
        root_component_versions_to_add: 
        root_components_to_remove: 
        component_to_configuration: 
        component_to_run_with_info: 
        recipe_directory_path: 
        artifacts_directory_path: 
    """

    def __init__(self, *,
                 group_name: typing.Optional[str] = None,
                 root_component_versions_to_add: typing.Optional[typing.Dict[str, str]] = None,
                 root_components_to_remove: typing.Optional[typing.List[str]] = None,
                 component_to_configuration: typing.Optional[typing.Dict[str, typing.Dict[str, typing.Any]]] = None,
                 component_to_run_with_info: typing.Optional[typing.Dict[str, RunWithInfo]] = None,
                 recipe_directory_path: typing.Optional[str] = None,
                 artifacts_directory_path: typing.Optional[str] = None):
        super().__init__()
        self.group_name = group_name  # type: typing.Optional[str]
        self.root_component_versions_to_add = root_component_versions_to_add  # type: typing.Optional[typing.Dict[str, str]]
        self.root_components_to_remove = root_components_to_remove  # type: typing.Optional[typing.List[str]]
        self.component_to_configuration = component_to_configuration  # type: typing.Optional[typing.Dict[str, typing.Dict[str, typing.Any]]]
        self.component_to_run_with_info = component_to_run_with_info  # type: typing.Optional[typing.Dict[str, RunWithInfo]]
        self.recipe_directory_path = recipe_directory_path  # type: typing.Optional[str]
        self.artifacts_directory_path = artifacts_directory_path  # type: typing.Optional[str]

    def set_group_name(self, group_name: str):
        self.group_name = group_name
        return self

    def set_root_component_versions_to_add(self, root_component_versions_to_add: typing.Dict[str, str]):
        self.root_component_versions_to_add = root_component_versions_to_add
        return self

    def set_root_components_to_remove(self, root_components_to_remove: typing.List[str]):
        self.root_components_to_remove = root_components_to_remove
        return self

    def set_component_to_configuration(self, component_to_configuration: typing.Dict[str, typing.Dict[str, typing.Any]]):
        self.component_to_configuration = component_to_configuration
        return self

    def set_component_to_run_with_info(self, component_to_run_with_info: typing.Dict[str, RunWithInfo]):
        self.component_to_run_with_info = component_to_run_with_info
        return self

    def set_recipe_directory_path(self, recipe_directory_path: str):
        self.recipe_directory_path = recipe_directory_path
        return self

    def set_artifacts_directory_path(self, artifacts_directory_path: str):
        self.artifacts_directory_path = artifacts_directory_path
        return self


    def _to_payload(self):
        payload = {}
        if self.group_name is not None:
            payload['groupName'] = self.group_name
        if self.root_component_versions_to_add is not None:
            payload['rootComponentVersionsToAdd'] = self.root_component_versions_to_add
        if self.root_components_to_remove is not None:
            payload['rootComponentsToRemove'] = self.root_components_to_remove
        if self.component_to_configuration is not None:
            payload['componentToConfiguration'] = self.component_to_configuration
        if self.component_to_run_with_info is not None:
            payload['componentToRunWithInfo'] = {k: v._to_payload() for k, v in self.component_to_run_with_info.items()}
        if self.recipe_directory_path is not None:
            payload['recipeDirectoryPath'] = self.recipe_directory_path
        if self.artifacts_directory_path is not None:
            payload['artifactsDirectoryPath'] = self.artifacts_directory_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'groupName' in payload:
            new.group_name = payload['groupName']
        if 'rootComponentVersionsToAdd' in payload:
            new.root_component_versions_to_add = payload['rootComponentVersionsToAdd']
        if 'rootComponentsToRemove' in payload:
            new.root_components_to_remove = payload['rootComponentsToRemove']
        if 'componentToConfiguration' in payload:
            new.component_to_configuration = payload['componentToConfiguration']
        if 'componentToRunWithInfo' in payload:
            new.component_to_run_with_info = {k: RunWithInfo._from_payload(v) for k,v in payload['componentToRunWithInfo'].items()}
        if 'recipeDirectoryPath' in payload:
            new.recipe_directory_path = payload['recipeDirectoryPath']
        if 'artifactsDirectoryPath' in payload:
            new.artifacts_directory_path = payload['artifactsDirectoryPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateLocalDeploymentRequest'

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


class PauseComponentResponse(rpc.Shape):
    """
    PauseComponentResponse
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
        return 'aws.greengrass#PauseComponentResponse'

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


class PauseComponentRequest(rpc.Shape):
    """
    PauseComponentRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 

    Attributes:
        component_name: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PauseComponentRequest'

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


class StopComponentResponse(rpc.Shape):
    """
    StopComponentResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        stop_status: RequestStatus enum value
        message: 

    Attributes:
        stop_status: RequestStatus enum value
        message: 
    """

    def __init__(self, *,
                 stop_status: typing.Optional[str] = None,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.stop_status = stop_status  # type: typing.Optional[str]
        self.message = message  # type: typing.Optional[str]

    def set_stop_status(self, stop_status: str):
        self.stop_status = stop_status
        return self

    def set_message(self, message: str):
        self.message = message
        return self


    def _to_payload(self):
        payload = {}
        if self.stop_status is not None:
            payload['stopStatus'] = self.stop_status
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'stopStatus' in payload:
            new.stop_status = payload['stopStatus']
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#StopComponentResponse'

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


class StopComponentRequest(rpc.Shape):
    """
    StopComponentRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 

    Attributes:
        component_name: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#StopComponentRequest'

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


class ListLocalDeploymentsResponse(rpc.Shape):
    """
    ListLocalDeploymentsResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        local_deployments: 

    Attributes:
        local_deployments: 
    """

    def __init__(self, *,
                 local_deployments: typing.Optional[typing.List[LocalDeployment]] = None):
        super().__init__()
        self.local_deployments = local_deployments  # type: typing.Optional[typing.List[LocalDeployment]]

    def set_local_deployments(self, local_deployments: typing.List[LocalDeployment]):
        self.local_deployments = local_deployments
        return self


    def _to_payload(self):
        payload = {}
        if self.local_deployments is not None:
            payload['localDeployments'] = [i._to_payload() for i in self.local_deployments]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'localDeployments' in payload:
            new.local_deployments = [LocalDeployment._from_payload(i) for i in payload['localDeployments']]
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListLocalDeploymentsResponse'

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


class ListLocalDeploymentsRequest(rpc.Shape):
    """
    ListLocalDeploymentsRequest
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
        return 'aws.greengrass#ListLocalDeploymentsRequest'

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


class SubscribeToComponentUpdatesResponse(rpc.Shape):
    """
    SubscribeToComponentUpdatesResponse
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
        return 'aws.greengrass#SubscribeToComponentUpdatesResponse'

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


class SubscribeToComponentUpdatesRequest(rpc.Shape):
    """
    SubscribeToComponentUpdatesRequest
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
        return 'aws.greengrass#SubscribeToComponentUpdatesRequest'

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


class ListNamedShadowsForThingResponse(rpc.Shape):
    """
    ListNamedShadowsForThingResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        results: 
        timestamp: 
        next_token: 

    Attributes:
        results: 
        timestamp: 
        next_token: 
    """

    def __init__(self, *,
                 results: typing.Optional[typing.List[str]] = None,
                 timestamp: typing.Optional[datetime.datetime] = None,
                 next_token: typing.Optional[str] = None):
        super().__init__()
        self.results = results  # type: typing.Optional[typing.List[str]]
        self.timestamp = timestamp  # type: typing.Optional[datetime.datetime]
        self.next_token = next_token  # type: typing.Optional[str]

    def set_results(self, results: typing.List[str]):
        self.results = results
        return self

    def set_timestamp(self, timestamp: datetime.datetime):
        self.timestamp = timestamp
        return self

    def set_next_token(self, next_token: str):
        self.next_token = next_token
        return self


    def _to_payload(self):
        payload = {}
        if self.results is not None:
            payload['results'] = self.results
        if self.timestamp is not None:
            payload['timestamp'] = self.timestamp.timestamp()
        if self.next_token is not None:
            payload['nextToken'] = self.next_token
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'results' in payload:
            new.results = payload['results']
        if 'timestamp' in payload:
            new.timestamp = datetime.datetime.fromtimestamp(payload['timestamp'], datetime.timezone.utc)
        if 'nextToken' in payload:
            new.next_token = payload['nextToken']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListNamedShadowsForThingResponse'

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


class ListNamedShadowsForThingRequest(rpc.Shape):
    """
    ListNamedShadowsForThingRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name: 
        next_token: 
        page_size: 

    Attributes:
        thing_name: 
        next_token: 
        page_size: 
    """

    def __init__(self, *,
                 thing_name: typing.Optional[str] = None,
                 next_token: typing.Optional[str] = None,
                 page_size: typing.Optional[int] = None):
        super().__init__()
        self.thing_name = thing_name  # type: typing.Optional[str]
        self.next_token = next_token  # type: typing.Optional[str]
        self.page_size = page_size  # type: typing.Optional[int]

    def set_thing_name(self, thing_name: str):
        self.thing_name = thing_name
        return self

    def set_next_token(self, next_token: str):
        self.next_token = next_token
        return self

    def set_page_size(self, page_size: int):
        self.page_size = page_size
        return self


    def _to_payload(self):
        payload = {}
        if self.thing_name is not None:
            payload['thingName'] = self.thing_name
        if self.next_token is not None:
            payload['nextToken'] = self.next_token
        if self.page_size is not None:
            payload['pageSize'] = self.page_size
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'thingName' in payload:
            new.thing_name = payload['thingName']
        if 'nextToken' in payload:
            new.next_token = payload['nextToken']
        if 'pageSize' in payload:
            new.page_size = int(payload['pageSize'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListNamedShadowsForThingRequest'

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


class UpdateStateResponse(rpc.Shape):
    """
    UpdateStateResponse
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
        return 'aws.greengrass#UpdateStateResponse'

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


class UpdateStateRequest(rpc.Shape):
    """
    UpdateStateRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        state: ReportedLifecycleState enum value

    Attributes:
        state: ReportedLifecycleState enum value
    """

    def __init__(self, *,
                 state: typing.Optional[str] = None):
        super().__init__()
        self.state = state  # type: typing.Optional[str]

    def set_state(self, state: str):
        self.state = state
        return self


    def _to_payload(self):
        payload = {}
        if self.state is not None:
            payload['state'] = self.state
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'state' in payload:
            new.state = payload['state']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateStateRequest'

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


class GetSecretValueResponse(rpc.Shape):
    """
    GetSecretValueResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        secret_id: 
        version_id: 
        version_stage: 
        secret_value: 

    Attributes:
        secret_id: 
        version_id: 
        version_stage: 
        secret_value: 
    """

    def __init__(self, *,
                 secret_id: typing.Optional[str] = None,
                 version_id: typing.Optional[str] = None,
                 version_stage: typing.Optional[typing.List[str]] = None,
                 secret_value: typing.Optional[SecretValue] = None):
        super().__init__()
        self.secret_id = secret_id  # type: typing.Optional[str]
        self.version_id = version_id  # type: typing.Optional[str]
        self.version_stage = version_stage  # type: typing.Optional[typing.List[str]]
        self.secret_value = secret_value  # type: typing.Optional[SecretValue]

    def set_secret_id(self, secret_id: str):
        self.secret_id = secret_id
        return self

    def set_version_id(self, version_id: str):
        self.version_id = version_id
        return self

    def set_version_stage(self, version_stage: typing.List[str]):
        self.version_stage = version_stage
        return self

    def set_secret_value(self, secret_value: SecretValue):
        self.secret_value = secret_value
        return self


    def _to_payload(self):
        payload = {}
        if self.secret_id is not None:
            payload['secretId'] = self.secret_id
        if self.version_id is not None:
            payload['versionId'] = self.version_id
        if self.version_stage is not None:
            payload['versionStage'] = self.version_stage
        if self.secret_value is not None:
            payload['secretValue'] = self.secret_value._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'secretId' in payload:
            new.secret_id = payload['secretId']
        if 'versionId' in payload:
            new.version_id = payload['versionId']
        if 'versionStage' in payload:
            new.version_stage = payload['versionStage']
        if 'secretValue' in payload:
            new.secret_value = SecretValue._from_payload(payload['secretValue'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetSecretValueResponse'

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


class GetSecretValueRequest(rpc.Shape):
    """
    GetSecretValueRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        secret_id: 
        version_id: 
        version_stage: 

    Attributes:
        secret_id: 
        version_id: 
        version_stage: 
    """

    def __init__(self, *,
                 secret_id: typing.Optional[str] = None,
                 version_id: typing.Optional[str] = None,
                 version_stage: typing.Optional[str] = None):
        super().__init__()
        self.secret_id = secret_id  # type: typing.Optional[str]
        self.version_id = version_id  # type: typing.Optional[str]
        self.version_stage = version_stage  # type: typing.Optional[str]

    def set_secret_id(self, secret_id: str):
        self.secret_id = secret_id
        return self

    def set_version_id(self, version_id: str):
        self.version_id = version_id
        return self

    def set_version_stage(self, version_stage: str):
        self.version_stage = version_stage
        return self


    def _to_payload(self):
        payload = {}
        if self.secret_id is not None:
            payload['secretId'] = self.secret_id
        if self.version_id is not None:
            payload['versionId'] = self.version_id
        if self.version_stage is not None:
            payload['versionStage'] = self.version_stage
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'secretId' in payload:
            new.secret_id = payload['secretId']
        if 'versionId' in payload:
            new.version_id = payload['versionId']
        if 'versionStage' in payload:
            new.version_stage = payload['versionStage']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetSecretValueRequest'

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


class GetLocalDeploymentStatusResponse(rpc.Shape):
    """
    GetLocalDeploymentStatusResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment: 

    Attributes:
        deployment: 
    """

    def __init__(self, *,
                 deployment: typing.Optional[LocalDeployment] = None):
        super().__init__()
        self.deployment = deployment  # type: typing.Optional[LocalDeployment]

    def set_deployment(self, deployment: LocalDeployment):
        self.deployment = deployment
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment is not None:
            payload['deployment'] = self.deployment._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deployment' in payload:
            new.deployment = LocalDeployment._from_payload(payload['deployment'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetLocalDeploymentStatusResponse'

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


class GetLocalDeploymentStatusRequest(rpc.Shape):
    """
    GetLocalDeploymentStatusRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment_id: 

    Attributes:
        deployment_id: 
    """

    def __init__(self, *,
                 deployment_id: typing.Optional[str] = None):
        super().__init__()
        self.deployment_id = deployment_id  # type: typing.Optional[str]

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetLocalDeploymentStatusRequest'

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


class ComponentNotFoundError(GreengrassCoreIPCError):
    """
    ComponentNotFoundError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ComponentNotFoundError'

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


class RestartComponentResponse(rpc.Shape):
    """
    RestartComponentResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        restart_status: RequestStatus enum value
        message: 

    Attributes:
        restart_status: RequestStatus enum value
        message: 
    """

    def __init__(self, *,
                 restart_status: typing.Optional[str] = None,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.restart_status = restart_status  # type: typing.Optional[str]
        self.message = message  # type: typing.Optional[str]

    def set_restart_status(self, restart_status: str):
        self.restart_status = restart_status
        return self

    def set_message(self, message: str):
        self.message = message
        return self


    def _to_payload(self):
        payload = {}
        if self.restart_status is not None:
            payload['restartStatus'] = self.restart_status
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'restartStatus' in payload:
            new.restart_status = payload['restartStatus']
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#RestartComponentResponse'

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


class RestartComponentRequest(rpc.Shape):
    """
    RestartComponentRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 

    Attributes:
        component_name: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#RestartComponentRequest'

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


class InvalidTokenError(GreengrassCoreIPCError):
    """
    InvalidTokenError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'server'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidTokenError'

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


class ValidateAuthorizationTokenResponse(rpc.Shape):
    """
    ValidateAuthorizationTokenResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        is_valid: 

    Attributes:
        is_valid: 
    """

    def __init__(self, *,
                 is_valid: typing.Optional[bool] = None):
        super().__init__()
        self.is_valid = is_valid  # type: typing.Optional[bool]

    def set_is_valid(self, is_valid: bool):
        self.is_valid = is_valid
        return self


    def _to_payload(self):
        payload = {}
        if self.is_valid is not None:
            payload['isValid'] = self.is_valid
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'isValid' in payload:
            new.is_valid = payload['isValid']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateAuthorizationTokenResponse'

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


class ValidateAuthorizationTokenRequest(rpc.Shape):
    """
    ValidateAuthorizationTokenRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        token: 

    Attributes:
        token: 
    """

    def __init__(self, *,
                 token: typing.Optional[str] = None):
        super().__init__()
        self.token = token  # type: typing.Optional[str]

    def set_token(self, token: str):
        self.token = token
        return self


    def _to_payload(self):
        payload = {}
        if self.token is not None:
            payload['token'] = self.token
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'token' in payload:
            new.token = payload['token']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateAuthorizationTokenRequest'

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


class FailedUpdateConditionCheckError(GreengrassCoreIPCError):
    """
    FailedUpdateConditionCheckError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#FailedUpdateConditionCheckError'

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


class UpdateConfigurationResponse(rpc.Shape):
    """
    UpdateConfigurationResponse
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
        return 'aws.greengrass#UpdateConfigurationResponse'

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


class UpdateConfigurationRequest(rpc.Shape):
    """
    UpdateConfigurationRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        key_path: 
        timestamp: 
        value_to_merge: 

    Attributes:
        key_path: 
        timestamp: 
        value_to_merge: 
    """

    def __init__(self, *,
                 key_path: typing.Optional[typing.List[str]] = None,
                 timestamp: typing.Optional[datetime.datetime] = None,
                 value_to_merge: typing.Optional[typing.Dict[str, typing.Any]] = None):
        super().__init__()
        self.key_path = key_path  # type: typing.Optional[typing.List[str]]
        self.timestamp = timestamp  # type: typing.Optional[datetime.datetime]
        self.value_to_merge = value_to_merge  # type: typing.Optional[typing.Dict[str, typing.Any]]

    def set_key_path(self, key_path: typing.List[str]):
        self.key_path = key_path
        return self

    def set_timestamp(self, timestamp: datetime.datetime):
        self.timestamp = timestamp
        return self

    def set_value_to_merge(self, value_to_merge: typing.Dict[str, typing.Any]):
        self.value_to_merge = value_to_merge
        return self


    def _to_payload(self):
        payload = {}
        if self.key_path is not None:
            payload['keyPath'] = self.key_path
        if self.timestamp is not None:
            payload['timestamp'] = self.timestamp.timestamp()
        if self.value_to_merge is not None:
            payload['valueToMerge'] = self.value_to_merge
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'keyPath' in payload:
            new.key_path = payload['keyPath']
        if 'timestamp' in payload:
            new.timestamp = datetime.datetime.fromtimestamp(payload['timestamp'], datetime.timezone.utc)
        if 'valueToMerge' in payload:
            new.value_to_merge = payload['valueToMerge']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateConfigurationRequest'

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


class ConflictError(GreengrassCoreIPCError):
    """
    ConflictError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConflictError'

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


class UpdateThingShadowResponse(rpc.Shape):
    """
    UpdateThingShadowResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        payload: 

    Attributes:
        payload: 
    """

    def __init__(self, *,
                 payload: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload  # type: typing.Optional[bytes]

    def set_payload(self, payload: typing.Union[bytes, str]):
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload
        return self


    def _to_payload(self):
        payload = {}
        if self.payload is not None:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'payload' in payload:
            new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateThingShadowResponse'

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


class UpdateThingShadowRequest(rpc.Shape):
    """
    UpdateThingShadowRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name: 
        shadow_name: 
        payload: 

    Attributes:
        thing_name: 
        shadow_name: 
        payload: 
    """

    def __init__(self, *,
                 thing_name: typing.Optional[str] = None,
                 shadow_name: typing.Optional[str] = None,
                 payload: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        self.thing_name = thing_name  # type: typing.Optional[str]
        self.shadow_name = shadow_name  # type: typing.Optional[str]
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload  # type: typing.Optional[bytes]

    def set_thing_name(self, thing_name: str):
        self.thing_name = thing_name
        return self

    def set_shadow_name(self, shadow_name: str):
        self.shadow_name = shadow_name
        return self

    def set_payload(self, payload: typing.Union[bytes, str]):
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload
        return self


    def _to_payload(self):
        payload = {}
        if self.thing_name is not None:
            payload['thingName'] = self.thing_name
        if self.shadow_name is not None:
            payload['shadowName'] = self.shadow_name
        if self.payload is not None:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'thingName' in payload:
            new.thing_name = payload['thingName']
        if 'shadowName' in payload:
            new.shadow_name = payload['shadowName']
        if 'payload' in payload:
            new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateThingShadowRequest'

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


class SendConfigurationValidityReportResponse(rpc.Shape):
    """
    SendConfigurationValidityReportResponse
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
        return 'aws.greengrass#SendConfigurationValidityReportResponse'

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


class SendConfigurationValidityReportRequest(rpc.Shape):
    """
    SendConfigurationValidityReportRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        configuration_validity_report: 

    Attributes:
        configuration_validity_report: 
    """

    def __init__(self, *,
                 configuration_validity_report: typing.Optional[ConfigurationValidityReport] = None):
        super().__init__()
        self.configuration_validity_report = configuration_validity_report  # type: typing.Optional[ConfigurationValidityReport]

    def set_configuration_validity_report(self, configuration_validity_report: ConfigurationValidityReport):
        self.configuration_validity_report = configuration_validity_report
        return self


    def _to_payload(self):
        payload = {}
        if self.configuration_validity_report is not None:
            payload['configurationValidityReport'] = self.configuration_validity_report._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'configurationValidityReport' in payload:
            new.configuration_validity_report = ConfigurationValidityReport._from_payload(payload['configurationValidityReport'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SendConfigurationValidityReportRequest'

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


class GetThingShadowResponse(rpc.Shape):
    """
    GetThingShadowResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        payload: 

    Attributes:
        payload: 
    """

    def __init__(self, *,
                 payload: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload  # type: typing.Optional[bytes]

    def set_payload(self, payload: typing.Union[bytes, str]):
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload
        return self


    def _to_payload(self):
        payload = {}
        if self.payload is not None:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'payload' in payload:
            new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetThingShadowResponse'

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


class GetThingShadowRequest(rpc.Shape):
    """
    GetThingShadowRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name: 
        shadow_name: 

    Attributes:
        thing_name: 
        shadow_name: 
    """

    def __init__(self, *,
                 thing_name: typing.Optional[str] = None,
                 shadow_name: typing.Optional[str] = None):
        super().__init__()
        self.thing_name = thing_name  # type: typing.Optional[str]
        self.shadow_name = shadow_name  # type: typing.Optional[str]

    def set_thing_name(self, thing_name: str):
        self.thing_name = thing_name
        return self

    def set_shadow_name(self, shadow_name: str):
        self.shadow_name = shadow_name
        return self


    def _to_payload(self):
        payload = {}
        if self.thing_name is not None:
            payload['thingName'] = self.thing_name
        if self.shadow_name is not None:
            payload['shadowName'] = self.shadow_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'thingName' in payload:
            new.thing_name = payload['thingName']
        if 'shadowName' in payload:
            new.shadow_name = payload['shadowName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetThingShadowRequest'

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


class CreateDebugPasswordResponse(rpc.Shape):
    """
    CreateDebugPasswordResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        password: 
        username: 
        password_expiration: 
        certificate_sha256_hash: 
        certificate_sha1_hash: 

    Attributes:
        password: 
        username: 
        password_expiration: 
        certificate_sha256_hash: 
        certificate_sha1_hash: 
    """

    def __init__(self, *,
                 password: typing.Optional[str] = None,
                 username: typing.Optional[str] = None,
                 password_expiration: typing.Optional[datetime.datetime] = None,
                 certificate_sha256_hash: typing.Optional[str] = None,
                 certificate_sha1_hash: typing.Optional[str] = None):
        super().__init__()
        self.password = password  # type: typing.Optional[str]
        self.username = username  # type: typing.Optional[str]
        self.password_expiration = password_expiration  # type: typing.Optional[datetime.datetime]
        self.certificate_sha256_hash = certificate_sha256_hash  # type: typing.Optional[str]
        self.certificate_sha1_hash = certificate_sha1_hash  # type: typing.Optional[str]

    def set_password(self, password: str):
        self.password = password
        return self

    def set_username(self, username: str):
        self.username = username
        return self

    def set_password_expiration(self, password_expiration: datetime.datetime):
        self.password_expiration = password_expiration
        return self

    def set_certificate_sha256_hash(self, certificate_sha256_hash: str):
        self.certificate_sha256_hash = certificate_sha256_hash
        return self

    def set_certificate_sha1_hash(self, certificate_sha1_hash: str):
        self.certificate_sha1_hash = certificate_sha1_hash
        return self


    def _to_payload(self):
        payload = {}
        if self.password is not None:
            payload['password'] = self.password
        if self.username is not None:
            payload['username'] = self.username
        if self.password_expiration is not None:
            payload['passwordExpiration'] = self.password_expiration.timestamp()
        if self.certificate_sha256_hash is not None:
            payload['certificateSHA256Hash'] = self.certificate_sha256_hash
        if self.certificate_sha1_hash is not None:
            payload['certificateSHA1Hash'] = self.certificate_sha1_hash
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'password' in payload:
            new.password = payload['password']
        if 'username' in payload:
            new.username = payload['username']
        if 'passwordExpiration' in payload:
            new.password_expiration = datetime.datetime.fromtimestamp(payload['passwordExpiration'], datetime.timezone.utc)
        if 'certificateSHA256Hash' in payload:
            new.certificate_sha256_hash = payload['certificateSHA256Hash']
        if 'certificateSHA1Hash' in payload:
            new.certificate_sha1_hash = payload['certificateSHA1Hash']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateDebugPasswordResponse'

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


class CreateDebugPasswordRequest(rpc.Shape):
    """
    CreateDebugPasswordRequest
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
        return 'aws.greengrass#CreateDebugPasswordRequest'

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


class ListComponentsResponse(rpc.Shape):
    """
    ListComponentsResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        components: 

    Attributes:
        components: 
    """

    def __init__(self, *,
                 components: typing.Optional[typing.List[ComponentDetails]] = None):
        super().__init__()
        self.components = components  # type: typing.Optional[typing.List[ComponentDetails]]

    def set_components(self, components: typing.List[ComponentDetails]):
        self.components = components
        return self


    def _to_payload(self):
        payload = {}
        if self.components is not None:
            payload['components'] = [i._to_payload() for i in self.components]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'components' in payload:
            new.components = [ComponentDetails._from_payload(i) for i in payload['components']]
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListComponentsResponse'

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


class ListComponentsRequest(rpc.Shape):
    """
    ListComponentsRequest
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
        return 'aws.greengrass#ListComponentsRequest'

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


class InvalidClientDeviceAuthTokenError(GreengrassCoreIPCError):
    """
    InvalidClientDeviceAuthTokenError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidClientDeviceAuthTokenError'

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


class AuthorizeClientDeviceActionResponse(rpc.Shape):
    """
    AuthorizeClientDeviceActionResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        is_authorized: 

    Attributes:
        is_authorized: 
    """

    def __init__(self, *,
                 is_authorized: typing.Optional[bool] = None):
        super().__init__()
        self.is_authorized = is_authorized  # type: typing.Optional[bool]

    def set_is_authorized(self, is_authorized: bool):
        self.is_authorized = is_authorized
        return self


    def _to_payload(self):
        payload = {}
        if self.is_authorized is not None:
            payload['isAuthorized'] = self.is_authorized
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'isAuthorized' in payload:
            new.is_authorized = payload['isAuthorized']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#AuthorizeClientDeviceActionResponse'

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


class AuthorizeClientDeviceActionRequest(rpc.Shape):
    """
    AuthorizeClientDeviceActionRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_device_auth_token: 
        operation: 
        resource: 

    Attributes:
        client_device_auth_token: 
        operation: 
        resource: 
    """

    def __init__(self, *,
                 client_device_auth_token: typing.Optional[str] = None,
                 operation: typing.Optional[str] = None,
                 resource: typing.Optional[str] = None):
        super().__init__()
        self.client_device_auth_token = client_device_auth_token  # type: typing.Optional[str]
        self.operation = operation  # type: typing.Optional[str]
        self.resource = resource  # type: typing.Optional[str]

    def set_client_device_auth_token(self, client_device_auth_token: str):
        self.client_device_auth_token = client_device_auth_token
        return self

    def set_operation(self, operation: str):
        self.operation = operation
        return self

    def set_resource(self, resource: str):
        self.resource = resource
        return self


    def _to_payload(self):
        payload = {}
        if self.client_device_auth_token is not None:
            payload['clientDeviceAuthToken'] = self.client_device_auth_token
        if self.operation is not None:
            payload['operation'] = self.operation
        if self.resource is not None:
            payload['resource'] = self.resource
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'clientDeviceAuthToken' in payload:
            new.client_device_auth_token = payload['clientDeviceAuthToken']
        if 'operation' in payload:
            new.operation = payload['operation']
        if 'resource' in payload:
            new.resource = payload['resource']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#AuthorizeClientDeviceActionRequest'

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


class VerifyClientDeviceIdentityResponse(rpc.Shape):
    """
    VerifyClientDeviceIdentityResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        is_valid_client_device: 

    Attributes:
        is_valid_client_device: 
    """

    def __init__(self, *,
                 is_valid_client_device: typing.Optional[bool] = None):
        super().__init__()
        self.is_valid_client_device = is_valid_client_device  # type: typing.Optional[bool]

    def set_is_valid_client_device(self, is_valid_client_device: bool):
        self.is_valid_client_device = is_valid_client_device
        return self


    def _to_payload(self):
        payload = {}
        if self.is_valid_client_device is not None:
            payload['isValidClientDevice'] = self.is_valid_client_device
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'isValidClientDevice' in payload:
            new.is_valid_client_device = payload['isValidClientDevice']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#VerifyClientDeviceIdentityResponse'

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


class VerifyClientDeviceIdentityRequest(rpc.Shape):
    """
    VerifyClientDeviceIdentityRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        credential: 

    Attributes:
        credential: 
    """

    def __init__(self, *,
                 credential: typing.Optional[ClientDeviceCredential] = None):
        super().__init__()
        self.credential = credential  # type: typing.Optional[ClientDeviceCredential]

    def set_credential(self, credential: ClientDeviceCredential):
        self.credential = credential
        return self


    def _to_payload(self):
        payload = {}
        if self.credential is not None:
            payload['credential'] = self.credential._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'credential' in payload:
            new.credential = ClientDeviceCredential._from_payload(payload['credential'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#VerifyClientDeviceIdentityRequest'

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


class SubscribeToCertificateUpdatesResponse(rpc.Shape):
    """
    SubscribeToCertificateUpdatesResponse
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
        return 'aws.greengrass#SubscribeToCertificateUpdatesResponse'

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


class SubscribeToCertificateUpdatesRequest(rpc.Shape):
    """
    SubscribeToCertificateUpdatesRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        certificate_options: 

    Attributes:
        certificate_options: 
    """

    def __init__(self, *,
                 certificate_options: typing.Optional[CertificateOptions] = None):
        super().__init__()
        self.certificate_options = certificate_options  # type: typing.Optional[CertificateOptions]

    def set_certificate_options(self, certificate_options: CertificateOptions):
        self.certificate_options = certificate_options
        return self


    def _to_payload(self):
        payload = {}
        if self.certificate_options is not None:
            payload['certificateOptions'] = self.certificate_options._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'certificateOptions' in payload:
            new.certificate_options = CertificateOptions._from_payload(payload['certificateOptions'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToCertificateUpdatesRequest'

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


class PublishToTopicResponse(rpc.Shape):
    """
    PublishToTopicResponse
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
        return 'aws.greengrass#PublishToTopicResponse'

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


class PublishToTopicRequest(rpc.Shape):
    """
    PublishToTopicRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic: 
        publish_message: 

    Attributes:
        topic: 
        publish_message: 
    """

    def __init__(self, *,
                 topic: typing.Optional[str] = None,
                 publish_message: typing.Optional[PublishMessage] = None):
        super().__init__()
        self.topic = topic  # type: typing.Optional[str]
        self.publish_message = publish_message  # type: typing.Optional[PublishMessage]

    def set_topic(self, topic: str):
        self.topic = topic
        return self

    def set_publish_message(self, publish_message: PublishMessage):
        self.publish_message = publish_message
        return self


    def _to_payload(self):
        payload = {}
        if self.topic is not None:
            payload['topic'] = self.topic
        if self.publish_message is not None:
            payload['publishMessage'] = self.publish_message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topic' in payload:
            new.topic = payload['topic']
        if 'publishMessage' in payload:
            new.publish_message = PublishMessage._from_payload(payload['publishMessage'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishToTopicRequest'

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


class InvalidCredentialError(GreengrassCoreIPCError):
    """
    InvalidCredentialError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidCredentialError'

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


class GetClientDeviceAuthTokenResponse(rpc.Shape):
    """
    GetClientDeviceAuthTokenResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        client_device_auth_token: 

    Attributes:
        client_device_auth_token: 
    """

    def __init__(self, *,
                 client_device_auth_token: typing.Optional[str] = None):
        super().__init__()
        self.client_device_auth_token = client_device_auth_token  # type: typing.Optional[str]

    def set_client_device_auth_token(self, client_device_auth_token: str):
        self.client_device_auth_token = client_device_auth_token
        return self


    def _to_payload(self):
        payload = {}
        if self.client_device_auth_token is not None:
            payload['clientDeviceAuthToken'] = self.client_device_auth_token
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'clientDeviceAuthToken' in payload:
            new.client_device_auth_token = payload['clientDeviceAuthToken']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetClientDeviceAuthTokenResponse'

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


class GetClientDeviceAuthTokenRequest(rpc.Shape):
    """
    GetClientDeviceAuthTokenRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        credential: 

    Attributes:
        credential: 
    """

    def __init__(self, *,
                 credential: typing.Optional[CredentialDocument] = None):
        super().__init__()
        self.credential = credential  # type: typing.Optional[CredentialDocument]

    def set_credential(self, credential: CredentialDocument):
        self.credential = credential
        return self


    def _to_payload(self):
        payload = {}
        if self.credential is not None:
            payload['credential'] = self.credential._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'credential' in payload:
            new.credential = CredentialDocument._from_payload(payload['credential'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetClientDeviceAuthTokenRequest'

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


class GetComponentDetailsResponse(rpc.Shape):
    """
    GetComponentDetailsResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_details: 

    Attributes:
        component_details: 
    """

    def __init__(self, *,
                 component_details: typing.Optional[ComponentDetails] = None):
        super().__init__()
        self.component_details = component_details  # type: typing.Optional[ComponentDetails]

    def set_component_details(self, component_details: ComponentDetails):
        self.component_details = component_details
        return self


    def _to_payload(self):
        payload = {}
        if self.component_details is not None:
            payload['componentDetails'] = self.component_details._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentDetails' in payload:
            new.component_details = ComponentDetails._from_payload(payload['componentDetails'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetComponentDetailsResponse'

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


class GetComponentDetailsRequest(rpc.Shape):
    """
    GetComponentDetailsRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 

    Attributes:
        component_name: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetComponentDetailsRequest'

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


class SubscribeToTopicResponse(rpc.Shape):
    """
    SubscribeToTopicResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic_name: Deprecated  No longer used

    Attributes:
        topic_name: Deprecated  No longer used
    """

    def __init__(self, *,
                 topic_name: typing.Optional[str] = None):
        super().__init__()
        self.topic_name = topic_name  # type: typing.Optional[str]

    def set_topic_name(self, topic_name: str):
        self.topic_name = topic_name
        return self


    def _to_payload(self):
        payload = {}
        if self.topic_name is not None:
            payload['topicName'] = self.topic_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            new.topic_name = payload['topicName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToTopicResponse'

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


class SubscribeToTopicRequest(rpc.Shape):
    """
    SubscribeToTopicRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic: 
        receive_mode: ReceiveMode enum value

    Attributes:
        topic: 
        receive_mode: ReceiveMode enum value
    """

    def __init__(self, *,
                 topic: typing.Optional[str] = None,
                 receive_mode: typing.Optional[str] = None):
        super().__init__()
        self.topic = topic  # type: typing.Optional[str]
        self.receive_mode = receive_mode  # type: typing.Optional[str]

    def set_topic(self, topic: str):
        self.topic = topic
        return self

    def set_receive_mode(self, receive_mode: str):
        self.receive_mode = receive_mode
        return self


    def _to_payload(self):
        payload = {}
        if self.topic is not None:
            payload['topic'] = self.topic
        if self.receive_mode is not None:
            payload['receiveMode'] = self.receive_mode
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topic' in payload:
            new.topic = payload['topic']
        if 'receiveMode' in payload:
            new.receive_mode = payload['receiveMode']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToTopicRequest'

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


class GetConfigurationResponse(rpc.Shape):
    """
    GetConfigurationResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 
        value: 

    Attributes:
        component_name: 
        value: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None,
                 value: typing.Optional[typing.Dict[str, typing.Any]] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]
        self.value = value  # type: typing.Optional[typing.Dict[str, typing.Any]]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self

    def set_value(self, value: typing.Dict[str, typing.Any]):
        self.value = value
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        if self.value is not None:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        if 'value' in payload:
            new.value = payload['value']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetConfigurationResponse'

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


class GetConfigurationRequest(rpc.Shape):
    """
    GetConfigurationRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 
        key_path: 

    Attributes:
        component_name: 
        key_path: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None,
                 key_path: typing.Optional[typing.List[str]] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]
        self.key_path = key_path  # type: typing.Optional[typing.List[str]]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self

    def set_key_path(self, key_path: typing.List[str]):
        self.key_path = key_path
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        if self.key_path is not None:
            payload['keyPath'] = self.key_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        if 'keyPath' in payload:
            new.key_path = payload['keyPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetConfigurationRequest'

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


class SubscribeToValidateConfigurationUpdatesResponse(rpc.Shape):
    """
    SubscribeToValidateConfigurationUpdatesResponse
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
        return 'aws.greengrass#SubscribeToValidateConfigurationUpdatesResponse'

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


class SubscribeToValidateConfigurationUpdatesRequest(rpc.Shape):
    """
    SubscribeToValidateConfigurationUpdatesRequest
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
        return 'aws.greengrass#SubscribeToValidateConfigurationUpdatesRequest'

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


class DeferComponentUpdateResponse(rpc.Shape):
    """
    DeferComponentUpdateResponse
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
        return 'aws.greengrass#DeferComponentUpdateResponse'

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


class DeferComponentUpdateRequest(rpc.Shape):
    """
    DeferComponentUpdateRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        deployment_id: 
        message: 
        recheck_after_ms: 

    Attributes:
        deployment_id: 
        message: 
        recheck_after_ms: 
    """

    def __init__(self, *,
                 deployment_id: typing.Optional[str] = None,
                 message: typing.Optional[str] = None,
                 recheck_after_ms: typing.Optional[int] = None):
        super().__init__()
        self.deployment_id = deployment_id  # type: typing.Optional[str]
        self.message = message  # type: typing.Optional[str]
        self.recheck_after_ms = recheck_after_ms  # type: typing.Optional[int]

    def set_deployment_id(self, deployment_id: str):
        self.deployment_id = deployment_id
        return self

    def set_message(self, message: str):
        self.message = message
        return self

    def set_recheck_after_ms(self, recheck_after_ms: int):
        self.recheck_after_ms = recheck_after_ms
        return self


    def _to_payload(self):
        payload = {}
        if self.deployment_id is not None:
            payload['deploymentId'] = self.deployment_id
        if self.message is not None:
            payload['message'] = self.message
        if self.recheck_after_ms is not None:
            payload['recheckAfterMs'] = self.recheck_after_ms
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            new.deployment_id = payload['deploymentId']
        if 'message' in payload:
            new.message = payload['message']
        if 'recheckAfterMs' in payload:
            new.recheck_after_ms = int(payload['recheckAfterMs'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#DeferComponentUpdateRequest'

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


class PutComponentMetricResponse(rpc.Shape):
    """
    PutComponentMetricResponse
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
        return 'aws.greengrass#PutComponentMetricResponse'

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


class PutComponentMetricRequest(rpc.Shape):
    """
    PutComponentMetricRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        metrics: 

    Attributes:
        metrics: 
    """

    def __init__(self, *,
                 metrics: typing.Optional[typing.List[Metric]] = None):
        super().__init__()
        self.metrics = metrics  # type: typing.Optional[typing.List[Metric]]

    def set_metrics(self, metrics: typing.List[Metric]):
        self.metrics = metrics
        return self


    def _to_payload(self):
        payload = {}
        if self.metrics is not None:
            payload['metrics'] = [i._to_payload() for i in self.metrics]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'metrics' in payload:
            new.metrics = [Metric._from_payload(i) for i in payload['metrics']]
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PutComponentMetricRequest'

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


class InvalidArgumentsError(GreengrassCoreIPCError):
    """
    InvalidArgumentsError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidArgumentsError'

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


class DeleteThingShadowResponse(rpc.Shape):
    """
    DeleteThingShadowResponse

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        payload: 

    Attributes:
        payload: 
    """

    def __init__(self, *,
                 payload: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload  # type: typing.Optional[bytes]

    def set_payload(self, payload: typing.Union[bytes, str]):
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload
        return self


    def _to_payload(self):
        payload = {}
        if self.payload is not None:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'payload' in payload:
            new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#DeleteThingShadowResponse'

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


class DeleteThingShadowRequest(rpc.Shape):
    """
    DeleteThingShadowRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        thing_name: 
        shadow_name: 

    Attributes:
        thing_name: 
        shadow_name: 
    """

    def __init__(self, *,
                 thing_name: typing.Optional[str] = None,
                 shadow_name: typing.Optional[str] = None):
        super().__init__()
        self.thing_name = thing_name  # type: typing.Optional[str]
        self.shadow_name = shadow_name  # type: typing.Optional[str]

    def set_thing_name(self, thing_name: str):
        self.thing_name = thing_name
        return self

    def set_shadow_name(self, shadow_name: str):
        self.shadow_name = shadow_name
        return self


    def _to_payload(self):
        payload = {}
        if self.thing_name is not None:
            payload['thingName'] = self.thing_name
        if self.shadow_name is not None:
            payload['shadowName'] = self.shadow_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'thingName' in payload:
            new.thing_name = payload['thingName']
        if 'shadowName' in payload:
            new.shadow_name = payload['shadowName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#DeleteThingShadowRequest'

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


class SubscribeToConfigurationUpdateResponse(rpc.Shape):
    """
    SubscribeToConfigurationUpdateResponse
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
        return 'aws.greengrass#SubscribeToConfigurationUpdateResponse'

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


class SubscribeToConfigurationUpdateRequest(rpc.Shape):
    """
    SubscribeToConfigurationUpdateRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 
        key_path: 

    Attributes:
        component_name: 
        key_path: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None,
                 key_path: typing.Optional[typing.List[str]] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]
        self.key_path = key_path  # type: typing.Optional[typing.List[str]]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self

    def set_key_path(self, key_path: typing.List[str]):
        self.key_path = key_path
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        if self.key_path is not None:
            payload['keyPath'] = self.key_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        if 'keyPath' in payload:
            new.key_path = payload['keyPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToConfigurationUpdateRequest'

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


class PublishToIoTCoreResponse(rpc.Shape):
    """
    PublishToIoTCoreResponse
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
        return 'aws.greengrass#PublishToIoTCoreResponse'

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


class PublishToIoTCoreRequest(rpc.Shape):
    """
    PublishToIoTCoreRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic_name: 
        qos: QOS enum value
        payload: 

    Attributes:
        topic_name: 
        qos: QOS enum value
        payload: 
    """

    def __init__(self, *,
                 topic_name: typing.Optional[str] = None,
                 qos: typing.Optional[str] = None,
                 payload: typing.Optional[typing.Union[bytes, str]] = None):
        super().__init__()
        self.topic_name = topic_name  # type: typing.Optional[str]
        self.qos = qos  # type: typing.Optional[str]
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload  # type: typing.Optional[bytes]

    def set_topic_name(self, topic_name: str):
        self.topic_name = topic_name
        return self

    def set_qos(self, qos: str):
        self.qos = qos
        return self

    def set_payload(self, payload: typing.Union[bytes, str]):
        if payload is not None and isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.payload = payload
        return self


    def _to_payload(self):
        payload = {}
        if self.topic_name is not None:
            payload['topicName'] = self.topic_name
        if self.qos is not None:
            payload['qos'] = self.qos
        if self.payload is not None:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            new.topic_name = payload['topicName']
        if 'qos' in payload:
            new.qos = payload['qos']
        if 'payload' in payload:
            new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishToIoTCoreRequest'

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


class ResourceNotFoundError(GreengrassCoreIPCError):
    """
    ResourceNotFoundError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 
        resource_type: 
        resource_name: 

    Attributes:
        message: 
        resource_type: 
        resource_name: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None,
                 resource_type: typing.Optional[str] = None,
                 resource_name: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]
        self.resource_type = resource_type  # type: typing.Optional[str]
        self.resource_name = resource_name  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self

    def set_resource_type(self, resource_type: str):
        self.resource_type = resource_type
        return self

    def set_resource_name(self, resource_name: str):
        self.resource_name = resource_name
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        if self.resource_type is not None:
            payload['resourceType'] = self.resource_type
        if self.resource_name is not None:
            payload['resourceName'] = self.resource_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        if 'resourceType' in payload:
            new.resource_type = payload['resourceType']
        if 'resourceName' in payload:
            new.resource_name = payload['resourceName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ResourceNotFoundError'

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


class ResumeComponentResponse(rpc.Shape):
    """
    ResumeComponentResponse
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
        return 'aws.greengrass#ResumeComponentResponse'

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


class ResumeComponentRequest(rpc.Shape):
    """
    ResumeComponentRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        component_name: 

    Attributes:
        component_name: 
    """

    def __init__(self, *,
                 component_name: typing.Optional[str] = None):
        super().__init__()
        self.component_name = component_name  # type: typing.Optional[str]

    def set_component_name(self, component_name: str):
        self.component_name = component_name
        return self


    def _to_payload(self):
        payload = {}
        if self.component_name is not None:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ResumeComponentRequest'

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


class UnauthorizedError(GreengrassCoreIPCError):
    """
    UnauthorizedError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UnauthorizedError'

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


class ServiceError(GreengrassCoreIPCError):
    """
    ServiceError

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        message: 

    Attributes:
        message: 
    """

    def __init__(self, *,
                 message: typing.Optional[str] = None):
        super().__init__()
        self.message = message  # type: typing.Optional[str]

    def set_message(self, message: str):
        self.message = message
        return self


    def _get_error_type_string(self):
        return 'server'

    def _to_payload(self):
        payload = {}
        if self.message is not None:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ServiceError'

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


class SubscribeToIoTCoreResponse(rpc.Shape):
    """
    SubscribeToIoTCoreResponse
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
        return 'aws.greengrass#SubscribeToIoTCoreResponse'

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


class SubscribeToIoTCoreRequest(rpc.Shape):
    """
    SubscribeToIoTCoreRequest

    All attributes are None by default, and may be set by keyword in the constructor.

    Keyword Args:
        topic_name: 
        qos: QOS enum value

    Attributes:
        topic_name: 
        qos: QOS enum value
    """

    def __init__(self, *,
                 topic_name: typing.Optional[str] = None,
                 qos: typing.Optional[str] = None):
        super().__init__()
        self.topic_name = topic_name  # type: typing.Optional[str]
        self.qos = qos  # type: typing.Optional[str]

    def set_topic_name(self, topic_name: str):
        self.topic_name = topic_name
        return self

    def set_qos(self, qos: str):
        self.qos = qos
        return self


    def _to_payload(self):
        payload = {}
        if self.topic_name is not None:
            payload['topicName'] = self.topic_name
        if self.qos is not None:
            payload['qos'] = self.qos
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            new.topic_name = payload['topicName']
        if 'qos' in payload:
            new.qos = payload['qos']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToIoTCoreRequest'

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
    SystemResourceLimits,
    MessageContext,
    ValidateConfigurationUpdateEvent,
    RunWithInfo,
    PreComponentUpdateEvent,
    PostComponentUpdateEvent,
    MQTTMessage,
    MQTTCredential,
    Metric,
    JsonMessage,
    ConfigurationUpdateEvent,
    CertificateUpdate,
    BinaryMessage,
    LocalDeployment,
    ConfigurationValidityReport,
    ComponentDetails,
    CertificateOptions,
    InvalidArtifactsDirectoryPathError,
    InvalidRecipeDirectoryPathError,
    CreateLocalDeploymentResponse,
    CreateLocalDeploymentRequest,
    PauseComponentResponse,
    PauseComponentRequest,
    StopComponentResponse,
    StopComponentRequest,
    ListLocalDeploymentsResponse,
    ListLocalDeploymentsRequest,
    SubscribeToComponentUpdatesResponse,
    SubscribeToComponentUpdatesRequest,
    ListNamedShadowsForThingResponse,
    ListNamedShadowsForThingRequest,
    UpdateStateResponse,
    UpdateStateRequest,
    GetSecretValueResponse,
    GetSecretValueRequest,
    GetLocalDeploymentStatusResponse,
    GetLocalDeploymentStatusRequest,
    ComponentNotFoundError,
    RestartComponentResponse,
    RestartComponentRequest,
    InvalidTokenError,
    ValidateAuthorizationTokenResponse,
    ValidateAuthorizationTokenRequest,
    FailedUpdateConditionCheckError,
    UpdateConfigurationResponse,
    UpdateConfigurationRequest,
    ConflictError,
    UpdateThingShadowResponse,
    UpdateThingShadowRequest,
    SendConfigurationValidityReportResponse,
    SendConfigurationValidityReportRequest,
    GetThingShadowResponse,
    GetThingShadowRequest,
    CreateDebugPasswordResponse,
    CreateDebugPasswordRequest,
    ListComponentsResponse,
    ListComponentsRequest,
    InvalidClientDeviceAuthTokenError,
    AuthorizeClientDeviceActionResponse,
    AuthorizeClientDeviceActionRequest,
    VerifyClientDeviceIdentityResponse,
    VerifyClientDeviceIdentityRequest,
    SubscribeToCertificateUpdatesResponse,
    SubscribeToCertificateUpdatesRequest,
    PublishToTopicResponse,
    PublishToTopicRequest,
    InvalidCredentialError,
    GetClientDeviceAuthTokenResponse,
    GetClientDeviceAuthTokenRequest,
    GetComponentDetailsResponse,
    GetComponentDetailsRequest,
    SubscribeToTopicResponse,
    SubscribeToTopicRequest,
    GetConfigurationResponse,
    GetConfigurationRequest,
    SubscribeToValidateConfigurationUpdatesResponse,
    SubscribeToValidateConfigurationUpdatesRequest,
    DeferComponentUpdateResponse,
    DeferComponentUpdateRequest,
    PutComponentMetricResponse,
    PutComponentMetricRequest,
    InvalidArgumentsError,
    DeleteThingShadowResponse,
    DeleteThingShadowRequest,
    SubscribeToConfigurationUpdateResponse,
    SubscribeToConfigurationUpdateRequest,
    PublishToIoTCoreResponse,
    PublishToIoTCoreRequest,
    ResourceNotFoundError,
    ResumeComponentResponse,
    ResumeComponentRequest,
    UnauthorizedError,
    ServiceError,
    SubscribeToIoTCoreResponse,
    SubscribeToIoTCoreRequest,
])


class _AuthorizeClientDeviceActionOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#AuthorizeClientDeviceAction'

    @classmethod
    def _request_type(cls):
        return AuthorizeClientDeviceActionRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return AuthorizeClientDeviceActionResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _CreateDebugPasswordOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateDebugPassword'

    @classmethod
    def _request_type(cls):
        return CreateDebugPasswordRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return CreateDebugPasswordResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _CreateLocalDeploymentOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateLocalDeployment'

    @classmethod
    def _request_type(cls):
        return CreateLocalDeploymentRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return CreateLocalDeploymentResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _DeferComponentUpdateOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#DeferComponentUpdate'

    @classmethod
    def _request_type(cls):
        return DeferComponentUpdateRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return DeferComponentUpdateResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _DeleteThingShadowOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#DeleteThingShadow'

    @classmethod
    def _request_type(cls):
        return DeleteThingShadowRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return DeleteThingShadowResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetClientDeviceAuthTokenOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetClientDeviceAuthToken'

    @classmethod
    def _request_type(cls):
        return GetClientDeviceAuthTokenRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetClientDeviceAuthTokenResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetComponentDetailsOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetComponentDetails'

    @classmethod
    def _request_type(cls):
        return GetComponentDetailsRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetComponentDetailsResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetConfigurationOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetConfiguration'

    @classmethod
    def _request_type(cls):
        return GetConfigurationRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetConfigurationResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetLocalDeploymentStatusOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetLocalDeploymentStatus'

    @classmethod
    def _request_type(cls):
        return GetLocalDeploymentStatusRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetLocalDeploymentStatusResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetSecretValueOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetSecretValue'

    @classmethod
    def _request_type(cls):
        return GetSecretValueRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetSecretValueResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _GetThingShadowOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetThingShadow'

    @classmethod
    def _request_type(cls):
        return GetThingShadowRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return GetThingShadowResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _ListComponentsOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListComponents'

    @classmethod
    def _request_type(cls):
        return ListComponentsRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return ListComponentsResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _ListLocalDeploymentsOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListLocalDeployments'

    @classmethod
    def _request_type(cls):
        return ListLocalDeploymentsRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return ListLocalDeploymentsResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _ListNamedShadowsForThingOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListNamedShadowsForThing'

    @classmethod
    def _request_type(cls):
        return ListNamedShadowsForThingRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return ListNamedShadowsForThingResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _PauseComponentOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PauseComponent'

    @classmethod
    def _request_type(cls):
        return PauseComponentRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return PauseComponentResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _PublishToIoTCoreOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishToIoTCore'

    @classmethod
    def _request_type(cls):
        return PublishToIoTCoreRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return PublishToIoTCoreResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _PublishToTopicOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishToTopic'

    @classmethod
    def _request_type(cls):
        return PublishToTopicRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return PublishToTopicResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _PutComponentMetricOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PutComponentMetric'

    @classmethod
    def _request_type(cls):
        return PutComponentMetricRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return PutComponentMetricResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _RestartComponentOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#RestartComponent'

    @classmethod
    def _request_type(cls):
        return RestartComponentRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return RestartComponentResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _ResumeComponentOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ResumeComponent'

    @classmethod
    def _request_type(cls):
        return ResumeComponentRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return ResumeComponentResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _SendConfigurationValidityReportOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SendConfigurationValidityReport'

    @classmethod
    def _request_type(cls):
        return SendConfigurationValidityReportRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SendConfigurationValidityReportResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _StopComponentOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#StopComponent'

    @classmethod
    def _request_type(cls):
        return StopComponentRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return StopComponentResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _SubscribeToCertificateUpdatesOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToCertificateUpdates'

    @classmethod
    def _request_type(cls):
        return SubscribeToCertificateUpdatesRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SubscribeToCertificateUpdatesResponse

    @classmethod
    def _response_stream_type(cls):
        return CertificateUpdateEvent


class _SubscribeToComponentUpdatesOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToComponentUpdates'

    @classmethod
    def _request_type(cls):
        return SubscribeToComponentUpdatesRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SubscribeToComponentUpdatesResponse

    @classmethod
    def _response_stream_type(cls):
        return ComponentUpdatePolicyEvents


class _SubscribeToConfigurationUpdateOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToConfigurationUpdate'

    @classmethod
    def _request_type(cls):
        return SubscribeToConfigurationUpdateRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SubscribeToConfigurationUpdateResponse

    @classmethod
    def _response_stream_type(cls):
        return ConfigurationUpdateEvents


class _SubscribeToIoTCoreOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToIoTCore'

    @classmethod
    def _request_type(cls):
        return SubscribeToIoTCoreRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SubscribeToIoTCoreResponse

    @classmethod
    def _response_stream_type(cls):
        return IoTCoreMessage


class _SubscribeToTopicOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToTopic'

    @classmethod
    def _request_type(cls):
        return SubscribeToTopicRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SubscribeToTopicResponse

    @classmethod
    def _response_stream_type(cls):
        return SubscriptionResponseMessage


class _SubscribeToValidateConfigurationUpdatesOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToValidateConfigurationUpdates'

    @classmethod
    def _request_type(cls):
        return SubscribeToValidateConfigurationUpdatesRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return SubscribeToValidateConfigurationUpdatesResponse

    @classmethod
    def _response_stream_type(cls):
        return ValidateConfigurationUpdateEvents


class _UpdateConfigurationOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateConfiguration'

    @classmethod
    def _request_type(cls):
        return UpdateConfigurationRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return UpdateConfigurationResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _UpdateStateOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateState'

    @classmethod
    def _request_type(cls):
        return UpdateStateRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return UpdateStateResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _UpdateThingShadowOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateThingShadow'

    @classmethod
    def _request_type(cls):
        return UpdateThingShadowRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return UpdateThingShadowResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _ValidateAuthorizationTokenOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateAuthorizationToken'

    @classmethod
    def _request_type(cls):
        return ValidateAuthorizationTokenRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return ValidateAuthorizationTokenResponse

    @classmethod
    def _response_stream_type(cls):
        return None


class _VerifyClientDeviceIdentityOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#VerifyClientDeviceIdentity'

    @classmethod
    def _request_type(cls):
        return VerifyClientDeviceIdentityRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return VerifyClientDeviceIdentityResponse

    @classmethod
    def _response_stream_type(cls):
        return None
