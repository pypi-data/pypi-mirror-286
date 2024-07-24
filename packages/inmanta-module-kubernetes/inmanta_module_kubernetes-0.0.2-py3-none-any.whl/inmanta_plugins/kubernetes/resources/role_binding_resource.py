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

from kubernetes.client import (
    RbacAuthorizationV1Api,
    V1ClusterRoleBinding,
    V1RoleBinding,
)
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource
from inmanta_plugins.kubernetes.resources.namespaced_resource import NamespacedResource


@resource(
    "kubernetes::resources::NamespacedRoleBinding",
    agent="cluster.name",
    id_attribute="identifier",
)
class NamespacedRoleBindingResource(NamespacedResource):

    fields = ("subjects", "role_ref")

    @staticmethod
    def get_subjects(exporter, entity):
        subjects = []
        for subject in entity.subjects:
            obj = {
                "kind": subject.kind,
                "name": subject.name,
            }
            if subject.api_group is not None:
                obj["apiGroup"] = subject.api_group
            if subject.namespace is not None:
                obj["namespace"] = subject.namespace
            subjects.append(obj)

        return subjects

    @staticmethod
    def get_role_ref(exporter, entity):
        return {
            "kind": entity.role_ref._kind,
            "name": entity.role_ref.name,
            "apiGroup": entity.role_ref._api_group,
        }

    @staticmethod
    def get_identifier(exporter, entity):
        return (
            NamespacedResource.get_identifier(exporter, entity)
            + f"/role-binding/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> RbacAuthorizationV1Api:
        return RbacAuthorizationV1Api(self._build_api_client())

    @property
    def api_instance(self) -> RbacAuthorizationV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider(
    "kubernetes::resources::NamespacedRoleBinding",
    name="namespaced-role-binding-resource",
)
class NamespacedRoleBindingResourceProvider(CRUDHandler):
    def read_resource(
        self, ctx: HandlerContext, resource: NamespacedRoleBindingResource
    ) -> None:
        try:
            api_response: V1RoleBinding = (
                resource.api_instance.read_namespaced_role_binding(
                    resource.name, resource.namespace
                )
            )
            resource.labels = api_response.metadata.labels
            resource.role_ref = api_response.role_ref
            resource.subjects = api_response.subjects
            ctx.debug(str(api_response))
        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(
        self, ctx: HandlerContext, resource: NamespacedRoleBindingResource
    ) -> None:
        try:
            api_response = resource.api_instance.create_namespaced_role_binding(
                resource.namespace,
                V1RoleBinding(
                    metadata={"name": resource.name, "labels": resource.labels},
                    role_ref=resource.role_ref,
                    subjects=resource.subjects,
                ),
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(
        self, ctx: HandlerContext, resource: NamespacedRoleBindingResource
    ) -> None:
        try:
            api_response = resource.api_instance.delete_namespaced_role_binding(
                resource.name, resource.namespace
            )
            ctx.debug(str(api_response))
            while True:
                api_response = resource.api_instance.read_namespaced_role_binding(
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
        self,
        ctx: HandlerContext,
        changes: dict,
        resource: NamespacedRoleBindingResource,
    ) -> None:
        try:
            current: V1ClusterRoleBinding = (
                resource.api_instance.read_namespaced_role_binding(
                    resource.name, resource.namespace
                )
            )
            current.metadata.labels = resource.labels
            current.role_ref = resource.role_ref
            current.subjects = resource.subjects
            api_response = resource.api_instance.patch_namespaced_role_binding(
                resource.name, resource.namespace, current
            )
            ctx.debug(str(api_response))
        except ApiException as e:
            ctx.error(str(e))
            raise e
