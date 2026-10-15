from dataclasses import dataclass
from typing import List

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologySpec
from distributed_event_factory.topology.probability_analysis import (
    most_likely_trace_probability,
    normalized_trace_entropy,
)


@dataclass(frozen=True)
class EntropyOptimizationResult:
    graph: TopologyGraph
    normalized_entropy: float
    most_likely_trace_probability: float
    concentration: float
    target_reached: bool
    optimization_log: List[dict]


class TraceEntropyOptimizer:
    max_iterations = 30

    def optimize(self, graph: TopologyGraph, spec: TopologySpec) -> EntropyOptimizationResult:
        optimized_graph = graph.copy()
        groups = [
            (src, dst, optimized_graph.transition_count(src, dst))
            for src, dst in optimized_graph.edge_list()
        ]
        target = spec.trace_entropy.target
        tolerance = spec.trace_entropy.tolerance
        log_entries = []

        low, high = 0.0, 1.0
        concentration = 1.0
        for iteration in range(1, self.max_iterations + 1):
            if target >= 1.0:
                concentration = 1.0
            elif target <= 0.0:
                concentration = 0.0
            else:
                concentration = (low + high) / 2.0
            self._set_probabilities(optimized_graph, groups, concentration)
            entropy = normalized_trace_entropy(optimized_graph)
            log_entries.append({
                "type": "candidate",
                "iteration": iteration,
                "concentration": concentration,
                "normalizedEntropy": entropy,
                "target": target,
                "withinTolerance": abs(entropy - target) <= tolerance,
            })
            print(
                f"[topology][entropy] Iteration {iteration}: "
                f"concentration={concentration:.6f}, normalizedEntropy={entropy:.4f}, "
                f"target={target:.4f}±{tolerance:.4f}"
            )
            if abs(entropy - target) <= tolerance:
                break
            if target >= 1.0 or entropy < target:
                low = concentration
            elif target <= 0.0 or entropy > target:
                high = concentration

        normalized_entropy = normalized_trace_entropy(optimized_graph)
        most_likely_probability = most_likely_trace_probability(optimized_graph)
        target_reached = abs(normalized_entropy - target) <= tolerance
        log_entries.append({
            "type": "final",
            "iterations": len(log_entries),
            "concentration": concentration,
            "normalizedEntropy": normalized_entropy,
            "mostLikelyTraceProbability": most_likely_probability,
            "targetReached": target_reached,
        })
        print(
            f"[topology][entropy] Finished: normalizedEntropy={normalized_entropy:.4f}, "
            f"mostLikelyTrace={most_likely_probability * 100:.2f}%, "
            f"targetReached={target_reached}"
        )
        return EntropyOptimizationResult(
            graph=optimized_graph,
            normalized_entropy=normalized_entropy,
            most_likely_trace_probability=most_likely_probability,
            concentration=concentration,
            target_reached=target_reached,
            optimization_log=log_entries,
        )

    @staticmethod
    def _set_probabilities(graph, groups, concentration):
        groups_by_source = {}
        for src, dst, count in groups:
            groups_by_source.setdefault(src, []).append((dst, count, graph.nodes[dst].level, dst))

        for src, outgoing in groups_by_source.items():
            outgoing.sort(key=lambda edge: (edge[2], edge[3]))
            total_transitions = sum(count for _, count, _, _ in outgoing)
            baseline = 1.0 / total_transitions
            preferred_transition = (outgoing[0][0], 1)
            for dst, count, _, _ in outgoing:
                for index in range(1, count + 1):
                    probability = baseline * concentration
                    if (dst, index) == preferred_transition:
                        probability += 1.0 - concentration
                    graph.set_transition_probability(src, dst, index, probability)
