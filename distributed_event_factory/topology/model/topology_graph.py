from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from distributed_event_factory.topology.model.topology_spec import TopologySpec


@dataclass(frozen=True)
class TopologyNode:
    name: str
    level: int


class TopologyGraph:
    def __init__(
        self,
        nodes: Dict[str, TopologyNode],
        edges: Dict[str, Set[str]],
        transition_counts: Dict[Tuple[str, str], int] = None,
        payload_deltas: Dict[Tuple[str, str, int], int] = None,
        transition_probabilities: Dict[Tuple[str, str, int], float] = None,
    ):
        self.nodes = nodes
        self.edges = edges
        self.transition_counts = transition_counts or {}
        self.payload_deltas = payload_deltas or {}
        self.transition_probabilities = transition_probabilities or {}
        self.validate_invariants()

    @staticmethod
    def create_initial(spec: TopologySpec) -> "TopologyGraph":
        nodes: Dict[str, TopologyNode] = {"<start>": TopologyNode("<start>", 0)}
        layer_count = max(1, spec.trace_length.target)
        layers: List[List[str]] = []
        for level in range(1, layer_count + 1):
            name = f"Node-{level}"
            nodes[name] = TopologyNode(name=name, level=level)
            layers.append([name])

        end_level = layer_count + 1
        nodes["<end>"] = TopologyNode("<end>", end_level)

        edges: Dict[str, Set[str]] = {name: set() for name in nodes}
        transition_counts: Dict[Tuple[str, str], int] = {}
        if not layers:
            edges["<start>"].add("<end>")
        else:
            edges["<start>"].update(layers[0])
            transition_counts[("<start>", layers[0][0])] = 1
            for current_layer, next_layer in zip(layers, layers[1:]):
                src, dst = current_layer[0], next_layer[0]
                edges[src].add(dst)
                transition_counts[(src, dst)] = max(1, spec.initial_branching)
            for src in layers[-1]:
                edges[src].add("<end>")
                transition_counts[(src, "<end>")] = max(1, spec.initial_branching)

        return TopologyGraph(nodes=nodes, edges=edges, transition_counts=transition_counts)

    def copy(self) -> "TopologyGraph":
        return TopologyGraph(
            nodes={name: TopologyNode(node.name, node.level) for name, node in self.nodes.items()},
            edges={src: set(dsts) for src, dsts in self.edges.items()},
            transition_counts=dict(self.transition_counts),
            payload_deltas=dict(self.payload_deltas),
            transition_probabilities=dict(self.transition_probabilities),
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

    def transition_count(self, src: str, dst: str) -> int:
        return self.transition_counts.get((src, dst), 1)

    def set_transition_count(self, src: str, dst: str, count: int) -> None:
        if count < 1:
            raise ValueError("Transition count must be positive")
        if dst not in self.edges.get(src, set()):
            raise ValueError(f"Transition does not exist: {src}->{dst}")
        self.transition_counts[(src, dst)] = count
        self.transition_probabilities = {
            key: value for key, value in self.transition_probabilities.items()
            if key[:2] != (src, dst) or key[2] <= count
        }

    def transition_probability(self, src: str, dst: str, transition_index: int) -> float:
        total_count = sum(self.transition_count(src, successor) for successor in self.successors(src))
        if total_count == 0:
            return 0.0
        return self.transition_probabilities.get((src, dst, transition_index), 1.0 / total_count)

    def set_transition_probability(self, src: str, dst: str, transition_index: int, probability: float) -> None:
        if not 0.0 <= probability <= 1.0:
            raise ValueError("Transition probability must be between 0 and 1")
        if transition_index < 1 or transition_index > self.transition_count(src, dst):
            raise ValueError(f"Invalid transition index for {src}->{dst}: {transition_index}")
        self.transition_probabilities[(src, dst, transition_index)] = probability

    def payload_delta(self, src: str, dst: str, transition_index: int) -> int:
        return self.payload_deltas.get((src, dst, transition_index), 0)

    def set_payload_delta(self, src: str, dst: str, transition_index: int, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
            raise ValueError("Payload delta must be an integer between 0 and 100")
        if transition_index < 1 or transition_index > self.transition_count(src, dst):
            raise ValueError(f"Invalid transition index for {src}->{dst}: {transition_index}")
        self.payload_deltas[(src, dst, transition_index)] = value

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
        self.transition_counts = {
            edge: count for edge, count in self.transition_counts.items()
            if node_name not in edge
        }
        self.payload_deltas = {
            transition: value for transition, value in self.payload_deltas.items()
            if node_name not in transition[:2]
        }
        self.transition_probabilities = {
            transition: value for transition, value in self.transition_probabilities.items()
            if node_name not in transition[:2]
        }

        if validate:
            self.validate_invariants()

    def add_edge(self, src: str, dst: str, validate: bool = True) -> None:
        if src not in self.nodes or dst not in self.nodes:
            raise ValueError("Source and destination must exist")
        self.edges.setdefault(src, set()).add(dst)
        self.transition_counts.setdefault((src, dst), 1)
        if validate:
            self.validate_invariants()

    def remove_edge(self, src: str, dst: str, validate: bool = True) -> None:
        self.edges.setdefault(src, set()).discard(dst)
        self.transition_counts.pop((src, dst), None)
        if validate:
            self.validate_invariants()

    def validate_invariants(self) -> None:
        if "<start>" not in self.nodes or "<end>" not in self.nodes:
            raise ValueError("Topology graph must contain <start> and <end>")

        for src in self.nodes:
            self.edges.setdefault(src, set())

        for (src, dst, transition_index), probability in self.transition_probabilities.items():
            if dst not in self.edges.get(src, set()):
                raise ValueError(f"Probability assigned to missing transition: {src}->{dst}")
            if not 1 <= transition_index <= self.transition_count(src, dst):
                raise ValueError(f"Invalid transition index for {src}->{dst}: {transition_index}")
            if not 0.0 <= probability <= 1.0:
                raise ValueError("Transition probability must be between 0 and 1")

        for src in self.nodes:
            probabilities = [
                self.transition_probability(src, dst, index)
                for dst in self.successors(src)
                for index in range(1, self.transition_count(src, dst) + 1)
            ]
            if probabilities and abs(sum(probabilities) - 1.0) > 1e-9:
                raise ValueError(f"Transition probabilities from {src} must sum to 1")

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
