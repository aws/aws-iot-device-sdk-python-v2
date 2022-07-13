# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

# This file is generated

from . import model
from .client import GreengrassCoreIPCClient
from . import client

import concurrent.futures
import datetime
import typing


class GreengrassCoreIPCClientV2:
    """
    V2 client for the GreengrassCoreIPC service.

    Args:
        client: Connection that this client will use. If you do not provide one, it will be made automatically.
        executor: Executor used to run on_stream_event and on_stream_closed callbacks to avoid blocking the networking
         thread. By default, a ThreadPoolExecutor will be created and used. Use None to run callbacks in the
         networking thread, but understand that your code can deadlock the networking thread if it performs a
         synchronous network call.
    """

    def __init__(self, client: typing.Optional[GreengrassCoreIPCClient] = None,
                 executor: typing.Optional[concurrent.futures.Executor] = True):
        if client is None:
            import awsiot.greengrasscoreipc
            client = awsiot.greengrasscoreipc.connect()
        self.client = client
        if executor is True:
            executor = concurrent.futures.ThreadPoolExecutor()
        self.executor = executor

    def close(self, *, executor_wait=True) -> concurrent.futures.Future:
        """
        Close the underlying connection and shutdown the event executor (if any)

        Args:
            executor_wait: If true (default), then this method will block until the executor finishes running
                all tasks and shuts down.

        Returns:
            The future which will complete
            when the shutdown process is done. The future will have an
            exception if shutdown was caused by an error, or a result
            of None if the shutdown was clean and user-initiated.
        """
        fut = self.client.close()
        if self.executor is not None:
            self.executor.shutdown(wait=executor_wait)
        return fut

    def __combine_futures(self, future1: concurrent.futures.Future,
                          future2: concurrent.futures.Future) -> concurrent.futures.Future:
        def callback(*args, **kwargs):
            try:
                future1.result()
            except Exception as e:
                future2.set_exception(e)
        future1.add_done_callback(callback)
        return future2

    @staticmethod
    def __handle_error():
        import sys
        import traceback
        traceback.print_exc(file=sys.stderr)

    def __wrap_error(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.__handle_error()
                raise e
        return wrapper

    def __create_stream_handler(real_self, operation, on_stream_event, on_stream_error, on_stream_closed):
        stream_handler_type = type(operation + 'Handler', (getattr(client, operation + "StreamHandler"),), {})
        if on_stream_event is not None:
            on_stream_event = real_self.__wrap_error(on_stream_event)
            def handler(self, event):
                if real_self.executor is not None:
                    real_self.executor.submit(on_stream_event, event)
                else:
                    on_stream_event(event)
            setattr(stream_handler_type, "on_stream_event", handler)
        if on_stream_error is not None:
            on_stream_error = real_self.__wrap_error(on_stream_error)
            def handler(self, error):
                return on_stream_error(error)
            setattr(stream_handler_type, "on_stream_error", handler)
        if on_stream_closed is not None:
            on_stream_closed = real_self.__wrap_error(on_stream_closed)
            def handler(self):
                if real_self.executor is not None:
                    real_self.executor.submit(on_stream_closed)
                else:
                    on_stream_closed()
            setattr(stream_handler_type, "on_stream_closed", handler)
        return stream_handler_type()

    def __handle_stream_handler(real_self, operation, stream_handler, on_stream_event, on_stream_error, on_stream_closed):
        if stream_handler is not None and (on_stream_event is not None or on_stream_error is not None or on_stream_closed is not None):
            raise ValueError("Must choose either stream_handler or on_stream_event/on_stream_error/on_stream_closed")
        if stream_handler is not None and real_self.executor is not None:
            return real_self.__create_stream_handler(operation, stream_handler.on_stream_event,
                                                     stream_handler.on_stream_error, stream_handler.on_stream_closed)
        if stream_handler is None:
            return real_self.__create_stream_handler(operation, on_stream_event, on_stream_error, on_stream_closed)
        return stream_handler

    def authorize_client_device_action(self, *,
        client_device_auth_token: typing.Optional[str] = None,
        operation: typing.Optional[str] = None,
        resource: typing.Optional[str] = None) -> model.AuthorizeClientDeviceActionResponse:
        """
        Perform the AuthorizeClientDeviceAction operation synchronously.

        Args:
            client_device_auth_token: 
            operation: 
            resource: 
        """
        return self.authorize_client_device_action_async(client_device_auth_token=client_device_auth_token, operation=operation, resource=resource).result()

    def authorize_client_device_action_async(self, *,
        client_device_auth_token: typing.Optional[str] = None,
        operation: typing.Optional[str] = None,
        resource: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.AuthorizeClientDeviceActionResponse]
        """
        Perform the AuthorizeClientDeviceAction operation asynchronously.

        Args:
            client_device_auth_token: 
            operation: 
            resource: 
        """
        request = model.AuthorizeClientDeviceActionRequest(client_device_auth_token=client_device_auth_token, operation=operation, resource=resource)
        operation = self.client.new_authorize_client_device_action()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def create_debug_password(self) -> model.CreateDebugPasswordResponse:
        """
        Perform the CreateDebugPassword operation synchronously.

        """
        return self.create_debug_password_async().result()

    def create_debug_password_async(self):  # type: (...) -> concurrent.futures.Future[model.CreateDebugPasswordResponse]
        """
        Perform the CreateDebugPassword operation asynchronously.

        """
        request = model.CreateDebugPasswordRequest()
        operation = self.client.new_create_debug_password()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def create_local_deployment(self, *,
        group_name: typing.Optional[str] = None,
        root_component_versions_to_add: typing.Optional[typing.Dict[str, str]] = None,
        root_components_to_remove: typing.Optional[typing.List[str]] = None,
        component_to_configuration: typing.Optional[typing.Dict[str, typing.Dict[str, typing.Any]]] = None,
        component_to_run_with_info: typing.Optional[typing.Dict[str, model.RunWithInfo]] = None,
        recipe_directory_path: typing.Optional[str] = None,
        artifacts_directory_path: typing.Optional[str] = None) -> model.CreateLocalDeploymentResponse:
        """
        Perform the CreateLocalDeployment operation synchronously.

        Args:
            group_name: 
            root_component_versions_to_add: 
            root_components_to_remove: 
            component_to_configuration: 
            component_to_run_with_info: 
            recipe_directory_path: 
            artifacts_directory_path: 
        """
        return self.create_local_deployment_async(group_name=group_name, root_component_versions_to_add=root_component_versions_to_add, root_components_to_remove=root_components_to_remove, component_to_configuration=component_to_configuration, component_to_run_with_info=component_to_run_with_info, recipe_directory_path=recipe_directory_path, artifacts_directory_path=artifacts_directory_path).result()

    def create_local_deployment_async(self, *,
        group_name: typing.Optional[str] = None,
        root_component_versions_to_add: typing.Optional[typing.Dict[str, str]] = None,
        root_components_to_remove: typing.Optional[typing.List[str]] = None,
        component_to_configuration: typing.Optional[typing.Dict[str, typing.Dict[str, typing.Any]]] = None,
        component_to_run_with_info: typing.Optional[typing.Dict[str, model.RunWithInfo]] = None,
        recipe_directory_path: typing.Optional[str] = None,
        artifacts_directory_path: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.CreateLocalDeploymentResponse]
        """
        Perform the CreateLocalDeployment operation asynchronously.

        Args:
            group_name: 
            root_component_versions_to_add: 
            root_components_to_remove: 
            component_to_configuration: 
            component_to_run_with_info: 
            recipe_directory_path: 
            artifacts_directory_path: 
        """
        request = model.CreateLocalDeploymentRequest(group_name=group_name, root_component_versions_to_add=root_component_versions_to_add, root_components_to_remove=root_components_to_remove, component_to_configuration=component_to_configuration, component_to_run_with_info=component_to_run_with_info, recipe_directory_path=recipe_directory_path, artifacts_directory_path=artifacts_directory_path)
        operation = self.client.new_create_local_deployment()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def defer_component_update(self, *,
        deployment_id: typing.Optional[str] = None,
        message: typing.Optional[str] = None,
        recheck_after_ms: typing.Optional[int] = None) -> model.DeferComponentUpdateResponse:
        """
        Perform the DeferComponentUpdate operation synchronously.

        Args:
            deployment_id: 
            message: 
            recheck_after_ms: 
        """
        return self.defer_component_update_async(deployment_id=deployment_id, message=message, recheck_after_ms=recheck_after_ms).result()

    def defer_component_update_async(self, *,
        deployment_id: typing.Optional[str] = None,
        message: typing.Optional[str] = None,
        recheck_after_ms: typing.Optional[int] = None):  # type: (...) -> concurrent.futures.Future[model.DeferComponentUpdateResponse]
        """
        Perform the DeferComponentUpdate operation asynchronously.

        Args:
            deployment_id: 
            message: 
            recheck_after_ms: 
        """
        request = model.DeferComponentUpdateRequest(deployment_id=deployment_id, message=message, recheck_after_ms=recheck_after_ms)
        operation = self.client.new_defer_component_update()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def delete_thing_shadow(self, *,
        thing_name: typing.Optional[str] = None,
        shadow_name: typing.Optional[str] = None) -> model.DeleteThingShadowResponse:
        """
        Perform the DeleteThingShadow operation synchronously.

        Args:
            thing_name: 
            shadow_name: 
        """
        return self.delete_thing_shadow_async(thing_name=thing_name, shadow_name=shadow_name).result()

    def delete_thing_shadow_async(self, *,
        thing_name: typing.Optional[str] = None,
        shadow_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.DeleteThingShadowResponse]
        """
        Perform the DeleteThingShadow operation asynchronously.

        Args:
            thing_name: 
            shadow_name: 
        """
        request = model.DeleteThingShadowRequest(thing_name=thing_name, shadow_name=shadow_name)
        operation = self.client.new_delete_thing_shadow()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_client_device_auth_token(self, *,
        credential: typing.Optional[model.CredentialDocument] = None) -> model.GetClientDeviceAuthTokenResponse:
        """
        Perform the GetClientDeviceAuthToken operation synchronously.

        Args:
            credential: 
        """
        return self.get_client_device_auth_token_async(credential=credential).result()

    def get_client_device_auth_token_async(self, *,
        credential: typing.Optional[model.CredentialDocument] = None):  # type: (...) -> concurrent.futures.Future[model.GetClientDeviceAuthTokenResponse]
        """
        Perform the GetClientDeviceAuthToken operation asynchronously.

        Args:
            credential: 
        """
        request = model.GetClientDeviceAuthTokenRequest(credential=credential)
        operation = self.client.new_get_client_device_auth_token()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_component_details(self, *,
        component_name: typing.Optional[str] = None) -> model.GetComponentDetailsResponse:
        """
        Perform the GetComponentDetails operation synchronously.

        Args:
            component_name: 
        """
        return self.get_component_details_async(component_name=component_name).result()

    def get_component_details_async(self, *,
        component_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.GetComponentDetailsResponse]
        """
        Perform the GetComponentDetails operation asynchronously.

        Args:
            component_name: 
        """
        request = model.GetComponentDetailsRequest(component_name=component_name)
        operation = self.client.new_get_component_details()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_configuration(self, *,
        component_name: typing.Optional[str] = None,
        key_path: typing.Optional[typing.List[str]] = None) -> model.GetConfigurationResponse:
        """
        Perform the GetConfiguration operation synchronously.

        Args:
            component_name: 
            key_path: 
        """
        return self.get_configuration_async(component_name=component_name, key_path=key_path).result()

    def get_configuration_async(self, *,
        component_name: typing.Optional[str] = None,
        key_path: typing.Optional[typing.List[str]] = None):  # type: (...) -> concurrent.futures.Future[model.GetConfigurationResponse]
        """
        Perform the GetConfiguration operation asynchronously.

        Args:
            component_name: 
            key_path: 
        """
        request = model.GetConfigurationRequest(component_name=component_name, key_path=key_path)
        operation = self.client.new_get_configuration()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_local_deployment_status(self, *,
        deployment_id: typing.Optional[str] = None) -> model.GetLocalDeploymentStatusResponse:
        """
        Perform the GetLocalDeploymentStatus operation synchronously.

        Args:
            deployment_id: 
        """
        return self.get_local_deployment_status_async(deployment_id=deployment_id).result()

    def get_local_deployment_status_async(self, *,
        deployment_id: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.GetLocalDeploymentStatusResponse]
        """
        Perform the GetLocalDeploymentStatus operation asynchronously.

        Args:
            deployment_id: 
        """
        request = model.GetLocalDeploymentStatusRequest(deployment_id=deployment_id)
        operation = self.client.new_get_local_deployment_status()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_secret_value(self, *,
        secret_id: typing.Optional[str] = None,
        version_id: typing.Optional[str] = None,
        version_stage: typing.Optional[str] = None) -> model.GetSecretValueResponse:
        """
        Perform the GetSecretValue operation synchronously.

        Args:
            secret_id: 
            version_id: 
            version_stage: 
        """
        return self.get_secret_value_async(secret_id=secret_id, version_id=version_id, version_stage=version_stage).result()

    def get_secret_value_async(self, *,
        secret_id: typing.Optional[str] = None,
        version_id: typing.Optional[str] = None,
        version_stage: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.GetSecretValueResponse]
        """
        Perform the GetSecretValue operation asynchronously.

        Args:
            secret_id: 
            version_id: 
            version_stage: 
        """
        request = model.GetSecretValueRequest(secret_id=secret_id, version_id=version_id, version_stage=version_stage)
        operation = self.client.new_get_secret_value()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def get_thing_shadow(self, *,
        thing_name: typing.Optional[str] = None,
        shadow_name: typing.Optional[str] = None) -> model.GetThingShadowResponse:
        """
        Perform the GetThingShadow operation synchronously.

        Args:
            thing_name: 
            shadow_name: 
        """
        return self.get_thing_shadow_async(thing_name=thing_name, shadow_name=shadow_name).result()

    def get_thing_shadow_async(self, *,
        thing_name: typing.Optional[str] = None,
        shadow_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.GetThingShadowResponse]
        """
        Perform the GetThingShadow operation asynchronously.

        Args:
            thing_name: 
            shadow_name: 
        """
        request = model.GetThingShadowRequest(thing_name=thing_name, shadow_name=shadow_name)
        operation = self.client.new_get_thing_shadow()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def list_components(self) -> model.ListComponentsResponse:
        """
        Perform the ListComponents operation synchronously.

        """
        return self.list_components_async().result()

    def list_components_async(self):  # type: (...) -> concurrent.futures.Future[model.ListComponentsResponse]
        """
        Perform the ListComponents operation asynchronously.

        """
        request = model.ListComponentsRequest()
        operation = self.client.new_list_components()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def list_local_deployments(self) -> model.ListLocalDeploymentsResponse:
        """
        Perform the ListLocalDeployments operation synchronously.

        """
        return self.list_local_deployments_async().result()

    def list_local_deployments_async(self):  # type: (...) -> concurrent.futures.Future[model.ListLocalDeploymentsResponse]
        """
        Perform the ListLocalDeployments operation asynchronously.

        """
        request = model.ListLocalDeploymentsRequest()
        operation = self.client.new_list_local_deployments()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def list_named_shadows_for_thing(self, *,
        thing_name: typing.Optional[str] = None,
        next_token: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None) -> model.ListNamedShadowsForThingResponse:
        """
        Perform the ListNamedShadowsForThing operation synchronously.

        Args:
            thing_name: 
            next_token: 
            page_size: 
        """
        return self.list_named_shadows_for_thing_async(thing_name=thing_name, next_token=next_token, page_size=page_size).result()

    def list_named_shadows_for_thing_async(self, *,
        thing_name: typing.Optional[str] = None,
        next_token: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None):  # type: (...) -> concurrent.futures.Future[model.ListNamedShadowsForThingResponse]
        """
        Perform the ListNamedShadowsForThing operation asynchronously.

        Args:
            thing_name: 
            next_token: 
            page_size: 
        """
        request = model.ListNamedShadowsForThingRequest(thing_name=thing_name, next_token=next_token, page_size=page_size)
        operation = self.client.new_list_named_shadows_for_thing()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def pause_component(self, *,
        component_name: typing.Optional[str] = None) -> model.PauseComponentResponse:
        """
        Perform the PauseComponent operation synchronously.

        Args:
            component_name: 
        """
        return self.pause_component_async(component_name=component_name).result()

    def pause_component_async(self, *,
        component_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.PauseComponentResponse]
        """
        Perform the PauseComponent operation asynchronously.

        Args:
            component_name: 
        """
        request = model.PauseComponentRequest(component_name=component_name)
        operation = self.client.new_pause_component()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def publish_to_iot_core(self, *,
        topic_name: typing.Optional[str] = None,
        qos: typing.Optional[str] = None,
        payload: typing.Optional[typing.Union[bytes, str]] = None) -> model.PublishToIoTCoreResponse:
        """
        Perform the PublishToIoTCore operation synchronously.

        Args:
            topic_name: 
            qos: QOS enum value
            payload: 
        """
        return self.publish_to_iot_core_async(topic_name=topic_name, qos=qos, payload=payload).result()

    def publish_to_iot_core_async(self, *,
        topic_name: typing.Optional[str] = None,
        qos: typing.Optional[str] = None,
        payload: typing.Optional[typing.Union[bytes, str]] = None):  # type: (...) -> concurrent.futures.Future[model.PublishToIoTCoreResponse]
        """
        Perform the PublishToIoTCore operation asynchronously.

        Args:
            topic_name: 
            qos: QOS enum value
            payload: 
        """
        request = model.PublishToIoTCoreRequest(topic_name=topic_name, qos=qos, payload=payload)
        operation = self.client.new_publish_to_iot_core()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def publish_to_topic(self, *,
        topic: typing.Optional[str] = None,
        publish_message: typing.Optional[model.PublishMessage] = None) -> model.PublishToTopicResponse:
        """
        Perform the PublishToTopic operation synchronously.

        Args:
            topic: 
            publish_message: 
        """
        return self.publish_to_topic_async(topic=topic, publish_message=publish_message).result()

    def publish_to_topic_async(self, *,
        topic: typing.Optional[str] = None,
        publish_message: typing.Optional[model.PublishMessage] = None):  # type: (...) -> concurrent.futures.Future[model.PublishToTopicResponse]
        """
        Perform the PublishToTopic operation asynchronously.

        Args:
            topic: 
            publish_message: 
        """
        request = model.PublishToTopicRequest(topic=topic, publish_message=publish_message)
        operation = self.client.new_publish_to_topic()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def put_component_metric(self, *,
        metrics: typing.Optional[typing.List[model.Metric]] = None) -> model.PutComponentMetricResponse:
        """
        Perform the PutComponentMetric operation synchronously.

        Args:
            metrics: 
        """
        return self.put_component_metric_async(metrics=metrics).result()

    def put_component_metric_async(self, *,
        metrics: typing.Optional[typing.List[model.Metric]] = None):  # type: (...) -> concurrent.futures.Future[model.PutComponentMetricResponse]
        """
        Perform the PutComponentMetric operation asynchronously.

        Args:
            metrics: 
        """
        request = model.PutComponentMetricRequest(metrics=metrics)
        operation = self.client.new_put_component_metric()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def restart_component(self, *,
        component_name: typing.Optional[str] = None) -> model.RestartComponentResponse:
        """
        Perform the RestartComponent operation synchronously.

        Args:
            component_name: 
        """
        return self.restart_component_async(component_name=component_name).result()

    def restart_component_async(self, *,
        component_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.RestartComponentResponse]
        """
        Perform the RestartComponent operation asynchronously.

        Args:
            component_name: 
        """
        request = model.RestartComponentRequest(component_name=component_name)
        operation = self.client.new_restart_component()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def resume_component(self, *,
        component_name: typing.Optional[str] = None) -> model.ResumeComponentResponse:
        """
        Perform the ResumeComponent operation synchronously.

        Args:
            component_name: 
        """
        return self.resume_component_async(component_name=component_name).result()

    def resume_component_async(self, *,
        component_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.ResumeComponentResponse]
        """
        Perform the ResumeComponent operation asynchronously.

        Args:
            component_name: 
        """
        request = model.ResumeComponentRequest(component_name=component_name)
        operation = self.client.new_resume_component()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def send_configuration_validity_report(self, *,
        configuration_validity_report: typing.Optional[model.ConfigurationValidityReport] = None) -> model.SendConfigurationValidityReportResponse:
        """
        Perform the SendConfigurationValidityReport operation synchronously.

        Args:
            configuration_validity_report: 
        """
        return self.send_configuration_validity_report_async(configuration_validity_report=configuration_validity_report).result()

    def send_configuration_validity_report_async(self, *,
        configuration_validity_report: typing.Optional[model.ConfigurationValidityReport] = None):  # type: (...) -> concurrent.futures.Future[model.SendConfigurationValidityReportResponse]
        """
        Perform the SendConfigurationValidityReport operation asynchronously.

        Args:
            configuration_validity_report: 
        """
        request = model.SendConfigurationValidityReportRequest(configuration_validity_report=configuration_validity_report)
        operation = self.client.new_send_configuration_validity_report()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def stop_component(self, *,
        component_name: typing.Optional[str] = None) -> model.StopComponentResponse:
        """
        Perform the StopComponent operation synchronously.

        Args:
            component_name: 
        """
        return self.stop_component_async(component_name=component_name).result()

    def stop_component_async(self, *,
        component_name: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.StopComponentResponse]
        """
        Perform the StopComponent operation asynchronously.

        Args:
            component_name: 
        """
        request = model.StopComponentRequest(component_name=component_name)
        operation = self.client.new_stop_component()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def subscribe_to_certificate_updates(self, *,
        certificate_options: typing.Optional[model.CertificateOptions] = None,
        stream_handler: typing.Optional[client.SubscribeToCertificateUpdatesStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.CertificateUpdateEvent], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.SubscribeToCertificateUpdatesResponse, client.SubscribeToCertificateUpdatesOperation]:
        """
        Perform the SubscribeToCertificateUpdates operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            certificate_options: 
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.subscribe_to_certificate_updates_async(certificate_options=certificate_options, 
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def subscribe_to_certificate_updates_async(self, *,
        certificate_options: typing.Optional[model.CertificateOptions] = None,
        stream_handler: client.SubscribeToCertificateUpdatesStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.CertificateUpdateEvent], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.SubscribeToCertificateUpdatesResponse], client.SubscribeToCertificateUpdatesOperation]
        """
        Perform the SubscribeToCertificateUpdates operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            certificate_options: 
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("SubscribeToCertificateUpdates", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.SubscribeToCertificateUpdatesRequest(certificate_options=certificate_options)
        operation = self.client.new_subscribe_to_certificate_updates(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def subscribe_to_component_updates(self, *,
        stream_handler: typing.Optional[client.SubscribeToComponentUpdatesStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.ComponentUpdatePolicyEvents], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.SubscribeToComponentUpdatesResponse, client.SubscribeToComponentUpdatesOperation]:
        """
        Perform the SubscribeToComponentUpdates operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.subscribe_to_component_updates_async(
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def subscribe_to_component_updates_async(self, *,
        stream_handler: client.SubscribeToComponentUpdatesStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.ComponentUpdatePolicyEvents], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.SubscribeToComponentUpdatesResponse], client.SubscribeToComponentUpdatesOperation]
        """
        Perform the SubscribeToComponentUpdates operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("SubscribeToComponentUpdates", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.SubscribeToComponentUpdatesRequest()
        operation = self.client.new_subscribe_to_component_updates(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def subscribe_to_configuration_update(self, *,
        component_name: typing.Optional[str] = None,
        key_path: typing.Optional[typing.List[str]] = None,
        stream_handler: typing.Optional[client.SubscribeToConfigurationUpdateStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.ConfigurationUpdateEvents], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.SubscribeToConfigurationUpdateResponse, client.SubscribeToConfigurationUpdateOperation]:
        """
        Perform the SubscribeToConfigurationUpdate operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            component_name: 
            key_path: 
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.subscribe_to_configuration_update_async(component_name=component_name, key_path=key_path, 
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def subscribe_to_configuration_update_async(self, *,
        component_name: typing.Optional[str] = None,
        key_path: typing.Optional[typing.List[str]] = None,
        stream_handler: client.SubscribeToConfigurationUpdateStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.ConfigurationUpdateEvents], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.SubscribeToConfigurationUpdateResponse], client.SubscribeToConfigurationUpdateOperation]
        """
        Perform the SubscribeToConfigurationUpdate operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            component_name: 
            key_path: 
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("SubscribeToConfigurationUpdate", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.SubscribeToConfigurationUpdateRequest(component_name=component_name, key_path=key_path)
        operation = self.client.new_subscribe_to_configuration_update(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def subscribe_to_iot_core(self, *,
        topic_name: typing.Optional[str] = None,
        qos: typing.Optional[str] = None,
        stream_handler: typing.Optional[client.SubscribeToIoTCoreStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.IoTCoreMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.SubscribeToIoTCoreResponse, client.SubscribeToIoTCoreOperation]:
        """
        Perform the SubscribeToIoTCore operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            topic_name: 
            qos: QOS enum value
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.subscribe_to_iot_core_async(topic_name=topic_name, qos=qos, 
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def subscribe_to_iot_core_async(self, *,
        topic_name: typing.Optional[str] = None,
        qos: typing.Optional[str] = None,
        stream_handler: client.SubscribeToIoTCoreStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.IoTCoreMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.SubscribeToIoTCoreResponse], client.SubscribeToIoTCoreOperation]
        """
        Perform the SubscribeToIoTCore operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            topic_name: 
            qos: QOS enum value
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("SubscribeToIoTCore", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.SubscribeToIoTCoreRequest(topic_name=topic_name, qos=qos)
        operation = self.client.new_subscribe_to_iot_core(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def subscribe_to_topic(self, *,
        topic: typing.Optional[str] = None,
        receive_mode: typing.Optional[str] = None,
        stream_handler: typing.Optional[client.SubscribeToTopicStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.SubscriptionResponseMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.SubscribeToTopicResponse, client.SubscribeToTopicOperation]:
        """
        Perform the SubscribeToTopic operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            topic: 
            receive_mode: ReceiveMode enum value
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.subscribe_to_topic_async(topic=topic, receive_mode=receive_mode, 
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def subscribe_to_topic_async(self, *,
        topic: typing.Optional[str] = None,
        receive_mode: typing.Optional[str] = None,
        stream_handler: client.SubscribeToTopicStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.SubscriptionResponseMessage], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.SubscribeToTopicResponse], client.SubscribeToTopicOperation]
        """
        Perform the SubscribeToTopic operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            topic: 
            receive_mode: ReceiveMode enum value
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("SubscribeToTopic", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.SubscribeToTopicRequest(topic=topic, receive_mode=receive_mode)
        operation = self.client.new_subscribe_to_topic(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def subscribe_to_validate_configuration_updates(self, *,
        stream_handler: typing.Optional[client.SubscribeToValidateConfigurationUpdatesStreamHandler] = None,
        on_stream_event: typing.Optional[typing.Callable[[model.ValidateConfigurationUpdateEvents], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
) -> typing.Tuple[model.SubscribeToValidateConfigurationUpdatesResponse, client.SubscribeToValidateConfigurationUpdatesOperation]:
        """
        Perform the SubscribeToValidateConfigurationUpdates operation synchronously.
        The initial response or error will be returned synchronously, further events will arrive via the streaming
        callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        (fut, op) = self.subscribe_to_validate_configuration_updates_async(
            stream_handler=stream_handler, on_stream_event=on_stream_event, on_stream_error=on_stream_error,
            on_stream_closed=on_stream_closed)
        return fut.result(), op

    def subscribe_to_validate_configuration_updates_async(self, *,
        stream_handler: client.SubscribeToValidateConfigurationUpdatesStreamHandler = None,
        on_stream_event: typing.Optional[typing.Callable[[model.ValidateConfigurationUpdateEvents], None]] = None,
        on_stream_error: typing.Optional[typing.Callable[[Exception], bool]] = None,
        on_stream_closed: typing.Optional[typing.Callable[[], None]] = None
        ):  # type: (...) -> typing.Tuple[concurrent.futures.Future[model.SubscribeToValidateConfigurationUpdatesResponse], client.SubscribeToValidateConfigurationUpdatesOperation]
        """
        Perform the SubscribeToValidateConfigurationUpdates operation asynchronously.
        The initial response or error will be returned as the result of the asynchronous future, further events will
        arrive via the streaming callbacks

        Args:
            stream_handler: Methods on this object will be called as stream events happen on this operation. If an
                executor is provided, the on_stream_event and on_stream_closed methods will run in the executor.
            on_stream_event: Callback for stream events. Mutually exclusive with stream_handler. If an executor is
                provided, this method will run in the executor.
            on_stream_error: Callback for stream errors. Return true to close the stream, return false to keep the
                stream open. Mutually exclusive with stream_handler. Even if an executor is provided, this method
                will not run in the executor.
            on_stream_closed: Callback for when the stream closes. Mutually exclusive with stream_handler. If an
                executor is provided, this method will run in the executor.
        """
        stream_handler = self.__handle_stream_handler("SubscribeToValidateConfigurationUpdates", stream_handler,
            on_stream_event, on_stream_error, on_stream_closed)
        request = model.SubscribeToValidateConfigurationUpdatesRequest()
        operation = self.client.new_subscribe_to_validate_configuration_updates(stream_handler)
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response()), operation

    def update_configuration(self, *,
        key_path: typing.Optional[typing.List[str]] = None,
        timestamp: typing.Optional[datetime.datetime] = None,
        value_to_merge: typing.Optional[typing.Dict[str, typing.Any]] = None) -> model.UpdateConfigurationResponse:
        """
        Perform the UpdateConfiguration operation synchronously.

        Args:
            key_path: 
            timestamp: 
            value_to_merge: 
        """
        return self.update_configuration_async(key_path=key_path, timestamp=timestamp, value_to_merge=value_to_merge).result()

    def update_configuration_async(self, *,
        key_path: typing.Optional[typing.List[str]] = None,
        timestamp: typing.Optional[datetime.datetime] = None,
        value_to_merge: typing.Optional[typing.Dict[str, typing.Any]] = None):  # type: (...) -> concurrent.futures.Future[model.UpdateConfigurationResponse]
        """
        Perform the UpdateConfiguration operation asynchronously.

        Args:
            key_path: 
            timestamp: 
            value_to_merge: 
        """
        request = model.UpdateConfigurationRequest(key_path=key_path, timestamp=timestamp, value_to_merge=value_to_merge)
        operation = self.client.new_update_configuration()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def update_state(self, *,
        state: typing.Optional[str] = None) -> model.UpdateStateResponse:
        """
        Perform the UpdateState operation synchronously.

        Args:
            state: ReportedLifecycleState enum value
        """
        return self.update_state_async(state=state).result()

    def update_state_async(self, *,
        state: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.UpdateStateResponse]
        """
        Perform the UpdateState operation asynchronously.

        Args:
            state: ReportedLifecycleState enum value
        """
        request = model.UpdateStateRequest(state=state)
        operation = self.client.new_update_state()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def update_thing_shadow(self, *,
        thing_name: typing.Optional[str] = None,
        shadow_name: typing.Optional[str] = None,
        payload: typing.Optional[typing.Union[bytes, str]] = None) -> model.UpdateThingShadowResponse:
        """
        Perform the UpdateThingShadow operation synchronously.

        Args:
            thing_name: 
            shadow_name: 
            payload: 
        """
        return self.update_thing_shadow_async(thing_name=thing_name, shadow_name=shadow_name, payload=payload).result()

    def update_thing_shadow_async(self, *,
        thing_name: typing.Optional[str] = None,
        shadow_name: typing.Optional[str] = None,
        payload: typing.Optional[typing.Union[bytes, str]] = None):  # type: (...) -> concurrent.futures.Future[model.UpdateThingShadowResponse]
        """
        Perform the UpdateThingShadow operation asynchronously.

        Args:
            thing_name: 
            shadow_name: 
            payload: 
        """
        request = model.UpdateThingShadowRequest(thing_name=thing_name, shadow_name=shadow_name, payload=payload)
        operation = self.client.new_update_thing_shadow()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def validate_authorization_token(self, *,
        token: typing.Optional[str] = None) -> model.ValidateAuthorizationTokenResponse:
        """
        Perform the ValidateAuthorizationToken operation synchronously.

        Args:
            token: 
        """
        return self.validate_authorization_token_async(token=token).result()

    def validate_authorization_token_async(self, *,
        token: typing.Optional[str] = None):  # type: (...) -> concurrent.futures.Future[model.ValidateAuthorizationTokenResponse]
        """
        Perform the ValidateAuthorizationToken operation asynchronously.

        Args:
            token: 
        """
        request = model.ValidateAuthorizationTokenRequest(token=token)
        operation = self.client.new_validate_authorization_token()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())

    def verify_client_device_identity(self, *,
        credential: typing.Optional[model.ClientDeviceCredential] = None) -> model.VerifyClientDeviceIdentityResponse:
        """
        Perform the VerifyClientDeviceIdentity operation synchronously.

        Args:
            credential: 
        """
        return self.verify_client_device_identity_async(credential=credential).result()

    def verify_client_device_identity_async(self, *,
        credential: typing.Optional[model.ClientDeviceCredential] = None):  # type: (...) -> concurrent.futures.Future[model.VerifyClientDeviceIdentityResponse]
        """
        Perform the VerifyClientDeviceIdentity operation asynchronously.

        Args:
            credential: 
        """
        request = model.VerifyClientDeviceIdentityRequest(credential=credential)
        operation = self.client.new_verify_client_device_identity()
        write_future = operation.activate(request)
        return self.__combine_futures(write_future, operation.get_response())
