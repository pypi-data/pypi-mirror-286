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

from kubernetes import config
from kubernetes.client import ApiClient
from kubernetes.client.configuration import Configuration

from inmanta.resources import Id, PurgeableResource


class ClusterResource(PurgeableResource):
    fields = (
        "name",
        "labels",
        "cluster_config",
    )

    def __init__(self, _id: "Id") -> None:
        super().__init__(_id)
        self._api_instance = None

    @staticmethod
    def get_identifier(exporter, entity):
        return f"/cluster/{entity.cluster.name}"

    @staticmethod
    def get_name(exporter, entity):
        return entity.name

    @staticmethod
    def get_labels(exporter, entity):
        return entity.labels

    @staticmethod
    def get_cluster_config(exporter, entity):
        config = {
            "kind": entity.cluster.config.kind,
        }
        if config["kind"] == "kube":
            config["config"] = {
                "config": entity.cluster.config.config,
                "context": entity.cluster.config.context,
            }

        elif config["kind"] == "token":
            config["config"] = {
                "host": entity.cluster.config.host,
                "token": entity.cluster.config.token,
                "verify_ssl": entity.cluster.config.verify_ssl,
                "certificate": entity.cluster.config.certificate,
            }

        return config

    def _build_api_client(self) -> ApiClient:
        if self.cluster_config["kind"] == "kube":
            config_file_path = f"/tmp/kube-config-{time.time()}.yaml"
            with open(config_file_path, "w") as f:
                f.write(self.cluster_config["config"]["config"])
                f.close()

            config.load_kube_config(
                config_file=config_file_path,
                context=self.cluster_config["config"]["context"],
            )
            return ApiClient()

        if self.cluster_config["kind"] == "token":
            configuration = Configuration()
            configuration.host = self.cluster_config["config"]["host"]
            configuration.api_key = {
                "Authorization": "Bearer " + self.cluster_config["config"]["token"]
            }
            configuration.verify_ssl = self.cluster_config["config"]["verify_ssl"]

            if configuration.verify_ssl:
                certificate_file_path = f"/tmp/cluster-ca-{time.time()}.crt"
                with open(certificate_file_path, "w") as f:
                    f.write(self.cluster_config["config"]["certificate"])
                    f.close()

                configuration.ssl_ca_cert = certificate_file_path

            return ApiClient(configuration)

        raise Exception(f"Unknown config kind: {self.cluster_config['kind']}")
