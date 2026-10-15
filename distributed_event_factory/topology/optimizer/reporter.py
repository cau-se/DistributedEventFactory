"""Formats and writes topology optimization reports."""

import os
from datetime import datetime
from typing import Dict

from distributed_event_factory.topology.generator.topology_datasource_generator import TopologyDatasourceGenerator
from distributed_event_factory.topology.model.topology_spec import TopologySpec
from distributed_event_factory.topology.optimizer.pipeline import TopologyPipelineResult


class TopologyReporter:
    def __init__(self, datasource_generator: TopologyDatasourceGenerator):
        self.datasource_generator = datasource_generator

    def report(self, result: TopologyPipelineResult, spec: TopologySpec) -> str:
        successful_cases = sum(
            payload > spec.payload_success_threshold
            for payload in result.completed_payloads.values()
        )
        completed_count = len(result.completed_payloads)
        observed_success_ratio = successful_cases / completed_count if completed_count else 0.0
        topology_summary = self._format_topology_summary(
            result,
            spec,
            observed_success_ratio,
            completed_count,
        )
        optimization_summary = self._format_optimization_summary(
            result,
            spec,
            successful_cases,
            observed_success_ratio,
        )
        logs: Dict[str, str] = {
            "transition": self._format_optimization_log(result.transition.optimization_log),
            "trace entropy": self._format_optimization_log(result.trace_entropy.optimization_log),
            "payload": self._format_optimization_log(result.payload.optimization_log),
        }

        print("[topology] Final topology:")
        print(topology_summary)
        print("[topology] Optimization summary:")
        print(optimization_summary)
        for name, content in logs.items():
            print(f"[topology] Complete {name} optimization log:")
            print(content)

        log_path = self._write_log(topology_summary, optimization_summary, logs)
        print(f"[topology] Full optimization log written to {log_path}")
        return topology_summary

    def _format_topology_summary(self, result, spec, observed_success_ratio, sample_size):
        graph = result.graph
        activity_names = self.datasource_generator.build_activity_names(graph)
        lines = ["nodes:"]
        ordered_nodes = sorted(graph.nodes.values(), key=lambda node: (node.level, node.name))
        lines.extend(f"  - {node.name} (level={node.level})" for node in ordered_nodes)
        lines.append("edges:")
        sorted_edges = sorted(graph.edge_list(), key=lambda edge: (graph.nodes[edge[0]].level, edge[0], edge[1]))
        lines.extend(
            f"  - {src} -> {dst} (transitions={graph.transition_count(src, dst)})"
            for src, dst in sorted_edges
        )
        lines.extend(["", "ASCII topology:"])
        lines.append(
            f"Trace entropy: normalized={result.trace_entropy.normalized_entropy:.4f} "
            f"(target={spec.trace_entropy.target:.4f}±{spec.trace_entropy.tolerance:.4f}), "
            f"mostLikelyTrace={result.trace_entropy.most_likely_trace_probability * 100:.2f}%, "
            f"concentration={result.trace_entropy.concentration:.4f}, "
            f"targetReached={result.trace_entropy.target_reached}"
        )
        lines.append(
            f"Payload optimization: threshold>{spec.payload_success_threshold}, "
            f"successfulCases={observed_success_ratio * 100:.2f}% of {sample_size} cases "
            f"(target={spec.successful_case_ratio.target}%±{spec.successful_case_ratio.tolerance}%), "
            f"initialDelta={result.payload.initial_delta}, iterations={result.payload.iterations}, "
            f"targetReached={result.payload.target_reached}"
        )
        lines.append(
            f"Payload entropy: normalized={result.payload.normalized_entropy:.4f} "
            f"(target={spec.payload_entropy.target:.4f}±{spec.payload_entropy.tolerance:.4f}), "
            f"successTargetReached={result.payload.success_ratio_target_reached}, "
            f"entropyTargetReached={result.payload.entropy_target_reached}"
        )
        lines.append("Expected payload contribution by step:")
        contributions_by_step = {}
        for (src, _, _), contribution in result.payload.expected_contributions.items():
            contributions_by_step[src] = contributions_by_step.get(src, 0.0) + contribution
        for step, contribution in sorted(
            contributions_by_step.items(),
            key=lambda item: (graph.nodes[item[0]].level, item[0]),
        ):
            lines.append(f"  - {step}: {contribution:.2f}")

        for successor in sorted(graph.successors("<start>")):
            lines.append(f"<start> --> {successor}")
        for node in ordered_nodes:
            if node.name in {"<start>", "<end>"}:
                continue
            lines.extend(["", node.name])
            successors = sorted(
                graph.successors(node.name),
                key=lambda name: (graph.nodes[name].level, name),
            )
            for successor in successors:
                for index in range(1, graph.transition_count(node.name, successor) + 1):
                    activity = activity_names[(node.name, successor, index)]
                    probability = graph.transition_probability(node.name, successor, index)
                    delta = graph.payload_delta(node.name, successor, index)
                    lines.append(f"  +-- {activity} (p={probability:.4f}, +{delta}) --> {successor}")
        return "\n".join(lines)

    @staticmethod
    def _format_optimization_summary(result, spec, successful_cases, observed_success_ratio):
        score = result.transition.best_score
        metrics = result.transition.best_metrics
        return (
            f"iterations={result.transition.iterations}\n"
            f"score={score.total:.3f}\n"
            f"tracePenalty={score.trace_length_penalty:.3f}\n"
            f"distinctPenalty={score.distinct_traces_penalty:.3f}\n"
            f"withinTarget={score.is_within_target}\n"
            f"avgTraceLen={metrics.avg_trace_length:.2f}\n"
            f"distinctTraces={metrics.distinct_traces_count}\n"
            f"traceLenMin={metrics.min_trace_length}\n"
            f"traceLenMax={metrics.max_trace_length}\n"
            f"traceLenInIntervalRatio={metrics.traces_in_length_interval_ratio:.3f}\n"
            f"traceNormalizedEntropy={result.trace_entropy.normalized_entropy:.4f}\n"
            f"traceEntropyTargetReached={result.trace_entropy.target_reached}\n"
            f"mostLikelyTrace={result.trace_entropy.most_likely_trace_probability * 100:.2f}%\n"
            f"payloadIterations={result.payload.iterations}\n"
            f"payloadInitialDelta={result.payload.initial_delta}\n"
            f"payloadTargetReached={result.payload.target_reached}\n"
            f"payloadSuccessRatioTargetReached={result.payload.success_ratio_target_reached}\n"
            f"payloadEntropy={result.payload.normalized_entropy:.4f}\n"
            f"payloadEntropyTarget={spec.payload_entropy.target:.4f}±{spec.payload_entropy.tolerance:.4f}\n"
            f"payloadEntropyTargetReached={result.payload.entropy_target_reached}\n"
            f"payloadExpectedSuccessfulCases={result.payload.expected_success_ratio * 100:.2f}%\n"
            f"payloadObservedSuccessfulCases={observed_success_ratio * 100:.2f}% "
            f"({successful_cases}/{len(result.completed_payloads)})"
        )

    @staticmethod
    def _format_optimization_log(entries):
        return "\n".join(
            f"{index:03d}: " + ", ".join(f"{key}={value}" for key, value in entry.items())
            for index, entry in enumerate(entries, start=1)
        )

    @staticmethod
    def _write_log(topology_summary, optimization_summary, logs):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = os.path.join(log_dir, f"topology-optimization-{timestamp}.log")
        with open(log_path, "w") as log_file:
            log_file.write("[topology] Final topology\n")
            log_file.write(topology_summary)
            log_file.write("\n\n[topology] Optimization summary\n")
            log_file.write(optimization_summary)
            for name, content in logs.items():
                log_file.write(f"\n\n[topology] Complete {name} optimization log\n")
                log_file.write(content)
            log_file.write("\n")
        return log_path
