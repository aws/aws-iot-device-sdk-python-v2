# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
import awsiot.eventstreamrpc as rpc
import concurrent.futures


class AuthorizeClientDeviceActionOperation(model._AuthorizeClientDeviceActionOperation):
    """
    AuthorizeClientDeviceActionOperation

    Create with GreengrassCoreIPCClient.new_authorize_client_device_action()
    """

    def activate(self, request: model.AuthorizeClientDeviceActionRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial AuthorizeClientDeviceActionRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.AuthorizeClientDeviceActionResponse]
        """
        Returns a Future which completes with a result of AuthorizeClientDeviceActionResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class CancelLocalDeploymentOperation(model._CancelLocalDeploymentOperation):
    """
    CancelLocalDeploymentOperation

    Create with GreengrassCoreIPCClient.new_cancel_local_deployment()
    """

    def activate(self, request: model.CancelLocalDeploymentRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial CancelLocalDeploymentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.CancelLocalDeploymentResponse]
        """
        Returns a Future which completes with a result of CancelLocalDeploymentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.CreateDebugPasswordRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial CreateDebugPasswordRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.CreateDebugPasswordResponse]
        """
        Returns a Future which completes with a result of CreateDebugPasswordResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.CreateLocalDeploymentRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial CreateLocalDeploymentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.CreateLocalDeploymentResponse]
        """
        Returns a Future which completes with a result of CreateLocalDeploymentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.DeferComponentUpdateRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial DeferComponentUpdateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.DeferComponentUpdateResponse]
        """
        Returns a Future which completes with a result of DeferComponentUpdateResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.DeleteThingShadowRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial DeleteThingShadowRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.DeleteThingShadowResponse]
        """
        Returns a Future which completes with a result of DeleteThingShadowResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GetClientDeviceAuthTokenOperation(model._GetClientDeviceAuthTokenOperation):
    """
    GetClientDeviceAuthTokenOperation

    Create with GreengrassCoreIPCClient.new_get_client_device_auth_token()
    """

    def activate(self, request: model.GetClientDeviceAuthTokenRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial GetClientDeviceAuthTokenRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.GetClientDeviceAuthTokenResponse]
        """
        Returns a Future which completes with a result of GetClientDeviceAuthTokenResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.GetComponentDetailsRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial GetComponentDetailsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.GetComponentDetailsResponse]
        """
        Returns a Future which completes with a result of GetComponentDetailsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.GetConfigurationRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial GetConfigurationRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.GetConfigurationResponse]
        """
        Returns a Future which completes with a result of GetConfigurationResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.GetLocalDeploymentStatusRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial GetLocalDeploymentStatusRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.GetLocalDeploymentStatusResponse]
        """
        Returns a Future which completes with a result of GetLocalDeploymentStatusResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.GetSecretValueRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial GetSecretValueRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.GetSecretValueResponse]
        """
        Returns a Future which completes with a result of GetSecretValueResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.GetThingShadowRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial GetThingShadowRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.GetThingShadowResponse]
        """
        Returns a Future which completes with a result of GetThingShadowResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.ListComponentsRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial ListComponentsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.ListComponentsResponse]
        """
        Returns a Future which completes with a result of ListComponentsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.ListLocalDeploymentsRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial ListLocalDeploymentsRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.ListLocalDeploymentsResponse]
        """
        Returns a Future which completes with a result of ListLocalDeploymentsResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.ListNamedShadowsForThingRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial ListNamedShadowsForThingRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.ListNamedShadowsForThingResponse]
        """
        Returns a Future which completes with a result of ListNamedShadowsForThingResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class PauseComponentOperation(model._PauseComponentOperation):
    """
    PauseComponentOperation

    Create with GreengrassCoreIPCClient.new_pause_component()
    """

    def activate(self, request: model.PauseComponentRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial PauseComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.PauseComponentResponse]
        """
        Returns a Future which completes with a result of PauseComponentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.PublishToIoTCoreRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial PublishToIoTCoreRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.PublishToIoTCoreResponse]
        """
        Returns a Future which completes with a result of PublishToIoTCoreResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.PublishToTopicRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial PublishToTopicRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.PublishToTopicResponse]
        """
        Returns a Future which completes with a result of PublishToTopicResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class PutComponentMetricOperation(model._PutComponentMetricOperation):
    """
    PutComponentMetricOperation

    Create with GreengrassCoreIPCClient.new_put_component_metric()
    """

    def activate(self, request: model.PutComponentMetricRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial PutComponentMetricRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.PutComponentMetricResponse]
        """
        Returns a Future which completes with a result of PutComponentMetricResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.RestartComponentRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial RestartComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.RestartComponentResponse]
        """
        Returns a Future which completes with a result of RestartComponentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class ResumeComponentOperation(model._ResumeComponentOperation):
    """
    ResumeComponentOperation

    Create with GreengrassCoreIPCClient.new_resume_component()
    """

    def activate(self, request: model.ResumeComponentRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial ResumeComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.ResumeComponentResponse]
        """
        Returns a Future which completes with a result of ResumeComponentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.SendConfigurationValidityReportRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SendConfigurationValidityReportRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SendConfigurationValidityReportResponse]
        """
        Returns a Future which completes with a result of SendConfigurationValidityReportResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.StopComponentRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial StopComponentRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.StopComponentResponse]
        """
        Returns a Future which completes with a result of StopComponentResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class SubscribeToCertificateUpdatesStreamHandler(rpc.StreamResponseHandler):
    """
    Event handler for SubscribeToCertificateUpdatesOperation

    Inherit from this class and override methods to handle
    stream events during a SubscribeToCertificateUpdatesOperation.
    """

    def on_stream_event(self, event: model.CertificateUpdateEvent) -> None:
        """
        Invoked when a CertificateUpdateEvent is received.
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


