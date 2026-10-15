from typing import Dict

from distributed_event_factory.core.datasource import GenericDataSource
from distributed_event_factory.topology.model.topology_graph import TopologyGraph


class TopologyDatasourceGenerator:
    def build_activity_names(self, graph: TopologyGraph) -> Dict[tuple, str]:
        counts_by_level = {}
        activity_names = {}

        for node_name in sorted(
            graph.node_names(),
            key=lambda name: (graph.nodes[name].level, name)
        ):
            if node_name in {"<start>", "<end>"}:
                continue

            level = graph.nodes[node_name].level
            for successor in sorted(
                graph.successors(node_name),
                key=lambda name: (graph.nodes[name].level, name)
            ):
                for transition_index in range(1, graph.transition_count(node_name, successor) + 1):
                    counts_by_level[level] = counts_by_level.get(level, 0) + 1
                    activity_names[(node_name, successor, transition_index)] = (
                        f"{self._layer_label(level)}{counts_by_level[level]}"
                    )

        return activity_names

    def build_end_activity_names(self, graph: TopologyGraph) -> set:
        return {
            activity_name
            for (_, target, _), activity_name in self.build_activity_names(graph).items()
            if target == "<end>"
        }

    def build_datasource_configs(self, graph: TopologyGraph) -> Dict[str, dict]:
        configs: Dict[str, dict] = {}
        activity_names = self.build_activity_names(graph)
        for node_name in graph.node_names():
            if node_name == "<end>":
                continue

            successors = sorted(
                graph.successors(node_name),
                key=lambda name: (graph.nodes[name].level, name)
            )
            if len(successors) == 0:
                continue

            event_data = []
            distribution = []
            for successor in successors:
                for transition_index in range(1, graph.transition_count(node_name, successor) + 1):
                    distribution.append(graph.transition_probability(node_name, successor, transition_index))
                    event_data.append({
                        "activity": activity_names.get(
                            (node_name, successor, transition_index),
                            f"{node_name}->{successor}-{transition_index}"
                        ),
                        "transition": successor,
                        "duration": 1,
                        "payloadUpdate": {
                            "type": "fixed",
                            "value": graph.payload_delta(node_name, successor, transition_index)
                        }
                    })

            configs[node_name] = {
                "name": node_name,
                "group": "topology",
                "selection": "genericProbability",
                "distribution": distribution,
                "eventData": event_data
            }

        return configs

    @staticmethod
    def _layer_label(level: int) -> str:
        label = ""
        while level:
            level, remainder = divmod(level - 1, 26)
            label = chr(ord("A") + remainder) + label
        return label

    def build_datasource_objects(self, graph: TopologyGraph, datasource_parser) -> Dict[str, GenericDataSource]:
        datasource_objects = {}
        datasource_configs = self.build_datasource_configs(graph)
        for key, config in datasource_configs.items():
            datasource_objects[key] = datasource_parser.parse(config)
        return datasource_objects
