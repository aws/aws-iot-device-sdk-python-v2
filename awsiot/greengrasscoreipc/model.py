# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

import awsiot.eventstreamrpc as rpc
import base64
import datetime
import enum


class GreengrassCoreIPCError(rpc.ErrorShape):

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


class PostComponentUpdateEvent(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment_id=None):
        super().__init__()
        self.deployment_id = deployment_id

    def _to_payload(self):
        payload = {}
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PostComponentUpdateEvent'

    def __repr__(self):
        attrs = []
        for attr in ['deployment_id']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PostComponentUpdateEvent):
            return self.__dict__ == other.__dict__
        return False


class PreComponentUpdateEvent(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment_id=None,
                 is_ggc_restarting=None):
        super().__init__()
        self.deployment_id = deployment_id
        self.is_ggc_restarting = is_ggc_restarting

    def _to_payload(self):
        payload = {}
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        if self.is_ggc_restarting is None:
            if self.is_explicitly_null('is_ggc_restarting'):
                payload['isGgcRestarting'] = None
        else:
            payload['isGgcRestarting'] = self.is_ggc_restarting
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        if 'isGgcRestarting' in payload:
            if payload['isGgcRestarting'] is None:
                new.set_explicitly_null('is_ggc_restarting')
            else:
                new.is_ggc_restarting = payload['isGgcRestarting']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PreComponentUpdateEvent'

    def __repr__(self):
        attrs = []
        for attr in ['deployment_id', 'is_ggc_restarting']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PreComponentUpdateEvent):
            return self.__dict__ == other.__dict__
        return False


class LifecycleState(enum.Enum):
    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'
    NEW = 'NEW'
    FINISHED = 'FINISHED'
    INSTALLED = 'INSTALLED'
    BROKEN = 'BROKEN'
    STARTING = 'STARTING'
    STOPPING = 'STOPPING'

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


class DeploymentStatus(enum.Enum):
    QUEUED = 'QUEUED'
    IN_PROGRESS = 'IN_PROGRESS'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'

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


class ValidateConfigurationUpdateEvent(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 configuration=None,
                 deployment_id=None):
        super().__init__()
        self.configuration = configuration
        self.deployment_id = deployment_id

    def _to_payload(self):
        payload = {}
        if self.configuration is None:
            if self.is_explicitly_null('configuration'):
                payload['configuration'] = None
        else:
            payload['configuration'] = self.configuration
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'configuration' in payload:
            if payload['configuration'] is None:
                new.set_explicitly_null('configuration')
            else:
                new.configuration = payload['configuration']
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateConfigurationUpdateEvent'

    def __repr__(self):
        attrs = []
        for attr in ['configuration', 'deployment_id']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ValidateConfigurationUpdateEvent):
            return self.__dict__ == other.__dict__
        return False


class ConfigurationValidityStatus(enum.Enum):
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

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


class ConfigurationUpdateEvent(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None,
                 key_path=None):
        super().__init__()
        self.component_name = component_name
        self.key_path = key_path

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        if self.key_path is None:
            if self.is_explicitly_null('key_path'):
                payload['keyPath'] = None
        else:
            payload['keyPath'] = self.key_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        if 'keyPath' in payload:
            if payload['keyPath'] is None:
                new.set_explicitly_null('key_path')
            else:
                new.key_path = payload['keyPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConfigurationUpdateEvent'

    def __repr__(self):
        attrs = []
        for attr in ['component_name', 'key_path']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ConfigurationUpdateEvent):
            return self.__dict__ == other.__dict__
        return False


class BinaryMessage(rpc.Shape, _ExplicitlyNullMixin):

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
            payload['message'] = base64.b64encode(self.message).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = base64.b64decode(payload['message'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#BinaryMessage'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, BinaryMessage):
            return self.__dict__ == other.__dict__
        return False


class JsonMessage(rpc.Shape, _ExplicitlyNullMixin):

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
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#JsonMessage'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, JsonMessage):
            return self.__dict__ == other.__dict__
        return False


class MQTTMessage(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 topic_name=None,
                 payload=None):
        super().__init__()
        self.topic_name = topic_name
        self.payload = payload

    def _to_payload(self):
        payload = {}
        if self.topic_name is None:
            if self.is_explicitly_null('topic_name'):
                payload['topicName'] = None
        else:
            payload['topicName'] = self.topic_name
        if self.payload is None:
            if self.is_explicitly_null('payload'):
                payload['payload'] = None
        else:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            if payload['topicName'] is None:
                new.set_explicitly_null('topic_name')
            else:
                new.topic_name = payload['topicName']
        if 'payload' in payload:
            if payload['payload'] is None:
                new.set_explicitly_null('payload')
            else:
                new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#MQTTMessage'

    def __repr__(self):
        attrs = []
        for attr in ['topic_name', 'payload']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, MQTTMessage):
            return self.__dict__ == other.__dict__
        return False


class ComponentUpdatePolicyEvents(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 pre_update_event=None,
                 post_update_event=None):
        super().__init__()
        self.pre_update_event = None
        self.post_update_event = None
        if pre_update_event is not None:
            self.pre_update_event = pre_update_event
        if post_update_event is not None:
            self.post_update_event = post_update_event

    def _to_payload(self):
        payload = {}
        if self.pre_update_event is not None and self._active_union_attr == 'pre_update_event':
            payload['preUpdateEvent'] = self.pre_update_event._to_payload()
        if self.post_update_event is not None and self._active_union_attr == 'post_update_event':
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
        for attr in ['pre_update_event', 'post_update_event']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ComponentUpdatePolicyEvents):
            return self.__dict__ == other.__dict__
        return False


