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

from kubernetes.client import RbacAuthorizationV1Api, V1ClusterRole
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource


@resource(
    "kubernetes::resources::ClusterRole",
    agent="cluster.name",
    id_attribute="identifier",
)
class ClusterRoleResource(ClusterResource):

    fields = ("rules",)

    @staticmethod
    def get_rules(exporter, entity):
        return [
            {
                "apiGroups": rule.api_groups,
                "nonResourceUrls": rule.non_resource_urls,
                "resources": rule.resources,
                "resourceNames": rule.resource_names,
                "verbs": rule.verbs,
            }
            for rule in entity.rules
        ]

    @staticmethod
    def get_identifier(exporter, entity):
        return (
            ClusterResource.get_identifier(exporter, entity)
            + f"/role/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> RbacAuthorizationV1Api:
        return RbacAuthorizationV1Api(self._build_api_client())

    @property
    def api_instance(self) -> RbacAuthorizationV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider("kubernetes::resources::ClusterRole", name="cluster-role-resource")
class ClusterRoleResourceProvider(CRUDHandler):
    def read_resource(self, ctx: HandlerContext, resource: ClusterRoleResource) -> None:
        try:
            api_response: V1ClusterRole = resource.api_instance.read_cluster_role(
                resource.name
            )
            resource.labels = api_response.metadata.labels
            resource.rules = api_response.rules
            ctx.debug(str(api_response))
        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(
        self, ctx: HandlerContext, resource: ClusterRoleResource
    ) -> None:
        try:
            api_response = resource.api_instance.create_cluster_role(
                V1ClusterRole(
                    metadata={"name": resource.name, "labels": resource.labels},
                    rules=resource.rules,
                )
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(
        self, ctx: HandlerContext, resource: ClusterRoleResource
    ) -> None:
        try:
            api_response = resource.api_instance.delete_cluster_role(resource.name)
            ctx.debug(str(api_response))
            while True:
                api_response = resource.api_instance.read_cluster_role(resource.name)
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
        self, ctx: HandlerContext, changes: dict, resource: ClusterRoleResource
    ) -> None:
        try:
            current: V1ClusterRole = resource.api_instance.read_cluster_role(
                resource.name
            )
            current.metadata.labels = resource.labels
            current.rules = resource.rules
            api_response = resource.api_instance.patch_cluster_role(
                resource.name, current
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e
