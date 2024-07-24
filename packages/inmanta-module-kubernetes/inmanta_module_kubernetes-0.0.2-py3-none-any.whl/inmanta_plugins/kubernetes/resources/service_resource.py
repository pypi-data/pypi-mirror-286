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

from kubernetes.client import CoreV1Api, V1Service
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource
from inmanta_plugins.kubernetes.resources.namespaced_resource import NamespacedResource


@resource(
    "kubernetes::resources::Service",
    agent="cluster.name",
    id_attribute="identifier",
)
class ServiceResource(NamespacedResource):
    fields = ("spec",)

    @staticmethod
    def get_spec(exporter, entity):
        return entity.spec

    @staticmethod
    def get_identifier(exporter, entity):
        return (
            NamespacedResource.get_identifier(exporter, entity)
            + f"/service/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> CoreV1Api:
        return CoreV1Api(self._build_api_client())

    @property
    def api_instance(self) -> CoreV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider("kubernetes::resources::Service", name="service-resource")
class ServiceResourceProvider(CRUDHandler):
    def read_resource(self, ctx: HandlerContext, resource: ServiceResource) -> None:
        try:
            api_response: V1Service = resource.api_instance.read_namespaced_service(
                resource.name, resource.namespace
            )
            resource.labels = api_response.metadata.labels
            resource.spec = api_response.spec
            ctx.debug(str(api_response))
        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(self, ctx: HandlerContext, resource: ServiceResource) -> None:
        try:
            api_response = resource.api_instance.create_namespaced_service(
                resource.namespace,
                V1Service(
                    metadata={
                        "name": resource.name,
                        "namespace": resource.namespace,
                        "labels": resource.labels,
                    },
                    spec=resource.spec,
                ),
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(self, ctx: HandlerContext, resource: ServiceResource) -> None:
        try:
            api_response = resource.api_instance.delete_namespaced_service(
                resource.name, resource.namespace
            )
            ctx.debug(str(api_response))
            while True:
                api_response: V1Service = resource.api_instance.read_namespaced_service(
                    resource.name, resource.namespace
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
        self, ctx: HandlerContext, changes: dict, resource: ServiceResource
    ) -> None:
        try:
            current: V1Service = resource.api_instance.read_namespaced_service(
                resource.name, resource.namespace
            )
            current.metadata.labels = resource.labels
            current.spec = resource.spec
            api_response = resource.api_instance.patch_namespaced_service(
                resource.name, resource.namespace, current
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e