class SubscribeToCertificateUpdatesOperation(model._SubscribeToCertificateUpdatesOperation):
    """
    SubscribeToCertificateUpdatesOperation

    Create with GreengrassCoreIPCClient.new_subscribe_to_certificate_updates()
    """

    def activate(self, request: model.SubscribeToCertificateUpdatesRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SubscribeToCertificateUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SubscribeToCertificateUpdatesResponse]
        """
        Returns a Future which completes with a result of SubscribeToCertificateUpdatesResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.SubscribeToComponentUpdatesRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SubscribeToComponentUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SubscribeToComponentUpdatesResponse]
        """
        Returns a Future which completes with a result of SubscribeToComponentUpdatesResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.SubscribeToConfigurationUpdateRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SubscribeToConfigurationUpdateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SubscribeToConfigurationUpdateResponse]
        """
        Returns a Future which completes with a result of SubscribeToConfigurationUpdateResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


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

    def activate(self, request: model.SubscribeToIoTCoreRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SubscribeToIoTCoreRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SubscribeToIoTCoreResponse]
        """
        Returns a Future which completes with a result of SubscribeToIoTCoreResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.SubscribeToTopicRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SubscribeToTopicRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SubscribeToTopicResponse]
        """
        Returns a Future which completes with a result of SubscribeToTopicResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.SubscribeToValidateConfigurationUpdatesRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial SubscribeToValidateConfigurationUpdatesRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.SubscribeToValidateConfigurationUpdatesResponse]
        """
        Returns a Future which completes with a result of SubscribeToValidateConfigurationUpdatesResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.UpdateConfigurationRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial UpdateConfigurationRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.UpdateConfigurationResponse]
        """
        Returns a Future which completes with a result of UpdateConfigurationResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.UpdateStateRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial UpdateStateRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.UpdateStateResponse]
        """
        Returns a Future which completes with a result of UpdateStateResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.UpdateThingShadowRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial UpdateThingShadowRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.UpdateThingShadowResponse]
        """
        Returns a Future which completes with a result of UpdateThingShadowResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
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

    def activate(self, request: model.ValidateAuthorizationTokenRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial ValidateAuthorizationTokenRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.ValidateAuthorizationTokenResponse]
        """
        Returns a Future which completes with a result of ValidateAuthorizationTokenResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class VerifyClientDeviceIdentityOperation(model._VerifyClientDeviceIdentityOperation):
    """
    VerifyClientDeviceIdentityOperation

    Create with GreengrassCoreIPCClient.new_verify_client_device_identity()
    """

    def activate(self, request: model.VerifyClientDeviceIdentityRequest):  # type: (...) -> concurrent.futures.Future[None]
        """
        Activate this operation by sending the initial VerifyClientDeviceIdentityRequest message.

        Returns a Future which completes with a result of None if the
        request is successfully written to the wire, or an exception if
        the request fails to send.
        """
        return self._activate(request)

    def get_response(self):  # type: (...) -> concurrent.futures.Future[model.VerifyClientDeviceIdentityResponse]
        """
        Returns a Future which completes with a result of VerifyClientDeviceIdentityResponse,
        when the initial response is received, or an exception.
        """
        return self._get_response()

    def close(self):  # type: (...) -> concurrent.futures.Future[None]
        """
        Close the operation, whether or not it has completed.

        Returns a Future which completes with a result of None
        when the operation has closed.
        """
        return super().close()


