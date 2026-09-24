from typing import Dict

from distributed_event_factory.core.datasource import GenericDataSource
from distributed_event_factory.topology.model.topology_graph import TopologyGraph


class TopologyDatasourceGenerator:
    def build_datasource_configs(self, graph: TopologyGraph) -> Dict[str, dict]:
        configs: Dict[str, dict] = {}
        for node_name in graph.node_names():
            if node_name == "<end>":
                continue

            successors = sorted(graph.successors(node_name), key=lambda name: graph.nodes[name].level)
            if len(successors) == 0:
                continue

            probability = 1.0 / len(successors)
            event_data = []
            for idx, successor in enumerate(successors):
                event_data.append({
                    "activity": f"{node_name}->{successor}-{idx + 1}",
                    "transition": successor,
                    "duration": 1,
                    "payloadUpdate": {
                        "type": "fixed",
                        "value": 0
                    }
                })

            configs[node_name] = {
                "name": node_name,
                "group": "topology",
                "selection": "genericProbability",
                "distribution": [probability for _ in successors],
                "eventData": event_data
            }

        return configs

    def build_datasource_objects(self, graph: TopologyGraph, datasource_parser) -> Dict[str, GenericDataSource]:
        datasource_objects = {}
        datasource_configs = self.build_datasource_configs(graph)
        for key, config in datasource_configs.items():
            datasource_objects[key] = datasource_parser.parse(config)
        return datasource_objects
