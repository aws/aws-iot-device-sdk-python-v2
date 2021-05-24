# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
import awsiot.eventstreamrpc as rpc
import concurrent.futures


class SubscribeToIoTCoreStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for SubscribeToIoTCoreOperation

    Inherit from this class and override methods to handle
    stream events during a SubscribeToIoTCoreOperation.
    """

    def on_stream_event(self, event: model.IoTCoreMessage) -> None:
        """
        Invoked when a IoTCoreMessage is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class SubscribeToIoTCoreOperation(model._SubscribeToIoTCoreOperation):
    """
    SubscribeToIoTCoreOperation

    Create with GreengrassCoreIPCClient.new_subscribe_to_iot_core()
    """

    def activate(self, request: model.SubscribeToIoTCoreRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial SubscribeToIoTCoreRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of SubscribeToIoTCoreResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class PublishToIoTCoreOperation(model._PublishToIoTCoreOperation):
    """
    PublishToIoTCoreOperation

    Create with GreengrassCoreIPCClient.new_publish_to_iot_core()
    """

    def activate(self, request: model.PublishToIoTCoreRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial PublishToIoTCoreRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of PublishToIoTCoreResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class SubscribeToConfigurationUpdateStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for SubscribeToConfigurationUpdateOperation

    Inherit from this class and override methods to handle
    stream events during a SubscribeToConfigurationUpdateOperation.
    """

    def on_stream_event(self, event: model.ConfigurationUpdateEvents) -> None:
        """
        Invoked when a ConfigurationUpdateEvents is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class SubscribeToConfigurationUpdateOperation(model._SubscribeToConfigurationUpdateOperation):
    """
    SubscribeToConfigurationUpdateOperation

    Create with GreengrassCoreIPCClient.new_subscribe_to_configuration_update()
    """

    def activate(self, request: model.SubscribeToConfigurationUpdateRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial SubscribeToConfigurationUpdateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of SubscribeToConfigurationUpdateResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class DeleteThingShadowOperation(model._DeleteThingShadowOperation):
    """
    DeleteThingShadowOperation

    Create with GreengrassCoreIPCClient.new_delete_thing_shadow()
    """

    def activate(self, request: model.DeleteThingShadowRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial DeleteThingShadowRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of DeleteThingShadowResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class DeferComponentUpdateOperation(model._DeferComponentUpdateOperation):
    """
    DeferComponentUpdateOperation

    Create with GreengrassCoreIPCClient.new_defer_component_update()
    """

    def activate(self, request: model.DeferComponentUpdateRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial DeferComponentUpdateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of DeferComponentUpdateResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class SubscribeToValidateConfigurationUpdatesStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for SubscribeToValidateConfigurationUpdatesOperation

    Inherit from this class and override methods to handle
    stream events during a SubscribeToValidateConfigurationUpdatesOperation.
    """

    def on_stream_event(self, event: model.ValidateConfigurationUpdateEvents) -> None:
        """
        Invoked when a ValidateConfigurationUpdateEvents is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class SubscribeToValidateConfigurationUpdatesOperation(model._SubscribeToValidateConfigurationUpdatesOperation):
    """
    SubscribeToValidateConfigurationUpdatesOperation

    Create with GreengrassCoreIPCClient.new_subscribe_to_validate_configuration_updates()
    """

    def activate(self, request: model.SubscribeToValidateConfigurationUpdatesRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial SubscribeToValidateConfigurationUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of SubscribeToValidateConfigurationUpdatesResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetConfigurationOperation(model._GetConfigurationOperation):
    """
    GetConfigurationOperation

    Create with GreengrassCoreIPCClient.new_get_configuration()
    """

    def activate(self, request: model.GetConfigurationRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetConfigurationRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetConfigurationResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class SubscribeToTopicStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for SubscribeToTopicOperation

    Inherit from this class and override methods to handle
    stream events during a SubscribeToTopicOperation.
    """

    def on_stream_event(self, event: model.SubscriptionResponseMessage) -> None:
        """
        Invoked when a SubscriptionResponseMessage is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class SubscribeToTopicOperation(model._SubscribeToTopicOperation):
    """
    SubscribeToTopicOperation

    Create with GreengrassCoreIPCClient.new_subscribe_to_topic()
    """

    def activate(self, request: model.SubscribeToTopicRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial SubscribeToTopicRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of SubscribeToTopicResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetComponentDetailsOperation(model._GetComponentDetailsOperation):
    """
    GetComponentDetailsOperation

    Create with GreengrassCoreIPCClient.new_get_component_details()
    """

    def activate(self, request: model.GetComponentDetailsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetComponentDetailsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetComponentDetailsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class PublishToTopicOperation(model._PublishToTopicOperation):
    """
    PublishToTopicOperation

    Create with GreengrassCoreIPCClient.new_publish_to_topic()
    """

    def activate(self, request: model.PublishToTopicRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial PublishToTopicRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of PublishToTopicResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class ListComponentsOperation(model._ListComponentsOperation):
    """
    ListComponentsOperation

    Create with GreengrassCoreIPCClient.new_list_components()
    """

    def activate(self, request: model.ListComponentsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial ListComponentsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of ListComponentsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class CreateDebugPasswordOperation(model._CreateDebugPasswordOperation):
    """
    CreateDebugPasswordOperation

    Create with GreengrassCoreIPCClient.new_create_debug_password()
    """

    def activate(self, request: model.CreateDebugPasswordRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial CreateDebugPasswordRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of CreateDebugPasswordResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetThingShadowOperation(model._GetThingShadowOperation):
    """
    GetThingShadowOperation

    Create with GreengrassCoreIPCClient.new_get_thing_shadow()
    """

    def activate(self, request: model.GetThingShadowRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetThingShadowRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetThingShadowResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class SendConfigurationValidityReportOperation(model._SendConfigurationValidityReportOperation):
    """
    SendConfigurationValidityReportOperation

    Create with GreengrassCoreIPCClient.new_send_configuration_validity_report()
    """

    def activate(self, request: model.SendConfigurationValidityReportRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial SendConfigurationValidityReportRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of SendConfigurationValidityReportResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class UpdateThingShadowOperation(model._UpdateThingShadowOperation):
    """
    UpdateThingShadowOperation

    Create with GreengrassCoreIPCClient.new_update_thing_shadow()
    """

    def activate(self, request: model.UpdateThingShadowRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial UpdateThingShadowRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of UpdateThingShadowResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class UpdateConfigurationOperation(model._UpdateConfigurationOperation):
    """
    UpdateConfigurationOperation

    Create with GreengrassCoreIPCClient.new_update_configuration()
    """

    def activate(self, request: model.UpdateConfigurationRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial UpdateConfigurationRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of UpdateConfigurationResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class ValidateAuthorizationTokenOperation(model._ValidateAuthorizationTokenOperation):
    """
    ValidateAuthorizationTokenOperation

    Create with GreengrassCoreIPCClient.new_validate_authorization_token()
    """

    def activate(self, request: model.ValidateAuthorizationTokenRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial ValidateAuthorizationTokenRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of ValidateAuthorizationTokenResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class RestartComponentOperation(model._RestartComponentOperation):
    """
    RestartComponentOperation

    Create with GreengrassCoreIPCClient.new_restart_component()
    """

    def activate(self, request: model.RestartComponentRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial RestartComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of RestartComponentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetLocalDeploymentStatusOperation(model._GetLocalDeploymentStatusOperation):
    """
    GetLocalDeploymentStatusOperation

    Create with GreengrassCoreIPCClient.new_get_local_deployment_status()
    """

    def activate(self, request: model.GetLocalDeploymentStatusRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetLocalDeploymentStatusRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetLocalDeploymentStatusResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetSecretValueOperation(model._GetSecretValueOperation):
    """
    GetSecretValueOperation

    Create with GreengrassCoreIPCClient.new_get_secret_value()
    """

    def activate(self, request: model.GetSecretValueRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial GetSecretValueRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of GetSecretValueResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class UpdateStateOperation(model._UpdateStateOperation):
    """
    UpdateStateOperation

    Create with GreengrassCoreIPCClient.new_update_state()
    """

    def activate(self, request: model.UpdateStateRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial UpdateStateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of UpdateStateResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class ListNamedShadowsForThingOperation(model._ListNamedShadowsForThingOperation):
    """
    ListNamedShadowsForThingOperation

    Create with GreengrassCoreIPCClient.new_list_named_shadows_for_thing()
    """

    def activate(self, request: model.ListNamedShadowsForThingRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial ListNamedShadowsForThingRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of ListNamedShadowsForThingResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class SubscribeToComponentUpdatesStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for SubscribeToComponentUpdatesOperation

    Inherit from this class and override methods to handle
    stream events during a SubscribeToComponentUpdatesOperation.
    """

    def on_stream_event(self, event: model.ComponentUpdatePolicyEvents) -> None:
        """
        Invoked when a ComponentUpdatePolicyEvents is received.
        """
        pass

    def on_stream_error(self, error: Exception) -> bool:
        """
        Invoked when an error occurs on the operation stream.

        Return True if operation should close as a result of this error,
        """
        return True

    def on_stream_closed(self) -> None:
        """
        Invoked when the stream for this operation is closed.
        """
        pass


class SubscribeToComponentUpdatesOperation(model._SubscribeToComponentUpdatesOperation):
    """
    SubscribeToComponentUpdatesOperation

    Create with GreengrassCoreIPCClient.new_subscribe_to_component_updates()
    """

    def activate(self, request: model.SubscribeToComponentUpdatesRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial SubscribeToComponentUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of SubscribeToComponentUpdatesResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class ListLocalDeploymentsOperation(model._ListLocalDeploymentsOperation):
    """
    ListLocalDeploymentsOperation

    Create with GreengrassCoreIPCClient.new_list_local_deployments()
    """

    def activate(self, request: model.ListLocalDeploymentsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial ListLocalDeploymentsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of ListLocalDeploymentsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class StopComponentOperation(model._StopComponentOperation):
    """
    StopComponentOperation

    Create with GreengrassCoreIPCClient.new_stop_component()
    """

    def activate(self, request: model.StopComponentRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial StopComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of StopComponentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class CreateLocalDeploymentOperation(model._CreateLocalDeploymentOperation):
    """
    CreateLocalDeploymentOperation

    Create with GreengrassCoreIPCClient.new_create_local_deployment()
    """

    def activate(self, request: model.CreateLocalDeploymentRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial CreateLocalDeploymentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of CreateLocalDeploymentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GreengrassCoreIPCClient(rpc.Client):
    """
    Client for the GreengrassCoreIPC service.

    Args:
        connection: Connection that this client will use.
    """

    def __init__(self, connection: rpc.Connection):
        super().__init__(connection, model.SHAPE_INDEX)

    def new_subscribe_to_iot_core(self, stream_handler: SubscribeToIoTCoreStreamHandler) -> SubscribeToIoTCoreOperation:
        """
        Create a new SubscribeToIoTCoreOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(SubscribeToIoTCoreOperation, stream_handler)

    def new_publish_to_iot_core(self) -> PublishToIoTCoreOperation:
        """
        Create a new PublishToIoTCoreOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(PublishToIoTCoreOperation)

    def new_subscribe_to_configuration_update(self, stream_handler: SubscribeToConfigurationUpdateStreamHandler) -> SubscribeToConfigurationUpdateOperation:
        """
        Create a new SubscribeToConfigurationUpdateOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(SubscribeToConfigurationUpdateOperation, stream_handler)

    def new_delete_thing_shadow(self) -> DeleteThingShadowOperation:
        """
        Create a new DeleteThingShadowOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(DeleteThingShadowOperation)

    def new_defer_component_update(self) -> DeferComponentUpdateOperation:
        """
        Create a new DeferComponentUpdateOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(DeferComponentUpdateOperation)

    def new_subscribe_to_validate_configuration_updates(self, stream_handler: SubscribeToValidateConfigurationUpdatesStreamHandler) -> SubscribeToValidateConfigurationUpdatesOperation:
        """
        Create a new SubscribeToValidateConfigurationUpdatesOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(SubscribeToValidateConfigurationUpdatesOperation, stream_handler)

    def new_get_configuration(self) -> GetConfigurationOperation:
        """
        Create a new GetConfigurationOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetConfigurationOperation)

    def new_subscribe_to_topic(self, stream_handler: SubscribeToTopicStreamHandler) -> SubscribeToTopicOperation:
        """
        Create a new SubscribeToTopicOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(SubscribeToTopicOperation, stream_handler)

    def new_get_component_details(self) -> GetComponentDetailsOperation:
        """
        Create a new GetComponentDetailsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetComponentDetailsOperation)

    def new_publish_to_topic(self) -> PublishToTopicOperation:
        """
        Create a new PublishToTopicOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(PublishToTopicOperation)

    def new_list_components(self) -> ListComponentsOperation:
        """
        Create a new ListComponentsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ListComponentsOperation)

    def new_create_debug_password(self) -> CreateDebugPasswordOperation:
        """
        Create a new CreateDebugPasswordOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(CreateDebugPasswordOperation)

    def new_get_thing_shadow(self) -> GetThingShadowOperation:
        """
        Create a new GetThingShadowOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetThingShadowOperation)

    def new_send_configuration_validity_report(self) -> SendConfigurationValidityReportOperation:
        """
        Create a new SendConfigurationValidityReportOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(SendConfigurationValidityReportOperation)

    def new_update_thing_shadow(self) -> UpdateThingShadowOperation:
        """
        Create a new UpdateThingShadowOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(UpdateThingShadowOperation)

    def new_update_configuration(self) -> UpdateConfigurationOperation:
        """
        Create a new UpdateConfigurationOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(UpdateConfigurationOperation)

    def new_validate_authorization_token(self) -> ValidateAuthorizationTokenOperation:
        """
        Create a new ValidateAuthorizationTokenOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ValidateAuthorizationTokenOperation)

    def new_restart_component(self) -> RestartComponentOperation:
        """
        Create a new RestartComponentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(RestartComponentOperation)

    def new_get_local_deployment_status(self) -> GetLocalDeploymentStatusOperation:
        """
        Create a new GetLocalDeploymentStatusOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetLocalDeploymentStatusOperation)

    def new_get_secret_value(self) -> GetSecretValueOperation:
        """
        Create a new GetSecretValueOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetSecretValueOperation)

    def new_update_state(self) -> UpdateStateOperation:
        """
        Create a new UpdateStateOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(UpdateStateOperation)

    def new_list_named_shadows_for_thing(self) -> ListNamedShadowsForThingOperation:
        """
        Create a new ListNamedShadowsForThingOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ListNamedShadowsForThingOperation)

    def new_subscribe_to_component_updates(self, stream_handler: SubscribeToComponentUpdatesStreamHandler) -> SubscribeToComponentUpdatesOperation:
        """
        Create a new SubscribeToComponentUpdatesOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(SubscribeToComponentUpdatesOperation, stream_handler)

    def new_list_local_deployments(self) -> ListLocalDeploymentsOperation:
        """
        Create a new ListLocalDeploymentsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ListLocalDeploymentsOperation)

    def new_stop_component(self) -> StopComponentOperation:
        """
        Create a new StopComponentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(StopComponentOperation)

    def new_create_local_deployment(self) -> CreateLocalDeploymentOperation:
        """
        Create a new CreateLocalDeploymentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(CreateLocalDeploymentOperation)