class GreengrassCoreIPCClient(rpc.Client):
    """
    Client for the GreengrassCoreIPC service.
    There is a new V2 client which should be preferred.
    See the GreengrassCoreIPCClientV2 class in the clientv2 subpackage.

    Args:
        connection: Connection that this client will use.
    """

    def __init__(self, connection: rpc.Connection):
        super().__init__(connection, model.SHAPE_INDEX)

    def new_authorize_client_device_action(self) -> AuthorizeClientDeviceActionOperation:
        """
        Create a new AuthorizeClientDeviceActionOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(AuthorizeClientDeviceActionOperation)

    def new_cancel_local_deployment(self) -> CancelLocalDeploymentOperation:
        """
        Create a new CancelLocalDeploymentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(CancelLocalDeploymentOperation)

    def new_create_debug_password(self) -> CreateDebugPasswordOperation:
        """
        Create a new CreateDebugPasswordOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(CreateDebugPasswordOperation)

    def new_create_local_deployment(self) -> CreateLocalDeploymentOperation:
        """
        Create a new CreateLocalDeploymentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(CreateLocalDeploymentOperation)

    def new_defer_component_update(self) -> DeferComponentUpdateOperation:
        """
        Create a new DeferComponentUpdateOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(DeferComponentUpdateOperation)

    def new_delete_thing_shadow(self) -> DeleteThingShadowOperation:
        """
        Create a new DeleteThingShadowOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(DeleteThingShadowOperation)

    def new_get_client_device_auth_token(self) -> GetClientDeviceAuthTokenOperation:
        """
        Create a new GetClientDeviceAuthTokenOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetClientDeviceAuthTokenOperation)

    def new_get_component_details(self) -> GetComponentDetailsOperation:
        """
        Create a new GetComponentDetailsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetComponentDetailsOperation)

    def new_get_configuration(self) -> GetConfigurationOperation:
        """
        Create a new GetConfigurationOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetConfigurationOperation)

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

    def new_get_thing_shadow(self) -> GetThingShadowOperation:
        """
        Create a new GetThingShadowOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(GetThingShadowOperation)

    def new_list_components(self) -> ListComponentsOperation:
        """
        Create a new ListComponentsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ListComponentsOperation)

    def new_list_local_deployments(self) -> ListLocalDeploymentsOperation:
        """
        Create a new ListLocalDeploymentsOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ListLocalDeploymentsOperation)

    def new_list_named_shadows_for_thing(self) -> ListNamedShadowsForThingOperation:
        """
        Create a new ListNamedShadowsForThingOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ListNamedShadowsForThingOperation)

    def new_pause_component(self) -> PauseComponentOperation:
        """
        Create a new PauseComponentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(PauseComponentOperation)

    def new_publish_to_iot_core(self) -> PublishToIoTCoreOperation:
        """
        Create a new PublishToIoTCoreOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(PublishToIoTCoreOperation)

    def new_publish_to_topic(self) -> PublishToTopicOperation:
        """
        Create a new PublishToTopicOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(PublishToTopicOperation)

    def new_put_component_metric(self) -> PutComponentMetricOperation:
        """
        Create a new PutComponentMetricOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(PutComponentMetricOperation)

    def new_restart_component(self) -> RestartComponentOperation:
        """
        Create a new RestartComponentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(RestartComponentOperation)

    def new_resume_component(self) -> ResumeComponentOperation:
        """
        Create a new ResumeComponentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ResumeComponentOperation)

    def new_send_configuration_validity_report(self) -> SendConfigurationValidityReportOperation:
        """
        Create a new SendConfigurationValidityReportOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(SendConfigurationValidityReportOperation)

    def new_stop_component(self) -> StopComponentOperation:
        """
        Create a new StopComponentOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(StopComponentOperation)

    def new_subscribe_to_certificate_updates(self, stream_handler: SubscribeToCertificateUpdatesStreamHandler) -> SubscribeToCertificateUpdatesOperation:
        """
        Create a new SubscribeToCertificateUpdatesOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.

        Args:
            stream_handler: Methods on this object will be called as
                stream events happen on this operation.
        """
        return self._new_operation(SubscribeToCertificateUpdatesOperation, stream_handler)

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

    def new_update_configuration(self) -> UpdateConfigurationOperation:
        """
        Create a new UpdateConfigurationOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(UpdateConfigurationOperation)

    def new_update_state(self) -> UpdateStateOperation:
        """
        Create a new UpdateStateOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(UpdateStateOperation)

    def new_update_thing_shadow(self) -> UpdateThingShadowOperation:
        """
        Create a new UpdateThingShadowOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(UpdateThingShadowOperation)

    def new_validate_authorization_token(self) -> ValidateAuthorizationTokenOperation:
        """
        Create a new ValidateAuthorizationTokenOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(ValidateAuthorizationTokenOperation)

    def new_verify_client_device_identity(self) -> VerifyClientDeviceIdentityOperation:
        """
        Create a new VerifyClientDeviceIdentityOperation.

        This operation will not send or receive any data until activate()
        is called. Call activate() when you're ready for callbacks and
        events to fire.
        """
        return self._new_operation(VerifyClientDeviceIdentityOperation)
