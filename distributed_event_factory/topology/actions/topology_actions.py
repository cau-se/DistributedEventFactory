from dataclasses import dataclass
from typing import List

from distributed_event_factory.topology.model.topology_graph import TopologyGraph


@dataclass(frozen=True)
class TopologyAction:
    name: str
    payload: dict


class TopologyActionGenerator:
    def generate_candidates(self, graph: TopologyGraph) -> List[TopologyAction]:
        actions: List[TopologyAction] = []
        mutable_nodes = [
            node for node in graph.node_names()
            if node not in {"<start>", "<end>"}
        ]
        mutable_nodes.sort(key=lambda n: graph.nodes[n].level)

        for src in mutable_nodes:
            for dst in mutable_nodes + ["<end>"]:
                if src == dst:
                    continue
                if dst in graph.successors(src):
                    continue
                if graph.nodes[src].level >= graph.nodes[dst].level:
                    continue
                actions.append(TopologyAction("add_transition", {"src": src, "dst": dst}))

        for src, dst in graph.edge_list():
            if src == "<start>" and dst in mutable_nodes[:1]:
                continue
            actions.append(TopologyAction("remove_transition", {"src": src, "dst": dst}))

        for src in ["<start>"] + mutable_nodes:
            if src == "<end>":
                continue
            src_level = graph.nodes[src].level
            level = src_level + 1
            node_name = self._next_node_name(graph)
            actions.append(TopologyAction("add_datasource", {
                "after": src,
                "node_name": node_name,
                "level": level
            }))

        for node in mutable_nodes:
            actions.append(TopologyAction("remove_datasource", {"node_name": node}))

        return actions

    def apply(self, graph: TopologyGraph, action: TopologyAction) -> TopologyGraph:
        candidate = graph.copy()

        if action.name == "add_transition":
            candidate.add_edge(action.payload["src"], action.payload["dst"])
            return candidate

        if action.name == "remove_transition":
            candidate.remove_edge(action.payload["src"], action.payload["dst"])
            return candidate

        if action.name == "add_datasource":
            self._apply_add_datasource(candidate, action)
            return candidate

        if action.name == "remove_datasource":
            self._apply_remove_datasource(candidate, action)
            return candidate

        raise ValueError(f"Unsupported topology action: {action.name}")

    def _apply_add_datasource(self, graph: TopologyGraph, action: TopologyAction) -> None:
        source = action.payload["after"]
        node_name = action.payload["node_name"]
        source_level = graph.nodes[source].level
        level = source_level + 1

        for existing in graph.nodes.values():
            if existing.name in {"<start>", "<end>"}:
                continue
            if existing.level >= level:
                graph.nodes[existing.name] = type(existing)(existing.name, existing.level + 1)
        end_node = graph.nodes["<end>"]
        graph.nodes["<end>"] = type(end_node)(end_node.name, end_node.level + 1)

        graph.add_node(node_name=node_name, level=level, validate=False)

        successors = list(graph.successors(source))
        for successor in successors:
            if successor == "<end>":
                continue
            graph.remove_edge(source, successor, validate=False)
            graph.add_edge(node_name, successor, validate=False)

        graph.add_edge(source, node_name, validate=False)
        if len(graph.successors(node_name)) == 0:
            graph.add_edge(node_name, "<end>", validate=False)

        graph.validate_invariants()

    def _apply_remove_datasource(self, graph: TopologyGraph, action: TopologyAction) -> None:
        node_name = action.payload["node_name"]
        predecessors = list(graph.predecessors(node_name))
        successors = list(graph.successors(node_name))

        graph.remove_node(node_name, validate=False)

        for src in predecessors:
            for dst in successors:
                if graph.nodes[src].level < graph.nodes[dst].level:
                    graph.add_edge(src, dst, validate=False)

        if len(graph.successors("<start>")) == 0:
            ordered_nodes = [n for n in graph.node_names() if n not in {"<start>", "<end>"}]
            if ordered_nodes:
                graph.add_edge("<start>", ordered_nodes[0], validate=False)
            else:
                graph.add_edge("<start>", "<end>", validate=False)

        graph.validate_invariants()

    def _next_node_name(self, graph: TopologyGraph) -> str:
        counter = 1
        while True:
            name = f"Node-{counter}"
            if name not in graph.nodes:
                return name
            counter += 1
