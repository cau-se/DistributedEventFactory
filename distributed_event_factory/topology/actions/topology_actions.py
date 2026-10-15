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
        for src, dst in graph.edge_list():
            if src == "<start>":
                continue
            actions.append(TopologyAction("increase_transition", {
                "src": src,
                "dst": dst,
            }))
            if graph.transition_count(src, dst) > 1:
                actions.append(TopologyAction("decrease_transition", {
                    "src": src,
                    "dst": dst,
                }))

        return actions

    def apply(self, graph: TopologyGraph, action: TopologyAction) -> TopologyGraph:
        candidate = graph.copy()

        if action.name in {"increase_transition", "decrease_transition"}:
            src = action.payload["src"]
            dst = action.payload["dst"]
            current_count = candidate.transition_count(src, dst)
            change = 1 if action.name == "increase_transition" else -1
            candidate.set_transition_count(src, dst, current_count + change)
            return candidate

        raise ValueError(f"Unsupported topology action: {action.name}")
