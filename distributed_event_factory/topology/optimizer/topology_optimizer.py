from dataclasses import dataclass
from typing import List, Tuple

from distributed_event_factory.topology.actions.topology_actions import TopologyActionGenerator
from distributed_event_factory.topology.evaluator.topology_evaluator import TopologyEvaluator, TopologyMetrics, TopologyScore
from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologySpec


@dataclass(frozen=True)
class TopologyOptimizationResult:
    best_graph: TopologyGraph
    best_score: TopologyScore
    best_metrics: TopologyMetrics
    iterations: int
    optimization_log: List[dict]


class TopologyOptimizer:
    def __init__(self, evaluator: TopologyEvaluator, action_generator: TopologyActionGenerator):
        self.evaluator = evaluator
        self.action_generator = action_generator

    def optimize(self, spec: TopologySpec, simulate_fn) -> TopologyOptimizationResult:
        optimization_log: List[dict] = []
        best_graph = TopologyGraph.create_initial(spec)
        best_score, best_metrics = self._evaluate_graph(best_graph, spec, simulate_fn)
        optimization_log.append({
            "type": "initial",
            "score": best_score.total,
            "tracePenalty": best_score.trace_length_penalty,
            "distinctPenalty": best_score.distinct_traces_penalty,
            "avgTraceLen": best_metrics.avg_trace_length,
            "distinct": best_metrics.distinct_traces_count,
            "withinTarget": best_score.is_within_target,
        })

        print(
            "[topology] Start optimization: "
            f"score={best_score.total:.3f}, "
            f"tracePenalty={best_score.trace_length_penalty:.3f}, "
            f"distinctPenalty={best_score.distinct_traces_penalty:.3f}, "
            f"avgTraceLen={best_metrics.avg_trace_length:.2f}, "
            f"distinct={best_metrics.distinct_traces_count}"
        )

        iterations = 0
        while iterations < spec.max_iterations and not best_score.is_within_target:
            iterations += 1
            best_candidate_graph = None
            best_candidate_score = None
            best_candidate_metrics = None
            best_candidate_action = None
            evaluated_candidates = 0

            for action in self.action_generator.generate_candidates(best_graph):
                try:
                    candidate_graph = self.action_generator.apply(best_graph, action)
                except ValueError:
                    continue

                candidate_score, candidate_metrics = self._evaluate_graph(candidate_graph, spec, simulate_fn)
                evaluated_candidates += 1

                if best_candidate_score is None or candidate_score.total < best_candidate_score.total:
                    best_candidate_graph = candidate_graph
                    best_candidate_score = candidate_score
                    best_candidate_metrics = candidate_metrics
                    best_candidate_action = action

            print(
                f"[topology] Iteration {iterations}: evaluated={evaluated_candidates}, "
                f"bestCandidate={self._format_action(best_candidate_action)}"
            )
            optimization_log.append({
                "type": "iteration",
                "iteration": iterations,
                "evaluatedCandidates": evaluated_candidates,
                "bestCandidate": self._format_action(best_candidate_action),
                "bestCandidateScore": None if best_candidate_score is None else best_candidate_score.total,
            })

            if best_candidate_graph is None or best_candidate_score is None:
                print("[topology] No valid candidate found, stopping optimization")
                optimization_log.append({
                    "type": "stop",
                    "iteration": iterations,
                    "reason": "no_valid_candidate",
                })
                break

            if best_candidate_score.total < best_score.total:
                best_graph = best_candidate_graph
                best_score = best_candidate_score
                best_metrics = best_candidate_metrics
                print(
                    "[topology] Accepted candidate: "
                    f"score={best_score.total:.3f}, "
                    f"tracePenalty={best_score.trace_length_penalty:.3f}, "
                    f"distinctPenalty={best_score.distinct_traces_penalty:.3f}"
                )
                optimization_log.append({
                    "type": "accepted",
                    "iteration": iterations,
                    "score": best_score.total,
                    "tracePenalty": best_score.trace_length_penalty,
                    "distinctPenalty": best_score.distinct_traces_penalty,
                    "avgTraceLen": None if best_metrics is None else best_metrics.avg_trace_length,
                    "distinct": None if best_metrics is None else best_metrics.distinct_traces_count,
                })
            else:
                print("[topology] No improving candidate found, stopping optimization")
                optimization_log.append({
                    "type": "stop",
                    "iteration": iterations,
                    "reason": "no_improvement",
                    "score": best_score.total,
                })
                break

        print(
            "[topology] Finished optimization: "
            f"iterations={iterations}, finalScore={best_score.total:.3f}, "
            f"withinTarget={best_score.is_within_target}"
        )

        optimization_log.append({
            "type": "final",
            "iterations": iterations,
            "score": best_score.total,
            "tracePenalty": best_score.trace_length_penalty,
            "distinctPenalty": best_score.distinct_traces_penalty,
            "avgTraceLen": best_metrics.avg_trace_length,
            "distinct": best_metrics.distinct_traces_count,
            "withinTarget": best_score.is_within_target,
        })

        return TopologyOptimizationResult(
            best_graph=best_graph,
            best_score=best_score,
            best_metrics=best_metrics,
            iterations=iterations,
            optimization_log=optimization_log,
        )

    def _evaluate_graph(self, graph: TopologyGraph, spec: TopologySpec, simulate_fn) -> Tuple[TopologyScore, TopologyMetrics]:
        events = simulate_fn(graph, spec.sample_size)
        traces = self.evaluator.extract_traces(events)
        metrics = self.evaluator.compute_metrics(traces, spec)
        return self.evaluator.score(metrics, spec), metrics

    @staticmethod
    def _format_action(action) -> str:
        if action is None:
            return "none"
        payload = ", ".join(f"{key}={value}" for key, value in action.payload.items())
        return f"{action.name}({payload})"
