"""
Copyright 2022 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

from kubernetes.client import CoreV1Api, V1ServiceAccount
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource
from inmanta_plugins.kubernetes.resources.namespaced_resource import NamespacedResource


@resource(
    "kubernetes::resources::ServiceAccount",
    agent="cluster.name",
    id_attribute="identifier",
)
class ServiceAccountResource(NamespacedResource):
    fields = ("secrets", "image_pull_secrets")

    @staticmethod
    def get_secrets(exporter, entity):
        return entity.secrets

    @staticmethod
    def get_image_pull_secrets(exporter, entity):
        return entity.image_pull_secrets

    @staticmethod
    def get_identifier(exporter, entity):
        return (
            NamespacedResource.get_identifier(exporter, entity)
            + f"/service-account/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> CoreV1Api:
        return CoreV1Api(self._build_api_client())

    @property
    def api_instance(self) -> CoreV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider("kubernetes::resources::ServiceAccount", name="service-account-resource")
class ServiceAccountResourceProvider(CRUDHandler):
    def read_resource(
        self, ctx: HandlerContext, resource: ServiceAccountResource
    ) -> None:
        try:
            api_response: V1ServiceAccount = (
                resource.api_instance.read_namespaced_service_account(
                    resource.name, resource.namespace
                )
            )
            resource.labels = api_response.metadata.labels
            resource.secrets = api_response.secrets
            resource.image_pull_secrets = api_response.image_pull_secrets
            ctx.debug(str(api_response))
        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(
        self, ctx: HandlerContext, resource: ServiceAccountResource
    ) -> None:
        try:
            api_response = resource.api_instance.create_namespaced_service_account(
                resource.namespace,
                V1ServiceAccount(
                    metadata={
                        "name": resource.name,
                        "namespace": resource.namespace,
                        "labels": resource.labels,
                    },
                    secrets=resource.secrets,
                    image_pull_secrets=resource.image_pull_secrets,
                ),
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(
        self, ctx: HandlerContext, resource: ServiceAccountResource
    ) -> None:
        try:
            api_response = resource.api_instance.delete_namespaced_service_account(
                resource.name, resource.namespace
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            if e.status != 404:
                ctx.error(str(e))
                raise e

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: ServiceAccountResource
    ) -> None:
        try:
            current: V1ServiceAccount = (
                resource.api_instance.read_namespaced_service_account(
                    resource.name, resource.namespace
                )
            )
            current.metadata.labels = resource.labels
            current.secrets = resource.secrets
            current.image_pull_secrets = resource.image_pull_secrets
            api_response = resource.api_instance.patch_namespaced_service_account(
                resource.name, resource.namespace, current
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e