class ComponentDetails(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None,
                 version=None,
                 state=None,
                 configuration=None):
        super().__init__()
        self.component_name = component_name
        self.version = version
        self.state = state
        self.configuration = configuration

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        if self.version is None:
            if self.is_explicitly_null('version'):
                payload['version'] = None
        else:
            payload['version'] = self.version
        if self.state is None:
            if self.is_explicitly_null('state'):
                payload['state'] = None
        else:
            payload['state'] = self.state._to_payload()
        if self.configuration is None:
            if self.is_explicitly_null('configuration'):
                payload['configuration'] = None
        else:
            payload['configuration'] = self.configuration
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        if 'version' in payload:
            if payload['version'] is None:
                new.set_explicitly_null('version')
            else:
                new.version = payload['version']
        if 'state' in payload:
            if payload['state'] is None:
                new.set_explicitly_null('state')
            else:
                new.state = LifecycleState._from_payload(payload['state'])
        if 'configuration' in payload:
            if payload['configuration'] is None:
                new.set_explicitly_null('configuration')
            else:
                new.configuration = payload['configuration']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ComponentDetails'

    def __repr__(self):
        attrs = []
        for attr in ['component_name', 'version', 'state', 'configuration']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ComponentDetails):
            return self.__dict__ == other.__dict__
        return False


class SubscriptionResponseMessage(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 json_message=None,
                 binary_message=None):
        super().__init__()
        self.json_message = None
        self.binary_message = None
        if json_message is not None:
            self.json_message = json_message
        if binary_message is not None:
            self.binary_message = binary_message

    def _to_payload(self):
        payload = {}
        if self.json_message is not None and self._active_union_attr == 'json_message':
            payload['jsonMessage'] = self.json_message._to_payload()
        if self.binary_message is not None and self._active_union_attr == 'binary_message':
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
        for attr in ['json_message', 'binary_message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscriptionResponseMessage):
            return self.__dict__ == other.__dict__
        return False


class ReportedLifecycleState(enum.Enum):
    RUNNING = 'RUNNING'
    ERRORED = 'ERRORED'

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


class SecretValue(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 secret_string=None,
                 secret_binary=None):
        super().__init__()
        self.secret_string = None
        self.secret_binary = None
        if secret_string is not None:
            self.secret_string = secret_string
        if secret_binary is not None:
            self.secret_binary = secret_binary

    def _to_payload(self):
        payload = {}
        if self.secret_string is not None and self._active_union_attr == 'secret_string':
            payload['secretString'] = self.secret_string
        if self.secret_binary is not None and self._active_union_attr == 'secret_binary':
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
        for attr in ['secret_string', 'secret_binary']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SecretValue):
            return self.__dict__ == other.__dict__
        return False


class LocalDeployment(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment_id=None,
                 status=None):
        super().__init__()
        self.deployment_id = deployment_id
        self.status = status

    def _to_payload(self):
        payload = {}
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        if self.status is None:
            if self.is_explicitly_null('status'):
                payload['status'] = None
        else:
            payload['status'] = self.status._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        if 'status' in payload:
            if payload['status'] is None:
                new.set_explicitly_null('status')
            else:
                new.status = DeploymentStatus._from_payload(payload['status'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#LocalDeployment'

    def __repr__(self):
        attrs = []
        for attr in ['deployment_id', 'status']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, LocalDeployment):
            return self.__dict__ == other.__dict__
        return False


class RequestStatus(enum.Enum):
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'

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


class ValidateConfigurationUpdateEvents(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 validate_configuration_update_event=None):
        super().__init__()
        self.validate_configuration_update_event = None
        if validate_configuration_update_event is not None:
            self.validate_configuration_update_event = validate_configuration_update_event

    def _to_payload(self):
        payload = {}
        if self.validate_configuration_update_event is not None and self._active_union_attr == 'validate_configuration_update_event':
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
        for attr in ['validate_configuration_update_event']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ValidateConfigurationUpdateEvents):
            return self.__dict__ == other.__dict__
        return False


class ConfigurationValidityReport(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 status=None,
                 deployment_id=None,
                 message=None):
        super().__init__()
        self.status = status
        self.deployment_id = deployment_id
        self.message = message

    def _to_payload(self):
        payload = {}
        if self.status is None:
            if self.is_explicitly_null('status'):
                payload['status'] = None
        else:
            payload['status'] = self.status._to_payload()
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'status' in payload:
            if payload['status'] is None:
                new.set_explicitly_null('status')
            else:
                new.status = ConfigurationValidityStatus._from_payload(payload['status'])
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConfigurationValidityReport'

    def __repr__(self):
        attrs = []
        for attr in ['status', 'deployment_id', 'message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ConfigurationValidityReport):
            return self.__dict__ == other.__dict__
        return False


class ConfigurationUpdateEvents(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 configuration_update_event=None):
        super().__init__()
        self.configuration_update_event = None
        if configuration_update_event is not None:
            self.configuration_update_event = configuration_update_event

    def _to_payload(self):
        payload = {}
        if self.configuration_update_event is not None and self._active_union_attr == 'configuration_update_event':
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
        for attr in ['configuration_update_event']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ConfigurationUpdateEvents):
            return self.__dict__ == other.__dict__
        return False


class PublishMessage(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 json_message=None,
                 binary_message=None):
        super().__init__()
        self.json_message = None
        self.binary_message = None
        if json_message is not None:
            self.json_message = json_message
        if binary_message is not None:
            self.binary_message = binary_message

    def _to_payload(self):
        payload = {}
        if self.json_message is not None and self._active_union_attr == 'json_message':
            payload['jsonMessage'] = self.json_message._to_payload()
        if self.binary_message is not None and self._active_union_attr == 'binary_message':
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
        for attr in ['json_message', 'binary_message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PublishMessage):
            return self.__dict__ == other.__dict__
        return False


class IoTCoreMessage(rpc.Shape, _UnionMixin):
    """
    This is a "tagged union" class.

    When any attribute's value is set, all other attributes' values will
    become None.
    """
    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = None
        if message is not None:
            self.message = message

    def _to_payload(self):
        payload = {}
        if self.message is not None and self._active_union_attr == 'message':
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
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, IoTCoreMessage):
            return self.__dict__ == other.__dict__
        return False


class QOS(enum.Enum):
    AT_MOST_ONCE = '0'
    AT_LEAST_ONCE = '1'

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


class CreateLocalDeploymentResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment_id=None):
        super().__init__()
        self.deployment_id = deployment_id

    def _to_payload(self):
        payload = {}
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateLocalDeploymentResponse'

    def __repr__(self):
        attrs = []
        for attr in ['deployment_id']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, CreateLocalDeploymentResponse):
            return self.__dict__ == other.__dict__
        return False


class CreateLocalDeploymentRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 group_name=None,
                 root_component_versions_to_add=None,
                 root_components_to_remove=None,
                 component_to_configuration=None,
                 component_to_run_with_info=None):
        super().__init__()
        self.group_name = group_name
        self.root_component_versions_to_add = root_component_versions_to_add
        self.root_components_to_remove = root_components_to_remove
        self.component_to_configuration = component_to_configuration
        self.component_to_run_with_info = component_to_run_with_info

    def _to_payload(self):
        payload = {}
        if self.group_name is None:
            if self.is_explicitly_null('group_name'):
                payload['groupName'] = None
        else:
            payload['groupName'] = self.group_name
        if self.root_component_versions_to_add is None:
            if self.is_explicitly_null('root_component_versions_to_add'):
                payload['rootComponentVersionsToAdd'] = None
        else:
            payload['rootComponentVersionsToAdd'] = self.root_component_versions_to_add
        if self.root_components_to_remove is None:
            if self.is_explicitly_null('root_components_to_remove'):
                payload['rootComponentsToRemove'] = None
        else:
            payload['rootComponentsToRemove'] = self.root_components_to_remove
        if self.component_to_configuration is None:
            if self.is_explicitly_null('component_to_configuration'):
                payload['componentToConfiguration'] = None
        else:
            payload['componentToConfiguration'] = self.component_to_configuration
        if self.component_to_run_with_info is None:
            if self.is_explicitly_null('component_to_run_with_info'):
                payload['componentToRunWithInfo'] = None
        else:
            payload['componentToRunWithInfo'] = {k: v._to_payload() for k, v in self.component_to_run_with_info.items()}
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'groupName' in payload:
            if payload['groupName'] is None:
                new.set_explicitly_null('group_name')
            else:
                new.group_name = payload['groupName']
        if 'rootComponentVersionsToAdd' in payload:
            if payload['rootComponentVersionsToAdd'] is None:
                new.set_explicitly_null('root_component_versions_to_add')
            else:
                new.root_component_versions_to_add = payload['rootComponentVersionsToAdd']
        if 'rootComponentsToRemove' in payload:
            if payload['rootComponentsToRemove'] is None:
                new.set_explicitly_null('root_components_to_remove')
            else:
                new.root_components_to_remove = payload['rootComponentsToRemove']
        if 'componentToConfiguration' in payload:
            if payload['componentToConfiguration'] is None:
                new.set_explicitly_null('component_to_configuration')
            else:
                new.component_to_configuration = payload['componentToConfiguration']
        if 'componentToRunWithInfo' in payload:
            if payload['componentToRunWithInfo'] is None:
                new.set_explicitly_null('component_to_run_with_info')
            else:
                new.component_to_run_with_info = {k: RunWithInfo._from_payload(v) for k,v in payload['componentToRunWithInfo'].items()}
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateLocalDeploymentRequest'

    def __repr__(self):
        attrs = []
        for attr in ['group_name', 'root_component_versions_to_add', 'root_components_to_remove', 'component_to_configuration', 'component_to_run_with_info']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, CreateLocalDeploymentRequest):
            return self.__dict__ == other.__dict__
        return False


class StopComponentResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 stop_status=None,
                 message=None):
        super().__init__()
        self.stop_status = stop_status
        self.message = message

    def _to_payload(self):
        payload = {}
        if self.stop_status is None:
            if self.is_explicitly_null('stop_status'):
                payload['stopStatus'] = None
        else:
            payload['stopStatus'] = self.stop_status._to_payload()
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'stopStatus' in payload:
            if payload['stopStatus'] is None:
                new.set_explicitly_null('stop_status')
            else:
                new.stop_status = RequestStatus._from_payload(payload['stopStatus'])
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#StopComponentResponse'

    def __repr__(self):
        attrs = []
        for attr in ['stop_status', 'message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, StopComponentResponse):
            return self.__dict__ == other.__dict__
        return False


class StopComponentRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None):
        super().__init__()
        self.component_name = component_name

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#StopComponentRequest'

    def __repr__(self):
        attrs = []
        for attr in ['component_name']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, StopComponentRequest):
            return self.__dict__ == other.__dict__
        return False


class ListLocalDeploymentsResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 local_deployments=None):
        super().__init__()
        self.local_deployments = local_deployments

    def _to_payload(self):
        payload = {}
        if self.local_deployments is None:
            if self.is_explicitly_null('local_deployments'):
                payload['localDeployments'] = None
        else:
            payload['localDeployments'] = [i._to_payload() for i in self.local_deployments]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'localDeployments' in payload:
            if payload['localDeployments'] is None:
                new.set_explicitly_null('local_deployments')
            else:
                new.local_deployments = [LocalDeployment._from_payload(i) for i in payload['localDeployments']]
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListLocalDeploymentsResponse'

    def __repr__(self):
        attrs = []
        for attr in ['local_deployments']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ListLocalDeploymentsResponse):
            return self.__dict__ == other.__dict__
        return False


class ListLocalDeploymentsRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ListLocalDeploymentsRequest):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToComponentUpdatesResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToComponentUpdatesResponse):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToComponentUpdatesRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToComponentUpdatesRequest):
            return self.__dict__ == other.__dict__
        return False


class GetComponentDetailsResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_details=None):
        super().__init__()
        self.component_details = component_details

    def _to_payload(self):
        payload = {}
        if self.component_details is None:
            if self.is_explicitly_null('component_details'):
                payload['componentDetails'] = None
        else:
            payload['componentDetails'] = self.component_details._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentDetails' in payload:
            if payload['componentDetails'] is None:
                new.set_explicitly_null('component_details')
            else:
                new.component_details = ComponentDetails._from_payload(payload['componentDetails'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetComponentDetailsResponse'

    def __repr__(self):
        attrs = []
        for attr in ['component_details']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetComponentDetailsResponse):
            return self.__dict__ == other.__dict__
        return False


class GetComponentDetailsRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None):
        super().__init__()
        self.component_name = component_name

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetComponentDetailsRequest'

    def __repr__(self):
        attrs = []
        for attr in ['component_name']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetComponentDetailsRequest):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToTopicResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 topic_name=None):
        super().__init__()
        self.topic_name = topic_name

    def _to_payload(self):
        payload = {}
        if self.topic_name is None:
            if self.is_explicitly_null('topic_name'):
                payload['topicName'] = None
        else:
            payload['topicName'] = self.topic_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            if payload['topicName'] is None:
                new.set_explicitly_null('topic_name')
            else:
                new.topic_name = payload['topicName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToTopicResponse'

    def __repr__(self):
        attrs = []
        for attr in ['topic_name']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToTopicResponse):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToTopicRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 topic=None):
        super().__init__()
        self.topic = topic

    def _to_payload(self):
        payload = {}
        if self.topic is None:
            if self.is_explicitly_null('topic'):
                payload['topic'] = None
        else:
            payload['topic'] = self.topic
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topic' in payload:
            if payload['topic'] is None:
                new.set_explicitly_null('topic')
            else:
                new.topic = payload['topic']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToTopicRequest'

    def __repr__(self):
        attrs = []
        for attr in ['topic']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToTopicRequest):
            return self.__dict__ == other.__dict__
        return False


class GetConfigurationResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None,
                 value=None):
        super().__init__()
        self.component_name = component_name
        self.value = value

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        if self.value is None:
            if self.is_explicitly_null('value'):
                payload['value'] = None
        else:
            payload['value'] = self.value
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        if 'value' in payload:
            if payload['value'] is None:
                new.set_explicitly_null('value')
            else:
                new.value = payload['value']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetConfigurationResponse'

    def __repr__(self):
        attrs = []
        for attr in ['component_name', 'value']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetConfigurationResponse):
            return self.__dict__ == other.__dict__
        return False


class GetConfigurationRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None,
                 key_path=None):
        super().__init__()
        self.component_name = component_name
        self.key_path = key_path

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        if self.key_path is None:
            if self.is_explicitly_null('key_path'):
                payload['keyPath'] = None
        else:
            payload['keyPath'] = self.key_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        if 'keyPath' in payload:
            if payload['keyPath'] is None:
                new.set_explicitly_null('key_path')
            else:
                new.key_path = payload['keyPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetConfigurationRequest'

    def __repr__(self):
        attrs = []
        for attr in ['component_name', 'key_path']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetConfigurationRequest):
            return self.__dict__ == other.__dict__
        return False


class UpdateStateResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UpdateStateResponse):
            return self.__dict__ == other.__dict__
        return False


class UpdateStateRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 state=None):
        super().__init__()
        self.state = state

    def _to_payload(self):
        payload = {}
        if self.state is None:
            if self.is_explicitly_null('state'):
                payload['state'] = None
        else:
            payload['state'] = self.state._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'state' in payload:
            if payload['state'] is None:
                new.set_explicitly_null('state')
            else:
                new.state = ReportedLifecycleState._from_payload(payload['state'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateStateRequest'

    def __repr__(self):
        attrs = []
        for attr in ['state']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UpdateStateRequest):
            return self.__dict__ == other.__dict__
        return False


class GetSecretValueResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 secret_id=None,
                 version_id=None,
                 version_stage=None,
                 secret_value=None):
        super().__init__()
        self.secret_id = secret_id
        self.version_id = version_id
        self.version_stage = version_stage
        self.secret_value = secret_value

    def _to_payload(self):
        payload = {}
        if self.secret_id is None:
            if self.is_explicitly_null('secret_id'):
                payload['secretId'] = None
        else:
            payload['secretId'] = self.secret_id
        if self.version_id is None:
            if self.is_explicitly_null('version_id'):
                payload['versionId'] = None
        else:
            payload['versionId'] = self.version_id
        if self.version_stage is None:
            if self.is_explicitly_null('version_stage'):
                payload['versionStage'] = None
        else:
            payload['versionStage'] = self.version_stage
        if self.secret_value is None:
            if self.is_explicitly_null('secret_value'):
                payload['secretValue'] = None
        else:
            payload['secretValue'] = self.secret_value._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'secretId' in payload:
            if payload['secretId'] is None:
                new.set_explicitly_null('secret_id')
            else:
                new.secret_id = payload['secretId']
        if 'versionId' in payload:
            if payload['versionId'] is None:
                new.set_explicitly_null('version_id')
            else:
                new.version_id = payload['versionId']
        if 'versionStage' in payload:
            if payload['versionStage'] is None:
                new.set_explicitly_null('version_stage')
            else:
                new.version_stage = payload['versionStage']
        if 'secretValue' in payload:
            if payload['secretValue'] is None:
                new.set_explicitly_null('secret_value')
            else:
                new.secret_value = SecretValue._from_payload(payload['secretValue'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetSecretValueResponse'

    def __repr__(self):
        attrs = []
        for attr in ['secret_id', 'version_id', 'version_stage', 'secret_value']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetSecretValueResponse):
            return self.__dict__ == other.__dict__
        return False


class GetSecretValueRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 secret_id=None,
                 version_id=None,
                 version_stage=None):
        super().__init__()
        self.secret_id = secret_id
        self.version_id = version_id
        self.version_stage = version_stage

    def _to_payload(self):
        payload = {}
        if self.secret_id is None:
            if self.is_explicitly_null('secret_id'):
                payload['secretId'] = None
        else:
            payload['secretId'] = self.secret_id
        if self.version_id is None:
            if self.is_explicitly_null('version_id'):
                payload['versionId'] = None
        else:
            payload['versionId'] = self.version_id
        if self.version_stage is None:
            if self.is_explicitly_null('version_stage'):
                payload['versionStage'] = None
        else:
            payload['versionStage'] = self.version_stage
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'secretId' in payload:
            if payload['secretId'] is None:
                new.set_explicitly_null('secret_id')
            else:
                new.secret_id = payload['secretId']
        if 'versionId' in payload:
            if payload['versionId'] is None:
                new.set_explicitly_null('version_id')
            else:
                new.version_id = payload['versionId']
        if 'versionStage' in payload:
            if payload['versionStage'] is None:
                new.set_explicitly_null('version_stage')
            else:
                new.version_stage = payload['versionStage']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetSecretValueRequest'

    def __repr__(self):
        attrs = []
        for attr in ['secret_id', 'version_id', 'version_stage']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetSecretValueRequest):
            return self.__dict__ == other.__dict__
        return False


class GetLocalDeploymentStatusResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment=None):
        super().__init__()
        self.deployment = deployment

    def _to_payload(self):
        payload = {}
        if self.deployment is None:
            if self.is_explicitly_null('deployment'):
                payload['deployment'] = None
        else:
            payload['deployment'] = self.deployment._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deployment' in payload:
            if payload['deployment'] is None:
                new.set_explicitly_null('deployment')
            else:
                new.deployment = LocalDeployment._from_payload(payload['deployment'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetLocalDeploymentStatusResponse'

    def __repr__(self):
        attrs = []
        for attr in ['deployment']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetLocalDeploymentStatusResponse):
            return self.__dict__ == other.__dict__
        return False


class GetLocalDeploymentStatusRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment_id=None):
        super().__init__()
        self.deployment_id = deployment_id

    def _to_payload(self):
        payload = {}
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#GetLocalDeploymentStatusRequest'

    def __repr__(self):
        attrs = []
        for attr in ['deployment_id']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, GetLocalDeploymentStatusRequest):
            return self.__dict__ == other.__dict__
        return False


class ComponentNotFoundError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ComponentNotFoundError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ComponentNotFoundError):
            return self.__dict__ == other.__dict__
        return False


class RestartComponentResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 restart_status=None,
                 message=None):
        super().__init__()
        self.restart_status = restart_status
        self.message = message

    def _to_payload(self):
        payload = {}
        if self.restart_status is None:
            if self.is_explicitly_null('restart_status'):
                payload['restartStatus'] = None
        else:
            payload['restartStatus'] = self.restart_status._to_payload()
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'restartStatus' in payload:
            if payload['restartStatus'] is None:
                new.set_explicitly_null('restart_status')
            else:
                new.restart_status = RequestStatus._from_payload(payload['restartStatus'])
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#RestartComponentResponse'

    def __repr__(self):
        attrs = []
        for attr in ['restart_status', 'message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, RestartComponentResponse):
            return self.__dict__ == other.__dict__
        return False


class RestartComponentRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None):
        super().__init__()
        self.component_name = component_name

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#RestartComponentRequest'

    def __repr__(self):
        attrs = []
        for attr in ['component_name']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, RestartComponentRequest):
            return self.__dict__ == other.__dict__
        return False


class InvalidArtifactsDirectoryPathError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidArtifactsDirectoryPathError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, InvalidArtifactsDirectoryPathError):
            return self.__dict__ == other.__dict__
        return False


class InvalidRecipeDirectoryPathError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidRecipeDirectoryPathError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, InvalidRecipeDirectoryPathError):
            return self.__dict__ == other.__dict__
        return False


class UpdateRecipesAndArtifactsResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        return 'aws.greengrass#UpdateRecipesAndArtifactsResponse'

    def __repr__(self):
        attrs = []
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UpdateRecipesAndArtifactsResponse):
            return self.__dict__ == other.__dict__
        return False


class UpdateRecipesAndArtifactsRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 recipe_directory_path=None,
                 artifacts_directory_path=None):
        super().__init__()
        self.recipe_directory_path = recipe_directory_path
        self.artifacts_directory_path = artifacts_directory_path

    def _to_payload(self):
        payload = {}
        if self.recipe_directory_path is None:
            if self.is_explicitly_null('recipe_directory_path'):
                payload['recipeDirectoryPath'] = None
        else:
            payload['recipeDirectoryPath'] = self.recipe_directory_path
        if self.artifacts_directory_path is None:
            if self.is_explicitly_null('artifacts_directory_path'):
                payload['artifactsDirectoryPath'] = None
        else:
            payload['artifactsDirectoryPath'] = self.artifacts_directory_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'recipeDirectoryPath' in payload:
            if payload['recipeDirectoryPath'] is None:
                new.set_explicitly_null('recipe_directory_path')
            else:
                new.recipe_directory_path = payload['recipeDirectoryPath']
        if 'artifactsDirectoryPath' in payload:
            if payload['artifactsDirectoryPath'] is None:
                new.set_explicitly_null('artifacts_directory_path')
            else:
                new.artifacts_directory_path = payload['artifactsDirectoryPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateRecipesAndArtifactsRequest'

    def __repr__(self):
        attrs = []
        for attr in ['recipe_directory_path', 'artifacts_directory_path']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UpdateRecipesAndArtifactsRequest):
            return self.__dict__ == other.__dict__
        return False


class InvalidTokenError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'server'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidTokenError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, InvalidTokenError):
            return self.__dict__ == other.__dict__
        return False


class ValidateAuthorizationTokenResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 is_valid=None):
        super().__init__()
        self.is_valid = is_valid

    def _to_payload(self):
        payload = {}
        if self.is_valid is None:
            if self.is_explicitly_null('is_valid'):
                payload['isValid'] = None
        else:
            payload['isValid'] = self.is_valid
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'isValid' in payload:
            if payload['isValid'] is None:
                new.set_explicitly_null('is_valid')
            else:
                new.is_valid = payload['isValid']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateAuthorizationTokenResponse'

    def __repr__(self):
        attrs = []
        for attr in ['is_valid']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ValidateAuthorizationTokenResponse):
            return self.__dict__ == other.__dict__
        return False


class ValidateAuthorizationTokenRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 token=None):
        super().__init__()
        self.token = token

    def _to_payload(self):
        payload = {}
        if self.token is None:
            if self.is_explicitly_null('token'):
                payload['token'] = None
        else:
            payload['token'] = self.token
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'token' in payload:
            if payload['token'] is None:
                new.set_explicitly_null('token')
            else:
                new.token = payload['token']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ValidateAuthorizationTokenRequest'

    def __repr__(self):
        attrs = []
        for attr in ['token']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ValidateAuthorizationTokenRequest):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToValidateConfigurationUpdatesResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToValidateConfigurationUpdatesResponse):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToValidateConfigurationUpdatesRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToValidateConfigurationUpdatesRequest):
            return self.__dict__ == other.__dict__
        return False


class FailedUpdateConditionCheckError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#FailedUpdateConditionCheckError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, FailedUpdateConditionCheckError):
            return self.__dict__ == other.__dict__
        return False


class ConflictError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ConflictError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ConflictError):
            return self.__dict__ == other.__dict__
        return False


class UpdateConfigurationResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UpdateConfigurationResponse):
            return self.__dict__ == other.__dict__
        return False


class UpdateConfigurationRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 key_path=None,
                 timestamp=None,
                 value_to_merge=None):
        super().__init__()
        self.key_path = key_path
        self.timestamp = timestamp
        self.value_to_merge = value_to_merge

    def _to_payload(self):
        payload = {}
        if self.key_path is None:
            if self.is_explicitly_null('key_path'):
                payload['keyPath'] = None
        else:
            payload['keyPath'] = self.key_path
        if self.timestamp is None:
            if self.is_explicitly_null('timestamp'):
                payload['timestamp'] = None
        else:
            payload['timestamp'] = self.timestamp.timestamp()
        if self.value_to_merge is None:
            if self.is_explicitly_null('value_to_merge'):
                payload['valueToMerge'] = None
        else:
            payload['valueToMerge'] = self.value_to_merge
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'keyPath' in payload:
            if payload['keyPath'] is None:
                new.set_explicitly_null('key_path')
            else:
                new.key_path = payload['keyPath']
        if 'timestamp' in payload:
            if payload['timestamp'] is None:
                new.set_explicitly_null('timestamp')
            else:
                new.timestamp = datetime.datetime.fromtimestamp(payload['timestamp'], datetime.timezone.utc)
        if 'valueToMerge' in payload:
            if payload['valueToMerge'] is None:
                new.set_explicitly_null('value_to_merge')
            else:
                new.value_to_merge = payload['valueToMerge']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateConfigurationRequest'

    def __repr__(self):
        attrs = []
        for attr in ['key_path', 'timestamp', 'value_to_merge']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UpdateConfigurationRequest):
            return self.__dict__ == other.__dict__
        return False


class SendConfigurationValidityReportResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SendConfigurationValidityReportResponse):
            return self.__dict__ == other.__dict__
        return False


class SendConfigurationValidityReportRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 configuration_validity_report=None):
        super().__init__()
        self.configuration_validity_report = configuration_validity_report

    def _to_payload(self):
        payload = {}
        if self.configuration_validity_report is None:
            if self.is_explicitly_null('configuration_validity_report'):
                payload['configurationValidityReport'] = None
        else:
            payload['configurationValidityReport'] = self.configuration_validity_report._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'configurationValidityReport' in payload:
            if payload['configurationValidityReport'] is None:
                new.set_explicitly_null('configuration_validity_report')
            else:
                new.configuration_validity_report = ConfigurationValidityReport._from_payload(payload['configurationValidityReport'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SendConfigurationValidityReportRequest'

    def __repr__(self):
        attrs = []
        for attr in ['configuration_validity_report']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SendConfigurationValidityReportRequest):
            return self.__dict__ == other.__dict__
        return False


class InvalidArgumentsError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#InvalidArgumentsError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, InvalidArgumentsError):
            return self.__dict__ == other.__dict__
        return False


class DeferComponentUpdateResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, DeferComponentUpdateResponse):
            return self.__dict__ == other.__dict__
        return False


class DeferComponentUpdateRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 deployment_id=None,
                 message=None,
                 recheck_after_ms=None):
        super().__init__()
        self.deployment_id = deployment_id
        self.message = message
        self.recheck_after_ms = recheck_after_ms

    def _to_payload(self):
        payload = {}
        if self.deployment_id is None:
            if self.is_explicitly_null('deployment_id'):
                payload['deploymentId'] = None
        else:
            payload['deploymentId'] = self.deployment_id
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        if self.recheck_after_ms is None:
            if self.is_explicitly_null('recheck_after_ms'):
                payload['recheckAfterMs'] = None
        else:
            payload['recheckAfterMs'] = self.recheck_after_ms
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'deploymentId' in payload:
            if payload['deploymentId'] is None:
                new.set_explicitly_null('deployment_id')
            else:
                new.deployment_id = payload['deploymentId']
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        if 'recheckAfterMs' in payload:
            if payload['recheckAfterMs'] is None:
                new.set_explicitly_null('recheck_after_ms')
            else:
                new.recheck_after_ms = int(payload['recheckAfterMs'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#DeferComponentUpdateRequest'

    def __repr__(self):
        attrs = []
        for attr in ['deployment_id', 'message', 'recheck_after_ms']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, DeferComponentUpdateRequest):
            return self.__dict__ == other.__dict__
        return False


class CreateDebugPasswordResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 password=None,
                 username=None,
                 password_expiration=None):
        super().__init__()
        self.password = password
        self.username = username
        self.password_expiration = password_expiration

    def _to_payload(self):
        payload = {}
        if self.password is None:
            if self.is_explicitly_null('password'):
                payload['password'] = None
        else:
            payload['password'] = self.password
        if self.username is None:
            if self.is_explicitly_null('username'):
                payload['username'] = None
        else:
            payload['username'] = self.username
        if self.password_expiration is None:
            if self.is_explicitly_null('password_expiration'):
                payload['passwordExpiration'] = None
        else:
            payload['passwordExpiration'] = self.password_expiration.timestamp()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'password' in payload:
            if payload['password'] is None:
                new.set_explicitly_null('password')
            else:
                new.password = payload['password']
        if 'username' in payload:
            if payload['username'] is None:
                new.set_explicitly_null('username')
            else:
                new.username = payload['username']
        if 'passwordExpiration' in payload:
            if payload['passwordExpiration'] is None:
                new.set_explicitly_null('password_expiration')
            else:
                new.password_expiration = datetime.datetime.fromtimestamp(payload['passwordExpiration'], datetime.timezone.utc)
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#CreateDebugPasswordResponse'

    def __repr__(self):
        attrs = []
        for attr in ['password', 'username', 'password_expiration']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, CreateDebugPasswordResponse):
            return self.__dict__ == other.__dict__
        return False


class CreateDebugPasswordRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, CreateDebugPasswordRequest):
            return self.__dict__ == other.__dict__
        return False


class ListComponentsResponse(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 components=None):
        super().__init__()
        self.components = components

    def _to_payload(self):
        payload = {}
        if self.components is None:
            if self.is_explicitly_null('components'):
                payload['components'] = None
        else:
            payload['components'] = [i._to_payload() for i in self.components]
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'components' in payload:
            if payload['components'] is None:
                new.set_explicitly_null('components')
            else:
                new.components = [ComponentDetails._from_payload(i) for i in payload['components']]
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ListComponentsResponse'

    def __repr__(self):
        attrs = []
        for attr in ['components']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ListComponentsResponse):
            return self.__dict__ == other.__dict__
        return False


