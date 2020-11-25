# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
import awsiot.eventstreamrpc as rpc
import concurrent.futures


class SubscribeToIoTCoreStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.IoTCoreMessage) -> None:
        """
        Invoked when a model.IoTCoreMessage is received.
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
    def activate(self, request: model.SubscribeToIoTCoreRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.SubscribeToIoTCoreRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.SubscribeToIoTCoreResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class PublishToTopicOperation(model._PublishToTopicOperation):
    def activate(self, request: model.PublishToTopicRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.PublishToTopicRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.PublishToTopicResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class PublishToIoTCoreOperation(model._PublishToIoTCoreOperation):
    def activate(self, request: model.PublishToIoTCoreRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.PublishToIoTCoreRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.PublishToIoTCoreResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class SubscribeToConfigurationUpdateStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.ConfigurationUpdateEvents) -> None:
        """
        Invoked when a model.ConfigurationUpdateEvents is received.
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
    def activate(self, request: model.SubscribeToConfigurationUpdateRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.SubscribeToConfigurationUpdateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.SubscribeToConfigurationUpdateResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class ListComponentsOperation(model._ListComponentsOperation):
    def activate(self, request: model.ListComponentsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.ListComponentsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.ListComponentsResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class CreateDebugPasswordOperation(model._CreateDebugPasswordOperation):
    def activate(self, request: model.CreateDebugPasswordRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.CreateDebugPasswordRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.CreateDebugPasswordResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class DeferComponentUpdateOperation(model._DeferComponentUpdateOperation):
    def activate(self, request: model.DeferComponentUpdateRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.DeferComponentUpdateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.DeferComponentUpdateResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class SendConfigurationValidityReportOperation(model._SendConfigurationValidityReportOperation):
    def activate(self, request: model.SendConfigurationValidityReportRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.SendConfigurationValidityReportRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.SendConfigurationValidityReportResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class UpdateConfigurationOperation(model._UpdateConfigurationOperation):
    def activate(self, request: model.UpdateConfigurationRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.UpdateConfigurationRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.UpdateConfigurationResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class SubscribeToValidateConfigurationUpdatesStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.ValidateConfigurationUpdateEvents) -> None:
        """
        Invoked when a model.ValidateConfigurationUpdateEvents is received.
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
    def activate(self, request: model.SubscribeToValidateConfigurationUpdatesRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.SubscribeToValidateConfigurationUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.SubscribeToValidateConfigurationUpdatesResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class ValidateAuthorizationTokenOperation(model._ValidateAuthorizationTokenOperation):
    def activate(self, request: model.ValidateAuthorizationTokenRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.ValidateAuthorizationTokenRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.ValidateAuthorizationTokenResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class UpdateRecipesAndArtifactsOperation(model._UpdateRecipesAndArtifactsOperation):
    def activate(self, request: model.UpdateRecipesAndArtifactsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.UpdateRecipesAndArtifactsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.UpdateRecipesAndArtifactsResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class RestartComponentOperation(model._RestartComponentOperation):
    def activate(self, request: model.RestartComponentRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.RestartComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.RestartComponentResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class GetLocalDeploymentStatusOperation(model._GetLocalDeploymentStatusOperation):
    def activate(self, request: model.GetLocalDeploymentStatusRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.GetLocalDeploymentStatusRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.GetLocalDeploymentStatusResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class GetSecretValueOperation(model._GetSecretValueOperation):
    def activate(self, request: model.GetSecretValueRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.GetSecretValueRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.GetSecretValueResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class UpdateStateOperation(model._UpdateStateOperation):
    def activate(self, request: model.UpdateStateRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.UpdateStateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.UpdateStateResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class GetConfigurationOperation(model._GetConfigurationOperation):
    def activate(self, request: model.GetConfigurationRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.GetConfigurationRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.GetConfigurationResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class SubscribeToTopicStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.SubscriptionResponseMessage) -> None:
        """
        Invoked when a model.SubscriptionResponseMessage is received.
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
    def activate(self, request: model.SubscribeToTopicRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.SubscribeToTopicRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.SubscribeToTopicResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class GetComponentDetailsOperation(model._GetComponentDetailsOperation):
    def activate(self, request: model.GetComponentDetailsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.GetComponentDetailsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.GetComponentDetailsResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class SubscribeToComponentUpdatesStreamHandler(rpc.StreamResponseHandler):
    """
    Inherit from this class and override methods to handle operation events.
    """

    def on_stream_event(self, event: model.ComponentUpdatePolicyEvents) -> None:
        """
        Invoked when a model.ComponentUpdatePolicyEvents is received.
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
    def activate(self, request: model.SubscribeToComponentUpdatesRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.SubscribeToComponentUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.SubscribeToComponentUpdatesResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class ListLocalDeploymentsOperation(model._ListLocalDeploymentsOperation):
    def activate(self, request: model.ListLocalDeploymentsRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.ListLocalDeploymentsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.ListLocalDeploymentsResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class StopComponentOperation(model._StopComponentOperation):
    def activate(self, request: model.StopComponentRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.StopComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.StopComponentResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class CreateLocalDeploymentOperation(model._CreateLocalDeploymentOperation):
    def activate(self, request: model.CreateLocalDeploymentRequest) -> concurrent.futures.Future:
        """
        Activate this operation by sending the initial model.CreateLocalDeploymentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self) -> concurrent.futures.Future:
        """
        Returns a Future which completes with a result of model.CreateLocalDeploymentResponse,
        or an exception.
        """
        return self._get_response()

    def close(self) -> concurrent.futures.Future:
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation  has closed.
        """
        return super().close()


class GreengrassCoreIPCClient(rpc.Client):

    def __init__(self, connection: rpc.Connection):
        super().__init__(connection, model.SHAPE_INDEX)

    def new_subscribe_to_iot_core(self, stream_handler: SubscribeToIoTCoreStreamHandler) -> SubscribeToIoTCoreOperation:
        return self._new_operation(SubscribeToIoTCoreOperation, stream_handler)

    def new_publish_to_topic(self) -> PublishToTopicOperation:
        return self._new_operation(PublishToTopicOperation)

    def new_publish_to_iot_core(self) -> PublishToIoTCoreOperation:
        return self._new_operation(PublishToIoTCoreOperation)

    def new_subscribe_to_configuration_update(self, stream_handler: SubscribeToConfigurationUpdateStreamHandler) -> SubscribeToConfigurationUpdateOperation:
        return self._new_operation(SubscribeToConfigurationUpdateOperation, stream_handler)

    def new_list_components(self) -> ListComponentsOperation:
        return self._new_operation(ListComponentsOperation)

    def new_create_debug_password(self) -> CreateDebugPasswordOperation:
        return self._new_operation(CreateDebugPasswordOperation)

    def new_defer_component_update(self) -> DeferComponentUpdateOperation:
        return self._new_operation(DeferComponentUpdateOperation)

    def new_send_configuration_validity_report(self) -> SendConfigurationValidityReportOperation:
        return self._new_operation(SendConfigurationValidityReportOperation)

    def new_update_configuration(self) -> UpdateConfigurationOperation:
        return self._new_operation(UpdateConfigurationOperation)

    def new_subscribe_to_validate_configuration_updates(self, stream_handler: SubscribeToValidateConfigurationUpdatesStreamHandler) -> SubscribeToValidateConfigurationUpdatesOperation:
        return self._new_operation(SubscribeToValidateConfigurationUpdatesOperation, stream_handler)

    def new_validate_authorization_token(self) -> ValidateAuthorizationTokenOperation:
        return self._new_operation(ValidateAuthorizationTokenOperation)

    def new_update_recipes_and_artifacts(self) -> UpdateRecipesAndArtifactsOperation:
        return self._new_operation(UpdateRecipesAndArtifactsOperation)

    def new_restart_component(self) -> RestartComponentOperation:
        return self._new_operation(RestartComponentOperation)

    def new_get_local_deployment_status(self) -> GetLocalDeploymentStatusOperation:
        return self._new_operation(GetLocalDeploymentStatusOperation)

    def new_get_secret_value(self) -> GetSecretValueOperation:
        return self._new_operation(GetSecretValueOperation)

    def new_update_state(self) -> UpdateStateOperation:
        return self._new_operation(UpdateStateOperation)

    def new_get_configuration(self) -> GetConfigurationOperation:
        return self._new_operation(GetConfigurationOperation)

    def new_subscribe_to_topic(self, stream_handler: SubscribeToTopicStreamHandler) -> SubscribeToTopicOperation:
        return self._new_operation(SubscribeToTopicOperation, stream_handler)

    def new_get_component_details(self) -> GetComponentDetailsOperation:
        return self._new_operation(GetComponentDetailsOperation)

    def new_subscribe_to_component_updates(self, stream_handler: SubscribeToComponentUpdatesStreamHandler) -> SubscribeToComponentUpdatesOperation:
        return self._new_operation(SubscribeToComponentUpdatesOperation, stream_handler)

    def new_list_local_deployments(self) -> ListLocalDeploymentsOperation:
        return self._new_operation(ListLocalDeploymentsOperation)

    def new_stop_component(self) -> StopComponentOperation:
        return self._new_operation(StopComponentOperation)

    def new_create_local_deployment(self) -> CreateLocalDeploymentOperation:
        return self._new_operation(CreateLocalDeploymentOperation)
