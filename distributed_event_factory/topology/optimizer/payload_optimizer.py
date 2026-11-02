from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Tuple

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologySpec
from distributed_event_factory.topology.probability_analysis import (
    expected_payload_contributions,
    final_payload_distribution,
    normalized_payload_entropy,
)


@dataclass(frozen=True)
class PayloadOptimizationResult:
    graph: TopologyGraph
    iterations: int
    expected_success_ratio: float
    initial_delta: int
    target_reached: bool
    optimization_log: List[dict]
    normalized_entropy: float
    expected_contributions: Dict[Tuple[str, str, int], float]
    success_ratio_target_reached: bool
    entropy_target_reached: bool


class PayloadOptimizer:
    beam_width = 5
    max_iterations = 300
    max_delta_step = 10

    def optimize(self, graph: TopologyGraph, spec: TopologySpec) -> PayloadOptimizationResult:
        optimized_graph = graph.copy()
        initial_delta = min(
            100,
            ceil((spec.payload_success_threshold + 1) / max(1, spec.trace_length.target)),
        )
        transition_keys = [
            (src, dst, transition_index)
            for src, dst in optimized_graph.edge_list()
            if src != "<start>"
            for transition_index in range(1, optimized_graph.transition_count(src, dst) + 1)
        ]
        for src, dst, transition_index in transition_keys:
            optimized_graph.set_payload_delta(src, dst, transition_index, initial_delta)

        start_state = tuple(optimized_graph.payload_delta(*key) for key in transition_keys)
        beam = [start_state]
        seen = {start_state}
        best_state = start_state
        best_rank = self._rank(start_state, optimized_graph, transition_keys, spec, initial_delta)
        iterations = 0
        optimization_log = [{
            "type": "initial",
            "expectedSuccessRatio": self._expected_success_ratio(optimized_graph, spec.payload_success_threshold) * 100,
            "scoreDistance": best_rank[0],
            "normalizedEntropy": self._normalized_payload_entropy(optimized_graph),
            "successRatioTargetReached": best_rank[0] == 0,
            "entropyTargetReached": best_rank[1] == 0,
            "initialDelta": initial_delta,
        }]
        print(
            f"[topology][payload] Initial: "
            f"success={optimization_log[0]['expectedSuccessRatio']:.2f}%, "
            f"entropy={optimization_log[0]['normalizedEntropy']:.4f}, "
            f"successTargetReached={optimization_log[0]['successRatioTargetReached']}, "
            f"entropyTargetReached={optimization_log[0]['entropyTargetReached']}"
        )

        for iterations in range(1, self.max_iterations + 1):
            candidates = {}
            for state in beam:
                state_graph = self._graph_with_deltas(graph, state, transition_keys)
                state_ratio = self._expected_success_ratio(
                    state_graph,
                    spec.payload_success_threshold,
                )
                step_size = self._step_size(state_ratio, spec)
                for index, value in enumerate(state):
                    for change in (-step_size, step_size):
                        changed_value = value + change
                        if not 0 <= changed_value <= 100:
                            continue
                        candidate = state[:index] + (changed_value,) + state[index + 1:]
                        if candidate not in seen:
                            candidates.setdefault(candidate, (state, (index,)))

                entropy_gap = spec.payload_entropy.target - self._normalized_payload_entropy(state_graph)
                contributions = expected_payload_contributions(state_graph)
                contribution_by_index = [
                    contributions.get(key, 0.0)
                    for key in transition_keys
                ]
                positive_indices = [
                    index for index, contribution in enumerate(contribution_by_index)
                    if contribution > 0
                ]
                if len(positive_indices) > 1 and entropy_gap != 0:
                    low_index = min(positive_indices, key=lambda index: contribution_by_index[index])
                    high_index = max(positive_indices, key=lambda index: contribution_by_index[index])
                    entropy_step = min(
                        self.max_delta_step,
                        max(1, ceil(
                            abs(entropy_gap)
                            * (spec.payload_success_threshold + 1)
                            / max(1, spec.trace_length.target)
                        )),
                    )
                    if entropy_gap < 0:
                        changes = ((high_index, entropy_step), (low_index, -entropy_step))
                    else:
                        changes = ((high_index, -entropy_step), (low_index, entropy_step))
                    changed_state = list(state)
                    for index, change in changes:
                        changed_state[index] += change
                    if all(0 <= value <= 100 for value in changed_state):
                        candidate = tuple(changed_state)
                        if candidate not in seen:
                            candidates.setdefault(candidate, (state, tuple(index for index, _ in changes)))

            if not candidates:
                iterations -= 1
                break

            ranks = {
                state: self._rank(state, graph, transition_keys, spec, initial_delta)
                for state in candidates
            }
            ranked_candidates = sorted(candidates, key=lambda state: ranks[state])
            for state in ranked_candidates:
                rank = ranks[state]
                if rank < best_rank:
                    best_state = state
                    best_rank = rank
                seen.add(state)
            beam = self._select_beam(ranked_candidates, ranks)
            feasible_candidates = [
                state for state in ranked_candidates
                if ranks[state][0] == 0
            ]
            iteration_best = min(
                feasible_candidates or ranked_candidates,
                key=lambda state: ranks[state],
            )
            iteration_rank = ranks[iteration_best]
            iteration_graph = self._graph_with_deltas(graph, iteration_best, transition_keys)
            iteration_success_ratio = self._expected_success_ratio(
                iteration_graph,
                spec.payload_success_threshold,
            ) * 100
            parent_state, changed_indices = candidates[iteration_best]
            changes = []
            for changed_index in changed_indices:
                src, dst, transition_index = transition_keys[changed_index]
                changes.append(
                    f"{src}->{dst}#{transition_index}:"
                    f"{parent_state[changed_index]}->{iteration_best[changed_index]}"
                )
            transition = ";".join(changes)
            step_size = max(
                abs(iteration_best[index] - parent_state[index])
                for index in changed_indices
            )
            print(
                f"[topology][payload] Iteration {iterations}: "
                f"best={transition}, "
                f"step={step_size}, "
                f"success={iteration_success_ratio:.2f}%, "
                f"entropy={self._normalized_payload_entropy(iteration_graph):.4f}, "
                f"scoreDistance={iteration_rank[0]:.2f}/{iteration_rank[1]:.4f}, "
                f"evaluated={len(ranked_candidates)}, retained={len(beam)}"
            )
            optimization_log.append({
                "type": "iteration",
                "iteration": iterations,
                "bestTransition": transition,
                "bestDeltaChange": transition,
                "stepSize": step_size,
                "bestExpectedSuccessRatio": iteration_success_ratio,
                "bestNormalizedEntropy": self._normalized_payload_entropy(iteration_graph),
                "bestScoreDistance": iteration_rank[0],
                "paretoCandidates": len(beam),
                "evaluatedCandidates": len(ranked_candidates),
                "retainedCandidates": len(beam),
            })
            if best_rank[0] == 0 and best_rank[1] == 0:
                break

        for key, value in zip(transition_keys, best_state):
            optimized_graph.set_payload_delta(*key, value)

        expected_success_ratio = self._expected_success_ratio(
            optimized_graph,
            spec.payload_success_threshold,
        )

        success_ratio_target_reached = self._ratio_penalty(
            expected_success_ratio,
            spec.successful_case_ratio.target,
            spec.successful_case_ratio.tolerance,
        ) == 0
        normalized_entropy = self._normalized_payload_entropy(optimized_graph)
        entropy_target_reached = self._entropy_penalty(
            normalized_entropy,
            spec.payload_entropy.target,
            spec.payload_entropy.tolerance,
        ) == 0
        target_reached = success_ratio_target_reached and entropy_target_reached
        expected_contributions = expected_payload_contributions(optimized_graph)
        optimization_log.append({
            "type": "final",
            "iterations": iterations,
            "expectedSuccessRatio": expected_success_ratio * 100,
            "targetReached": target_reached,
            "normalizedEntropy": normalized_entropy,
            "successRatioTargetReached": success_ratio_target_reached,
            "entropyTargetReached": entropy_target_reached,
            "deltaRange": (
                min(best_state) if best_state else 0,
                max(best_state) if best_state else 0,
            ),
        })
        print(
            f"[topology][payload] Finished: iterations={iterations}, "
            f"expectedSuccess={expected_success_ratio * 100:.2f}%, "
            f"normalizedEntropy={normalized_entropy:.4f}, "
            f"targetReached={target_reached}"
        )

        return PayloadOptimizationResult(
            graph=optimized_graph,
            iterations=iterations,
            expected_success_ratio=expected_success_ratio,
            initial_delta=initial_delta,
            target_reached=target_reached,
            optimization_log=optimization_log,
            normalized_entropy=normalized_entropy,
            expected_contributions=expected_contributions,
            success_ratio_target_reached=success_ratio_target_reached,
            entropy_target_reached=entropy_target_reached,
        )

    @staticmethod
    def _graph_with_deltas(graph, state, transition_keys):
        candidate_graph = graph.copy()
        for key, value in zip(transition_keys, state):
            candidate_graph.set_payload_delta(*key, value)
        return candidate_graph

    @classmethod
    def _step_size(cls, success_ratio, spec):
        distance_from_target = abs(success_ratio * 100 - spec.successful_case_ratio.target)
        target_payload = spec.payload_success_threshold + 1
        estimated_payload_adjustment = (
            distance_from_target / 100
            * target_payload
            / max(1, spec.trace_length.target)
        )
        return min(cls.max_delta_step, max(1, ceil(estimated_payload_adjustment)))

    @classmethod
    def _rank(cls, state, graph, transition_keys, spec, initial_delta):
        candidate_graph = cls._graph_with_deltas(graph, state, transition_keys)
        ratio = cls._expected_success_ratio(candidate_graph, spec.payload_success_threshold)
        penalty = cls._ratio_penalty(ratio, spec.successful_case_ratio.target, spec.successful_case_ratio.tolerance)
        ratio_distance = abs(ratio * 100 - spec.successful_case_ratio.target)
        entropy = cls._normalized_payload_entropy(candidate_graph)
        entropy_penalty = cls._entropy_penalty(
            entropy,
            spec.payload_entropy.target,
            spec.payload_entropy.tolerance,
        )
        changes = sum(abs(value - initial_delta) for value in state)
        return penalty, entropy_penalty, ratio_distance, changes, state

    @classmethod
    def _select_beam(cls, candidates, ranks):
        retained = []

        def add(state):
            if state not in retained and len(retained) < cls.beam_width:
                retained.append(state)

        ordered = sorted(candidates, key=lambda state: ranks[state])
        for state in ordered[:2]:
            add(state)
        for state in sorted(candidates, key=lambda item: (ranks[item][1], ranks[item][0], ranks[item][2], ranks[item][3]))[:2]:
            add(state)

        pareto = []
        for state in sorted(candidates, key=lambda item: (ranks[item][0], ranks[item][1], ranks[item][2])):
            ratio_penalty, entropy_penalty = ranks[state][:2]
            if any(
                ranks[other][0] <= ratio_penalty
                and ranks[other][1] <= entropy_penalty
                and ranks[other][:2] != (ratio_penalty, entropy_penalty)
                for other in pareto
            ):
                continue
            pareto = [
                other for other in pareto
                if not (
                    ratio_penalty <= ranks[other][0]
                    and entropy_penalty <= ranks[other][1]
                    and (ratio_penalty, entropy_penalty) != ranks[other][:2]
                )
            ]
            pareto.append(state)

        for state in sorted(pareto, key=lambda item: (ranks[item][0] + ranks[item][1], ranks[item][2], ranks[item][3])):
            add(state)
        for state in ordered:
            add(state)
            if len(retained) == cls.beam_width:
                break
        return retained

    @classmethod
    def _normalized_payload_entropy(cls, graph):
        return normalized_payload_entropy(graph)

    @staticmethod
    def _entropy_penalty(entropy, target, tolerance):
        difference = abs(entropy - target)
        return max(0.0, difference - tolerance)

    @staticmethod
    def _ratio_penalty(ratio: float, target: int, tolerance: int) -> float:
        observed = ratio * 100
        lower = target - tolerance
        upper = target + tolerance
        if observed < lower:
            return lower - observed
        if observed > upper:
            return observed - upper
        return 0.0

    @staticmethod
    def _expected_success_ratio(graph: TopologyGraph, threshold: int) -> float:
        return sum(
            probability for payload, probability in final_payload_distribution(graph).items()
            if payload > threshold
        )