class ListComponentsRequest(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ListComponentsRequest):
            return self.__dict__ == other.__dict__
        return False


class ResourceNotFoundError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None,
                 resource_type=None,
                 resource_name=None):
        super().__init__()
        self.message = message
        self.resource_type = resource_type
        self.resource_name = resource_name

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        if self.resource_type is None:
            if self.is_explicitly_null('resource_type'):
                payload['resourceType'] = None
        else:
            payload['resourceType'] = self.resource_type
        if self.resource_name is None:
            if self.is_explicitly_null('resource_name'):
                payload['resourceName'] = None
        else:
            payload['resourceName'] = self.resource_name
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        if 'resourceType' in payload:
            if payload['resourceType'] is None:
                new.set_explicitly_null('resource_type')
            else:
                new.resource_type = payload['resourceType']
        if 'resourceName' in payload:
            if payload['resourceName'] is None:
                new.set_explicitly_null('resource_name')
            else:
                new.resource_name = payload['resourceName']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ResourceNotFoundError'

    def __repr__(self):
        attrs = []
        for attr in ['message', 'resource_type', 'resource_name']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ResourceNotFoundError):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToConfigurationUpdateResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToConfigurationUpdateResponse):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToConfigurationUpdateRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 component_name=None,
                 key_path=None):
        super().__init__()
        self.component_name = component_name
        self.key_path = key_path

    def _to_payload(self):
        payload = {}
        if self.component_name is None:
            if self.is_explicitly_null('component_name'):
                payload['componentName'] = None
        else:
            payload['componentName'] = self.component_name
        if self.key_path is None:
            if self.is_explicitly_null('key_path'):
                payload['keyPath'] = None
        else:
            payload['keyPath'] = self.key_path
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'componentName' in payload:
            if payload['componentName'] is None:
                new.set_explicitly_null('component_name')
            else:
                new.component_name = payload['componentName']
        if 'keyPath' in payload:
            if payload['keyPath'] is None:
                new.set_explicitly_null('key_path')
            else:
                new.key_path = payload['keyPath']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToConfigurationUpdateRequest'

    def __repr__(self):
        attrs = []
        for attr in ['component_name', 'key_path']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToConfigurationUpdateRequest):
            return self.__dict__ == other.__dict__
        return False


class PublishToIoTCoreResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PublishToIoTCoreResponse):
            return self.__dict__ == other.__dict__
        return False


class PublishToIoTCoreRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 topic_name=None,
                 qos=None,
                 payload=None):
        super().__init__()
        self.topic_name = topic_name
        self.qos = qos
        self.payload = payload

    def _to_payload(self):
        payload = {}
        if self.topic_name is None:
            if self.is_explicitly_null('topic_name'):
                payload['topicName'] = None
        else:
            payload['topicName'] = self.topic_name
        if self.qos is None:
            if self.is_explicitly_null('qos'):
                payload['qos'] = None
        else:
            payload['qos'] = self.qos._to_payload()
        if self.payload is None:
            if self.is_explicitly_null('payload'):
                payload['payload'] = None
        else:
            payload['payload'] = base64.b64encode(self.payload).decode()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            if payload['topicName'] is None:
                new.set_explicitly_null('topic_name')
            else:
                new.topic_name = payload['topicName']
        if 'qos' in payload:
            if payload['qos'] is None:
                new.set_explicitly_null('qos')
            else:
                new.qos = QOS._from_payload(payload['qos'])
        if 'payload' in payload:
            if payload['payload'] is None:
                new.set_explicitly_null('payload')
            else:
                new.payload = base64.b64decode(payload['payload'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishToIoTCoreRequest'

    def __repr__(self):
        attrs = []
        for attr in ['topic_name', 'qos', 'payload']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PublishToIoTCoreRequest):
            return self.__dict__ == other.__dict__
        return False


class PublishToTopicResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PublishToTopicResponse):
            return self.__dict__ == other.__dict__
        return False


class PublishToTopicRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 topic=None,
                 publish_message=None):
        super().__init__()
        self.topic = topic
        self.publish_message = publish_message

    def _to_payload(self):
        payload = {}
        if self.topic is None:
            if self.is_explicitly_null('topic'):
                payload['topic'] = None
        else:
            payload['topic'] = self.topic
        if self.publish_message is None:
            if self.is_explicitly_null('publish_message'):
                payload['publishMessage'] = None
        else:
            payload['publishMessage'] = self.publish_message._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topic' in payload:
            if payload['topic'] is None:
                new.set_explicitly_null('topic')
            else:
                new.topic = payload['topic']
        if 'publishMessage' in payload:
            if payload['publishMessage'] is None:
                new.set_explicitly_null('publish_message')
            else:
                new.publish_message = PublishMessage._from_payload(payload['publishMessage'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#PublishToTopicRequest'

    def __repr__(self):
        attrs = []
        for attr in ['topic', 'publish_message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, PublishToTopicRequest):
            return self.__dict__ == other.__dict__
        return False


class UnauthorizedError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'client'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UnauthorizedError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, UnauthorizedError):
            return self.__dict__ == other.__dict__
        return False


class ServiceError(GreengrassCoreIPCError, _ExplicitlyNullMixin):

    def __init__(self, *,
                 message=None):
        super().__init__()
        self.message = message

    def _get_error_type_string(self):
        return 'server'

    def _to_payload(self):
        payload = {}
        if self.message is None:
            if self.is_explicitly_null('message'):
                payload['message'] = None
        else:
            payload['message'] = self.message
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'message' in payload:
            if payload['message'] is None:
                new.set_explicitly_null('message')
            else:
                new.message = payload['message']
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#ServiceError'

    def __repr__(self):
        attrs = []
        for attr in ['message']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, ServiceError):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToIoTCoreResponse(rpc.Shape, _ExplicitlyNullMixin):

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
        for attr in []:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToIoTCoreResponse):
            return self.__dict__ == other.__dict__
        return False


