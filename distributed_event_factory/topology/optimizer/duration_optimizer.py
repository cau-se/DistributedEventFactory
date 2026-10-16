"""Optimizes total trace duration and its distribution across process steps."""

from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Tuple

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologySpec
from distributed_event_factory.topology.probability_analysis import (
    expected_duration_contributions,
    expected_trace_duration,
    normalized_duration_entropy,
)


@dataclass(frozen=True)
class DurationOptimizationResult:
    graph: TopologyGraph
    iterations: int
    average_trace_duration: float
    normalized_entropy: float
    duration_target_reached: bool
    entropy_target_reached: bool
    optimization_log: List[dict]
    expected_contributions: Dict[Tuple[str, str, int], float]

    @property
    def target_reached(self) -> bool:
        return self.duration_target_reached and self.entropy_target_reached


class DurationOptimizer:
    beam_width = 5
    max_iterations = 200

    def optimize(self, graph: TopologyGraph, spec: TopologySpec) -> DurationOptimizationResult:
        optimized_graph = graph.copy()
        transition_keys = [
            (src, dst, index)
            for src, dst in optimized_graph.edge_list()
            if src != "<start>"
            for index in range(1, optimized_graph.transition_count(src, dst) + 1)
        ]
        initial_duration = max(
            1,
            min(
                spec.max_duration_per_transition,
                round(spec.average_trace_duration.target / max(1, spec.trace_length.target)),
            ),
        )
        initial_duration = int(initial_duration)
        for key in transition_keys:
            optimized_graph.set_duration(*key, initial_duration)

        initial_state = tuple(optimized_graph.duration(*key) for key in transition_keys)
        beam = [initial_state]
        seen = {initial_state}
        best_state = initial_state
        best_rank = self._rank(initial_state, optimized_graph, transition_keys, spec, initial_duration)
        log = [{
            "type": "initial",
            "averageTraceDuration": expected_trace_duration(optimized_graph),
            "normalizedEntropy": normalized_duration_entropy(optimized_graph),
            "initialDuration": initial_duration,
        }]
        iteration = 0

        for iteration in range(1, self.max_iterations + 1):
            candidates = {}
            for state in beam:
                state_graph = self._graph_with_durations(optimized_graph, state, transition_keys)
                duration_gap = spec.average_trace_duration.target - expected_trace_duration(state_graph)
                entropy_gap = spec.duration_entropy.target - normalized_duration_entropy(state_graph)
                step = min(
                    10,
                    max(1, ceil(abs(duration_gap) / max(1, spec.trace_length.target))),
                )

                for index, value in enumerate(state):
                    for change in (-step, step):
                        changed = value + change
                        if 1 <= changed <= spec.max_duration_per_transition:
                            self._add_candidate(candidates, seen, state, (index,), {index: changed})

                contributions = expected_duration_contributions(state_graph)
                per_step = {}
                for index, key in enumerate(transition_keys):
                    per_step.setdefault(key[0], []).append((index, contributions.get(key, 0.0)))
                positive_steps = [
                    (node, sum(value for _, value in values), values)
                    for node, values in per_step.items()
                    if sum(value for _, value in values) > 0
                ]
                if len(positive_steps) > 1 and entropy_gap != 0:
                    low_step = min(positive_steps, key=lambda item: item[1])
                    high_step = max(positive_steps, key=lambda item: item[1])
                    donor, receiver = (high_step, low_step) if entropy_gap > 0 else (low_step, high_step)
                    donor_index = max(donor[2], key=lambda item: item[1])[0]
                    receiver_index = min(receiver[2], key=lambda item: item[1])[0]
                    if donor_index != receiver_index:
                        changed = {donor_index: state[donor_index] - 1, receiver_index: state[receiver_index] + 1}
                        if all(1 <= value <= spec.max_duration_per_transition for value in changed.values()):
                            self._add_candidate(
                                candidates,
                                seen,
                                state,
                                (donor_index, receiver_index),
                                changed,
                            )

            if not candidates:
                iteration -= 1
                break

            ranks = {
                state: self._rank(state, optimized_graph, transition_keys, spec, initial_duration)
                for state in candidates
            }
            ranked = sorted(candidates, key=lambda state: ranks[state])
            for state in ranked:
                if ranks[state] < best_rank:
                    best_state, best_rank = state, ranks[state]
                seen.add(state)
            beam = ranked[:self.beam_width]
            best = ranked[0]
            best_graph = self._graph_with_durations(optimized_graph, best, transition_keys)
            contribution = expected_trace_duration(best_graph)
            entropy = normalized_duration_entropy(best_graph)
            log.append({
                "type": "iteration",
                "iteration": iteration,
                "averageTraceDuration": contribution,
                "normalizedEntropy": entropy,
                "durationPenalty": ranks[best][0],
                "entropyPenalty": ranks[best][1],
                "evaluatedCandidates": len(ranked),
                "retainedCandidates": len(beam),
            })
            print(
                f"[topology][duration] Iteration {iteration}: "
                f"average={contribution:.2f} min, entropy={entropy:.4f}, "
                f"evaluated={len(ranked)}, retained={len(beam)}"
            )
            if ranks[best][0] == 0 and ranks[best][1] == 0:
                break

        final_graph = self._graph_with_durations(optimized_graph, best_state, transition_keys)
        average = expected_trace_duration(final_graph)
        entropy = normalized_duration_entropy(final_graph)
        duration_reached = self._duration_penalty(average, spec) == 0
        entropy_reached = self._entropy_penalty(entropy, spec) == 0
        log.append({
            "type": "final",
            "iterations": iteration,
            "averageTraceDuration": average,
            "normalizedEntropy": entropy,
            "durationTargetReached": duration_reached,
            "entropyTargetReached": entropy_reached,
        })
        print(
            f"[topology][duration] Finished: average={average:.2f} min, "
            f"entropy={entropy:.4f}, targetReached={duration_reached and entropy_reached}"
        )
        return DurationOptimizationResult(
            graph=final_graph,
            iterations=iteration,
            average_trace_duration=average,
            normalized_entropy=entropy,
            duration_target_reached=duration_reached,
            entropy_target_reached=entropy_reached,
            optimization_log=log,
            expected_contributions=expected_duration_contributions(final_graph),
        )

    @staticmethod
    def _add_candidate(candidates, seen, parent, changed_indices, updates):
        state = list(parent)
        for index, value in updates.items():
            state[index] = value
        candidate = tuple(state)
        if candidate not in seen:
            candidates.setdefault(candidate, (parent, changed_indices))

    @staticmethod
    def _graph_with_durations(graph, state, transition_keys):
        candidate = graph.copy()
        for key, value in zip(transition_keys, state):
            candidate.set_duration(*key, value)
        return candidate

    @classmethod
    def _rank(cls, state, graph, transition_keys, spec, initial_duration):
        candidate = cls._graph_with_durations(graph, state, transition_keys)
        duration_penalty = cls._duration_penalty(expected_trace_duration(candidate), spec)
        entropy_penalty = cls._entropy_penalty(normalized_duration_entropy(candidate), spec)
        change_cost = sum(abs(value - initial_duration) for value in state)
        return duration_penalty, entropy_penalty, change_cost, state

    @staticmethod
    def _duration_penalty(observed, spec):
        target = spec.average_trace_duration
        return max(0.0, abs(observed - target.target) - target.tolerance)

    @staticmethod
    def _entropy_penalty(observed, spec):
        target = spec.duration_entropy
        return max(0.0, abs(observed - target.target) - target.tolerance)
