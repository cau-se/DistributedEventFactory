from dataclasses import dataclass
from typing import List

from distributed_event_factory.topology.model.topology_graph import TopologyGraph


@dataclass(frozen=True)
class TopologyAction:
    name: str
    payload: dict


class TopologyActionGenerator:
    def generate_candidates(self, graph: TopologyGraph, change_amount: int = 1) -> List[TopologyAction]:
        actions: List[TopologyAction] = []
        for src, dst in graph.edge_list():
            if src == "<start>":
                continue
            actions.append(TopologyAction("increase_transition", {
                "src": src,
                "dst": dst,
                "amount": change_amount,
            }))
            if graph.transition_count(src, dst) > 1:
                decrease_amount = min(change_amount, graph.transition_count(src, dst) - 1)
                actions.append(TopologyAction("decrease_transition", {
                    "src": src,
                    "dst": dst,
                    "amount": decrease_amount,
                }))

        return actions

    def apply(self, graph: TopologyGraph, action: TopologyAction) -> TopologyGraph:
        candidate = graph.copy()

        if action.name in {"increase_transition", "decrease_transition"}:
            src = action.payload["src"]
            dst = action.payload["dst"]
            current_count = candidate.transition_count(src, dst)
            amount = action.payload.get("amount", 1)
            change = amount if action.name == "increase_transition" else -amount
            candidate.set_transition_count(src, dst, max(1, current_count + change))
            return candidate

        raise ValueError(f"Unsupported topology action: {action.name}")
