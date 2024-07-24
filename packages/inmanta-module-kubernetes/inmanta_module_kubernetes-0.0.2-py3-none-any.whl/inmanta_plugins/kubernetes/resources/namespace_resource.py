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

from kubernetes.client import CoreV1Api, V1Namespace
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource


@resource(
    "kubernetes::resources::Namespace",
    agent="cluster.name",
    id_attribute="identifier",
)
class NamespaceResource(ClusterResource):
    @staticmethod
    def get_identifier(exporter, entity):
        return (
            ClusterResource.get_identifier(exporter, entity)
            + f"/namespace/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> CoreV1Api:
        return CoreV1Api(self._build_api_client())

    @property
    def api_instance(self) -> CoreV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider("kubernetes::resources::Namespace", name="namespace-resource")
class NamespaceResourceProvider(CRUDHandler):
    def read_resource(self, ctx: HandlerContext, resource: NamespaceResource) -> None:
        try:
            api_response: V1Namespace = resource.api_instance.read_namespace(
                resource.name
            )
            resource.labels = api_response.metadata.labels
            ctx.debug(str(api_response))
        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(self, ctx: HandlerContext, resource: NamespaceResource) -> None:
        try:
            api_response = resource.api_instance.create_namespace(
                V1Namespace(metadata={"name": resource.name, "labels": resource.labels})
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(self, ctx: HandlerContext, resource: NamespaceResource) -> None:
        try:
            api_response = resource.api_instance.delete_namespace(resource.name)
            ctx.debug(str(api_response))
            while True:
                api_response = resource.api_instance.read_namespace(resource.name)
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
        self, ctx: HandlerContext, changes: dict, resource: NamespaceResource
    ) -> None:
        try:
            current: V1Namespace = resource.api_instance.read_namespace(resource.name)
            current.metadata.labels = resource.labels
            api_response = resource.api_instance.patch_namespace(resource.name, current)
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e
