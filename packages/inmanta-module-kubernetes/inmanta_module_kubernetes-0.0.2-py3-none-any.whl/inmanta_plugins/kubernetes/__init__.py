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

from inmanta.plugins import PluginException, plugin


@plugin
def assert_common_cluster(
    first: "kubernetes::resources::ClusterResource",
    second: "kubernetes::resources::ClusterResource",
) -> None:
    if first.cluster != second.cluster:
        raise PluginException(
            f"Those two entities are not member of the same cluster but should: {first} and {second}"
        )