class SubscribeToIoTCoreRequest(rpc.Shape, _ExplicitlyNullMixin):

    def __init__(self, *,
                 topic_name=None,
                 qos=None):
        super().__init__()
        self.topic_name = topic_name
        self.qos = qos

    def _to_payload(self):
        payload = {}
        if self.topic_name is None:
            if self.is_explicitly_null('topic_name'):
                payload['topicName'] = None
        else:
            payload['topicName'] = self.topic_name
        if self.qos is None:
            if self.is_explicitly_null('qos'):
                payload['qos'] = None
        else:
            payload['qos'] = self.qos._to_payload()
        return payload

    @classmethod
    def _from_payload(cls, payload):
        new = cls()
        if 'topicName' in payload:
            if payload['topicName'] is None:
                new.set_explicitly_null('topic_name')
            else:
                new.topic_name = payload['topicName']
        if 'qos' in payload:
            if payload['qos'] is None:
                new.set_explicitly_null('qos')
            else:
                new.qos = QOS._from_payload(payload['qos'])
        return new

    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToIoTCoreRequest'

    def __repr__(self):
        attrs = []
        for attr in ['topic_name', 'qos']:
            val = getattr(self, attr)
            if val is not None:
                attrs.append('%s=%r' % (attr, val))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(attrs))

    def __eq__(self, other):
        if isinstance(other, SubscribeToIoTCoreRequest):
            return self.__dict__ == other.__dict__
        return False


SHAPE_INDEX = rpc.ShapeIndex([
    PostComponentUpdateEvent,
    PreComponentUpdateEvent,
    ValidateConfigurationUpdateEvent,
    ConfigurationUpdateEvent,
    BinaryMessage,
    JsonMessage,
    MQTTMessage,
    ComponentDetails,
    LocalDeployment,
    ConfigurationValidityReport,
    CreateLocalDeploymentResponse,
    CreateLocalDeploymentRequest,
    StopComponentResponse,
    StopComponentRequest,
    ListLocalDeploymentsResponse,
    ListLocalDeploymentsRequest,
    SubscribeToComponentUpdatesResponse,
    SubscribeToComponentUpdatesRequest,
    GetComponentDetailsResponse,
    GetComponentDetailsRequest,
    SubscribeToTopicResponse,
    SubscribeToTopicRequest,
    GetConfigurationResponse,
    GetConfigurationRequest,
    UpdateStateResponse,
    UpdateStateRequest,
    GetSecretValueResponse,
    GetSecretValueRequest,
    GetLocalDeploymentStatusResponse,
    GetLocalDeploymentStatusRequest,
    ComponentNotFoundError,
    RestartComponentResponse,
    RestartComponentRequest,
    InvalidArtifactsDirectoryPathError,
    InvalidRecipeDirectoryPathError,
    UpdateRecipesAndArtifactsResponse,
    UpdateRecipesAndArtifactsRequest,
    InvalidTokenError,
    ValidateAuthorizationTokenResponse,
    ValidateAuthorizationTokenRequest,
    SubscribeToValidateConfigurationUpdatesResponse,
    SubscribeToValidateConfigurationUpdatesRequest,
    FailedUpdateConditionCheckError,
    ConflictError,
    UpdateConfigurationResponse,
    UpdateConfigurationRequest,
    SendConfigurationValidityReportResponse,
    SendConfigurationValidityReportRequest,
    InvalidArgumentsError,
    DeferComponentUpdateResponse,
    DeferComponentUpdateRequest,
    CreateDebugPasswordResponse,
    CreateDebugPasswordRequest,
    ListComponentsResponse,
    ListComponentsRequest,
    ResourceNotFoundError,
    SubscribeToConfigurationUpdateResponse,
    SubscribeToConfigurationUpdateRequest,
    PublishToIoTCoreResponse,
    PublishToIoTCoreRequest,
    PublishToTopicResponse,
    PublishToTopicRequest,
    UnauthorizedError,
    ServiceError,
    SubscribeToIoTCoreResponse,
    SubscribeToIoTCoreRequest,
])


class _SubscribeToIoTCoreOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToIoTCore'

    @classmethod
    def _request_type(cls):
        return SubscribeToIoTCoreRequest

    @classmethod
    def _request_stream_type(cls):
        return IoTCoreMessage

    @classmethod
    def _response_type(cls):
        return SubscribeToIoTCoreResponse

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


class _SubscribeToConfigurationUpdateOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToConfigurationUpdate'

    @classmethod
    def _request_type(cls):
        return SubscribeToConfigurationUpdateRequest

    @classmethod
    def _request_stream_type(cls):
        return ConfigurationUpdateEvents

    @classmethod
    def _response_type(cls):
        return SubscribeToConfigurationUpdateResponse

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


class _SubscribeToValidateConfigurationUpdatesOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToValidateConfigurationUpdates'

    @classmethod
    def _request_type(cls):
        return SubscribeToValidateConfigurationUpdatesRequest

    @classmethod
    def _request_stream_type(cls):
        return ValidateConfigurationUpdateEvents

    @classmethod
    def _response_type(cls):
        return SubscribeToValidateConfigurationUpdatesResponse

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


class _UpdateRecipesAndArtifactsOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#UpdateRecipesAndArtifacts'

    @classmethod
    def _request_type(cls):
        return UpdateRecipesAndArtifactsRequest

    @classmethod
    def _request_stream_type(cls):
        return None

    @classmethod
    def _response_type(cls):
        return UpdateRecipesAndArtifactsResponse

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


class _SubscribeToTopicOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToTopic'

    @classmethod
    def _request_type(cls):
        return SubscribeToTopicRequest

    @classmethod
    def _request_stream_type(cls):
        return SubscriptionResponseMessage

    @classmethod
    def _response_type(cls):
        return SubscribeToTopicResponse

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


class _SubscribeToComponentUpdatesOperation(rpc.ClientOperation):
    @classmethod
    def _model_name(cls):
        return 'aws.greengrass#SubscribeToComponentUpdates'

    @classmethod
    def _request_type(cls):
        return SubscribeToComponentUpdatesRequest

    @classmethod
    def _request_stream_type(cls):
        return ComponentUpdatePolicyEvents

    @classmethod
    def _response_type(cls):
        return SubscribeToComponentUpdatesResponse

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


