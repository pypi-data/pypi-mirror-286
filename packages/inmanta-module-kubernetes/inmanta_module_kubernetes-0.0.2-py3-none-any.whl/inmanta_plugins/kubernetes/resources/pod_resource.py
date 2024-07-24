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

from kubernetes.client import CoreV1Api, V1ContainerStatus, V1Pod, V1Status
from kubernetes.client.rest import ApiException

from inmanta.agent.handler import CRUDHandler, HandlerContext, ResourcePurged, provider
from inmanta.resources import resource
from inmanta_plugins.kubernetes.resources.cluster_resource import ClusterResource
from inmanta_plugins.kubernetes.resources.namespaced_resource import NamespacedResource


@resource(
    "kubernetes::resources::Pod",
    agent="cluster.name",
    id_attribute="identifier",
)
class PodResource(NamespacedResource):
    fields = ("spec", "status")

    @staticmethod
    def get_data(exporter, entity):
        return entity.spec

    @staticmethod
    def get_status(exporter, entity):
        return "Running"

    @staticmethod
    def get_identifier(exporter, entity):
        return (
            NamespacedResource.get_identifier(exporter, entity)
            + f"/pod/{ClusterResource.get_name(exporter, entity)}"
        )

    def _build_api_instance(self) -> CoreV1Api:
        return CoreV1Api(self._build_api_client())

    @property
    def api_instance(self) -> CoreV1Api:
        if self._api_instance is None:
            self._api_instance = self._build_api_instance()

        return self._api_instance


@provider("kubernetes::resources::Pod", name="pod-resource")
class PodResourceProvider(CRUDHandler):
    def _find_state(self, pod: V1Pod) -> str:
        container_statuses: list[V1ContainerStatus] = (
            pod.status.container_statuses or []
        )
        for container_status in container_statuses:
            if container_status.state is None:
                continue

            if (
                container_status.state.waiting is not None
                and container_status.state.waiting.reason == "ImagePullBackOff"
            ):
                return container_status.state.waiting.reason

            if (
                container_status.state.terminated is not None
                and container_status.state.terminated.exit_code != 0
            ):
                return container_status.state.terminated.reason

        # Nothing wrong was detected so far
        return "Running"

    def read_resource(self, ctx: HandlerContext, resource: PodResource) -> None:
        try:
            api_response: V1Pod = resource.api_instance.read_namespaced_pod(
                resource.name, resource.namespace
            )
            resource.labels = api_response.metadata.labels
            resource.spec = api_response.spec

            phase = api_response.status.phase
            state = self._find_state(api_response)

            resource.status = state if state != "Running" else phase

            ctx.debug(str(api_response.status))

        except ApiException as e:
            if e.status == 404:
                raise ResourcePurged()
            else:
                ctx.error(str(e))
                raise e

    def create_resource(self, ctx: HandlerContext, resource: PodResource) -> None:
        try:
            api_response: V1Pod = resource.api_instance.create_namespaced_pod(
                resource.namespace,
                V1Pod(
                    metadata={
                        "name": resource.name,
                        "namespace": resource.namespace,
                        "labels": resource.labels,
                    },
                    spec=resource.spec,
                ),
            )
            ctx.debug(str(api_response.status))

            phase = "Pending"
            state = "Running"
            while phase == "Pending" and state == "Running":
                api_response: V1Pod = resource.api_instance.read_namespaced_pod(
                    resource.name, resource.namespace
                )
                phase = api_response.status.phase
                state = self._find_state(api_response)

                time.sleep(0.5)

            if state != "Running":
                raise Exception(
                    f"Pod is not in the expected state: got {state} (expected Running)"
                )

            if phase != "Running":
                raise Exception(
                    f"Pod is not in the expected phase: got {phase} (expected Running)"
                )

        except ApiException as e:
            ctx.error(str(e))
            raise e

    def delete_resource(self, ctx: HandlerContext, resource: PodResource) -> None:
        try:
            api_response: V1Status = resource.api_instance.delete_namespaced_pod(
                resource.name, resource.namespace
            )
            ctx.debug(str(api_response))

            phase = "Pending"
            while phase != "":
                api_response = resource.api_instance.read_namespaced_pod(
                    resource.name, resource.namespace
                )
                phase = api_response.status.phase

                time.sleep(0.5)

        except ApiException as e:
            if e.status != 404:
                ctx.error(str(e))
                raise e

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: PodResource
    ) -> None:
        try:
            current: V1Pod = resource.api_instance.read_namespaced_pod(
                resource.name, resource.namespace
            )
            current.metadata.labels = resource.labels
            current.spec = resource.spec

            api_response = resource.api_instance.patch_namespaced_pod(
                resource.name, resource.namespace, current
            )
            ctx.debug(str(api_response.status))

            phase = "Pending"
            state = "Running"
            while phase == "Pending" and state == "Running":
                api_response: V1Pod = resource.api_instance.read_namespaced_pod(
                    resource.name, resource.namespace
                )
                phase = api_response.status.phase
                state = self._find_state(api_response)

                time.sleep(0.5)

            if state != "Running":
                raise Exception(
                    f"Pod is not in the expected state: got {state} (expected Running)"
                )

            if phase != "Running":
                raise Exception(
                    f"Pod is not in the expected phase: got {phase} (expected Running)"
                )

        except ApiException as e:
            ctx.error(str(e))
            raise e
