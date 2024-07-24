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

import time

from kubernetes.client import AppsV1Api, V1Deployment, V1Status
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource
from inmanta_plugins.kubernetes.resources.namespaced_resource import NamespacedResource


@resource(
    "kubernetes::resources::Deployment",
    agent="cluster.name",
    id_attribute="identifier",
)
class DeploymentResource(NamespacedResource):
    fields = ("spec",)

    @staticmethod
    def get_spec(exporter, entity):
        return entity.spec

    @staticmethod
    def get_identifier(exporter, entity):
        return (
            NamespacedResource.get_identifier(exporter, entity)
            + f"/deployment/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> AppsV1Api:
        return AppsV1Api(self._build_api_client())

    @property
    def api_instance(self) -> AppsV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider("kubernetes::resources::Deployment", name="deployment-resource")
class DeploymentResourceProvider(CRUDHandler):
    def read_resource(self, ctx: HandlerContext, resource: DeploymentResource) -> None:
        try:
            api_response: V1Deployment = (
                resource.api_instance.read_namespaced_deployment(
                    resource.name, resource.namespace
                )
            )
            resource.labels = api_response.metadata.labels
            resource.spec = api_response.spec
            ctx.debug(str(api_response.status))
        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(
        self, ctx: HandlerContext, resource: DeploymentResource
    ) -> None:
        try:
            api_response: V1Deployment = (
                resource.api_instance.create_namespaced_deployment(
                    resource.namespace,
                    V1Deployment(
                        metadata={
                            "name": resource.name,
                            "namespace": resource.namespace,
                            "labels": resource.labels,
                        },
                        spec=resource.spec,
                    ),
                )
            )
            ctx.debug(str(api_response.status))
        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(
        self, ctx: HandlerContext, resource: DeploymentResource
    ) -> None:
        try:
            api_response: V1Status = resource.api_instance.delete_namespaced_deployment(
                resource.name, resource.namespace
            )
            ctx.debug(str(api_response))
            while True:
                api_response: V1Deployment = (
                    resource.api_instance.read_namespaced_deployment(
                        resource.name, resource.namespace
                    )
                )
                if api_response.status.phase != "Terminating":
                    raise Exception(
                        "Unexpected response when trying to delete resource, phase is "
                        f"{api_response.status.phase} (expected Terminating)"
                    )

                time.sleep(0.5)
        except ApiException as e:
            if e.status != 404:
                ctx.error(str(e))
                raise e

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: DeploymentResource
    ) -> None:
        try:
            current: V1Deployment = resource.api_instance.read_namespaced_deployment(
                resource.name, resource.namespace
            )
            current.metadata.labels = resource.labels
            current.spec = resource.spec
            api_response: V1Deployment = (
                resource.api_instance.patch_namespaced_deployment(
                    resource.name, resource.namespace, current
                )
            )
            ctx.debug(str(api_response.status))
        except ApiException as e:
            ctx.error(str(e))
            raise e
