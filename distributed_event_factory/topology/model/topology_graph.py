from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from distributed_event_factory.topology.model.topology_spec import TopologySpec


@dataclass(frozen=True)
class TopologyNode:
    name: str
    level: int


class TopologyGraph:
    def __init__(self, nodes: Dict[str, TopologyNode], edges: Dict[str, Set[str]]):
        self.nodes = nodes
        self.edges = edges
        self.validate_invariants()

    @staticmethod
    def create_initial(spec: TopologySpec) -> "TopologyGraph":
        datasource_count = max(1, spec.initial_datasource_count)
        branching = max(1, spec.initial_branching)
        nodes: Dict[str, TopologyNode] = {"<start>": TopologyNode("<start>", 0)}
        datasource_names: List[str] = []
        for idx in range(datasource_count):
            name = f"AutoDS{idx + 1}"
            nodes[name] = TopologyNode(name=name, level=idx + 1)
            datasource_names.append(name)
        end_level = datasource_count + 1
        nodes["<end>"] = TopologyNode("<end>", end_level)

        edges: Dict[str, Set[str]] = {name: set() for name in nodes}
        previous = "<start>"
        for name in datasource_names:
            edges[previous].add(name)
            previous = name
        edges[previous].add("<end>")

        for src_idx, src in enumerate(datasource_names):
            for offset in range(1, branching):
                dst_idx = src_idx + offset + 1
                if dst_idx < len(datasource_names):
                    edges[src].add(datasource_names[dst_idx])
                else:
                    edges[src].add("<end>")

        return TopologyGraph(nodes=nodes, edges=edges)

    def copy(self) -> "TopologyGraph":
        return TopologyGraph(
            nodes={name: TopologyNode(node.name, node.level) for name, node in self.nodes.items()},
            edges={src: set(dsts) for src, dsts in self.edges.items()}
        )

    def node_names(self) -> List[str]:
        return sorted(self.nodes.keys(), key=lambda n: self.nodes[n].level)

    def edge_list(self) -> List[Tuple[str, str]]:
        output = []
        for src, destinations in self.edges.items():
            for dst in destinations:
                output.append((src, dst))
        return output

    def successors(self, node: str) -> Set[str]:
        return set(self.edges.get(node, set()))

    def predecessors(self, node: str) -> Set[str]:
        incoming = set()
        for src, destinations in self.edges.items():
            if node in destinations:
                incoming.add(src)
        return incoming

    def add_node(self, node_name: str, level: int, validate: bool = True) -> None:
        if node_name in self.nodes:
            raise ValueError(f"Node already exists: {node_name}")
        if node_name in {"<start>", "<end>"}:
            raise ValueError("Cannot add reserved node names")
        self.nodes[node_name] = TopologyNode(node_name, level)
        self.edges[node_name] = set()
        if validate:
            self.validate_invariants()

    def remove_node(self, node_name: str, validate: bool = True) -> None:
        if node_name in {"<start>", "<end>"}:
            raise ValueError("Cannot remove reserved node names")
        if node_name not in self.nodes:
            return

        del self.nodes[node_name]
        self.edges.pop(node_name, None)
        for src in self.edges:
            self.edges[src].discard(node_name)

        if validate:
            self.validate_invariants()

    def add_edge(self, src: str, dst: str, validate: bool = True) -> None:
        if src not in self.nodes or dst not in self.nodes:
            raise ValueError("Source and destination must exist")
        self.edges.setdefault(src, set()).add(dst)
        if validate:
            self.validate_invariants()

    def remove_edge(self, src: str, dst: str, validate: bool = True) -> None:
        self.edges.setdefault(src, set()).discard(dst)
        if validate:
            self.validate_invariants()

    def validate_invariants(self) -> None:
        if "<start>" not in self.nodes or "<end>" not in self.nodes:
            raise ValueError("Topology graph must contain <start> and <end>")

        for src in self.nodes:
            self.edges.setdefault(src, set())

        for src, destinations in self.edges.items():
            if src not in self.nodes:
                raise ValueError(f"Unknown source node: {src}")
            src_level = self.nodes[src].level
            for dst in destinations:
                if dst not in self.nodes:
                    raise ValueError(f"Unknown destination node: {dst}")
                dst_level = self.nodes[dst].level
                if src_level >= dst_level:
                    raise ValueError(f"Invalid backward or equal edge: {src}->{dst}")

        for name in self.nodes:
            if name == "<end>":
                continue
            if len(self.edges.get(name, set())) == 0:
                raise ValueError(f"Node has no outgoing edge: {name}")

        for name in self.nodes:
            if name == "<start>":
                continue
            if len(self.predecessors(name)) == 0:
                raise ValueError(f"Node has no incoming edge: {name}")
