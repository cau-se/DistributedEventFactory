import os
from datetime import datetime

import yaml

from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.parser.datasource.event.activity.activity_parser import ActivityParser
from distributed_event_factory.parser.postprocessor.post_processor_parser import PostProcessorParser
from distributed_event_factory.parser.datasource.event.transition.transition_parser import TransitionParser
from distributed_event_factory.parser.parser_registry import ParserRegistry
from distributed_event_factory.parser.simulation.case.case_id_parser import CaseIdParser
from distributed_event_factory.parser.simulation.load.load_parser import LoadParser
from distributed_event_factory.parser.sink.sink_parser import SinkParser
from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor
from distributed_event_factory.provider.data.constant_count_provider import ConstantCountProvider
from distributed_event_factory.provider.data.increasing_case import IncreasingCaseIdProvider
from distributed_event_factory.provider.sink.sink_provider import Sink
from distributed_event_factory.simulation.process_simulation import ProcessSimulator
from distributed_event_factory.topology.actions.topology_actions import TopologyActionGenerator
from distributed_event_factory.topology.evaluator.topology_evaluator import TopologyEvaluator
from distributed_event_factory.topology.generator.topology_datasource_generator import TopologyDatasourceGenerator
from distributed_event_factory.topology.optimizer.topology_optimizer import TopologyOptimizer
from distributed_event_factory.topology.optimizer.payload_optimizer import PayloadOptimizer
from distributed_event_factory.topology.optimizer.entropy_optimizer import TraceEntropyOptimizer


class EventFactory:
    def __init__(self):
        self.sinks = dict()
        self.simulations = dict()
        self.datasources = dict()
        self.post_processors = dict()
        self.topologies = dict()
        self.datasources["<end>"] = EndDataSource()
        self.parser = ParserRegistry()

    def add_load_parser(self, key: str, parser: LoadParser):
        self.parser.load_parser.add_dependency(key, parser)
        return self

    def add_case_id_parser(self, key: str, parser: CaseIdParser):
        self.parser.case_id_parser.add_dependency(key, parser)
        return self

    def add_transition_parser(self, key: str, parser: TransitionParser):
        self.parser.transition_parser.add_dependency(key, parser)
        return self

    def add_activity_parser(self, key: str, parser: ActivityParser):
        self.parser.activity_parser.add_dependency(key, parser)
        return self

    def add_sink_parser(self, key: str, parser: SinkParser):
        self.parser.sink_parser.add_dependency(key, parser)
        return self

    def add_post_processor_parser(self, key: str, parser: PostProcessorParser):
        self.parser.post_processor_parser.add_dependency(key, parser)
        return self

    def add_selection_parser(self, key: str, parser: SinkParser):
        self.parser.probability_selection_parser.add_dependency(key, parser)
        return self

    def get_datasource(self, datasource_key):
        return self.datasources[datasource_key]

    def get_sink(self, sink_key):
        return self.sinks[sink_key]

    def add_directory(self, directory):
        for filename in os.listdir(directory):
            if not filename.startswith(".."):
                self.add_file(directory + "/" + filename)
        return self

    def add_sink(self, name, sink: Sink):
        self.sinks[name] = sink
        return self

    def add_datasource(self, name, datasource):
        self.datasources[name] = datasource
        return self

    def add_simulation(self, name, simulation):
        self.simulations[name] = simulation
        return self

    def add_post_processor(self, name, post_processor: PostProcessor):
        self.post_processors[name] = post_processor
        return self

    def add_topology(self, name: str, topology_spec):
        self.topologies[name] = topology_spec
        return self

    def add_file(self, filename):
        with open(filename) as file:
            configuration = yaml.safe_load(file)
            kind = configuration['kind']
            name = configuration['name']
            parsed_object = self.parser.kind_parser.parse(configuration)
            if kind == "simulation":
                self.add_simulation(name, parsed_object)
            elif kind == "datasource":
                self.add_datasource(name, parsed_object)
            elif kind == "sink":
                self.add_sink(name, parsed_object)
            elif kind == "postProcessor":
                self.add_post_processor(name, parsed_object)
            elif kind == "topology":
                self.add_topology(name, parsed_object)
        return self

    def run(self, hook=lambda: None):
        if len(self.topologies) > 0:
            self._run_topology_pipeline()

        for simulation in self.simulations:
            initial_payload = 0 if self.topologies else 50
            self.simulations[simulation].run_simulation(
                self.datasources,
                self.sinks,
                hook=hook,
                post_processors=self.post_processors,
                initial_payload=initial_payload,
            )

    def _run_topology_pipeline(self):
        topology_spec = next(iter(self.topologies.values()))
        generator = TopologyDatasourceGenerator()
        evaluator = TopologyEvaluator()
        action_generator = TopologyActionGenerator()
        optimizer = TopologyOptimizer(evaluator=evaluator, action_generator=action_generator)

        def simulate_fn(graph, sample_size):
            topology_datasources = generator.build_datasource_objects(graph, self.parser.datasource_parser)
            topology_datasources["<end>"] = EndDataSource()
            end_activity_names = generator.build_end_activity_names(graph)
            return self._simulate_for_topology(
                topology_datasources,
                topology_spec.trace_length.target,
                sample_size,
                end_activity_names,
                initial_payload=0,
            )

        optimization_result = optimizer.optimize(topology_spec, simulate_fn)
        entropy_result = TraceEntropyOptimizer().optimize(optimization_result.best_graph, topology_spec)
        payload_result = PayloadOptimizer().optimize(entropy_result.graph, topology_spec)
        final_graph = payload_result.graph
        final_events = simulate_fn(final_graph, topology_spec.sample_size)
        end_activity_names = generator.build_end_activity_names(final_graph)
        completed_payloads = {
            event.caseid: event.payload
            for event in final_events
            if event.activity in end_activity_names
        }
        successful_cases = sum(
            payload > topology_spec.payload_success_threshold
            for payload in completed_payloads.values()
        )
        observed_success_ratio = successful_cases / len(completed_payloads) if completed_payloads else 0.0
        optimized_datasources = generator.build_datasource_objects(
            final_graph,
            self.parser.datasource_parser
        )
        optimized_datasources["<end>"] = EndDataSource()
        self.datasources = optimized_datasources

        topology_summary = self._format_topology_summary(
            final_graph,
            generator.build_activity_names(final_graph),
            topology_spec.payload_success_threshold,
            topology_spec.successful_case_ratio.target,
            topology_spec.successful_case_ratio.tolerance,
            observed_success_ratio,
            payload_result.initial_delta,
            payload_result.iterations,
            len(completed_payloads),
            payload_result.target_reached,
            entropy_result.normalized_entropy,
            topology_spec.trace_entropy.target,
            topology_spec.trace_entropy.tolerance,
            entropy_result.most_likely_trace_probability,
            entropy_result.concentration,
            entropy_result.target_reached,
            topology_spec.payload_entropy.target,
            topology_spec.payload_entropy.tolerance,
            payload_result.normalized_entropy,
            payload_result.expected_contributions,
            payload_result.success_ratio_target_reached,
            payload_result.entropy_target_reached,
        )
        optimization_summary = (
            f"{self._format_optimization_summary(optimization_result)}\n"
            f"payloadIterations={payload_result.iterations}\n"
            f"payloadInitialDelta={payload_result.initial_delta}\n"
            f"payloadTargetReached={payload_result.target_reached}\n"
            f"payloadSuccessRatioTargetReached={payload_result.success_ratio_target_reached}\n"
            f"payloadEntropy={payload_result.normalized_entropy:.4f}\n"
            f"payloadEntropyTarget={topology_spec.payload_entropy.target:.4f}"
            f"±{topology_spec.payload_entropy.tolerance:.4f}\n"
            f"payloadEntropyTargetReached={payload_result.entropy_target_reached}\n"
            f"payloadExpectedSuccessfulCases={payload_result.expected_success_ratio * 100:.2f}%\n"
            f"payloadObservedSuccessfulCases={observed_success_ratio * 100:.2f}% "
            f"({successful_cases}/{len(completed_payloads)})\n"
            f"traceNormalizedEntropy={entropy_result.normalized_entropy:.4f}\n"
            f"traceEntropyTarget={topology_spec.trace_entropy.target:.4f}"
            f"±{topology_spec.trace_entropy.tolerance:.4f}\n"
            f"mostLikelyTrace={entropy_result.most_likely_trace_probability * 100:.2f}%\n"
            f"traceEntropyTargetReached={entropy_result.target_reached}"
        )
        optimization_log = self._format_optimization_log(optimization_result.optimization_log)
        entropy_optimization_log = self._format_optimization_log(entropy_result.optimization_log)
        payload_optimization_log = self._format_optimization_log(payload_result.optimization_log)

        print("[topology] Final topology:")
        print(topology_summary)
        print("[topology] Optimization summary:")
        print(optimization_summary)
        print("[topology] Complete optimization log:")
        print(optimization_log)
        print("[topology] Complete trace entropy optimization log:")
        print(entropy_optimization_log)
        print("[topology] Complete payload optimization log:")
        print(payload_optimization_log)

        log_path = self._write_topology_log_file(
            topology_summary=topology_summary,
            optimization_summary=optimization_summary,
            optimization_log=optimization_log,
            entropy_optimization_log=entropy_optimization_log,
            payload_optimization_log=payload_optimization_log,
        )
        print(f"[topology] Full optimization log written to {log_path}")

    def _simulate_for_topology(
        self,
        datasources: dict,
        trace_length_target: int,
        sample_size: int,
        end_activity_names: set,
        initial_payload: float = 50,
    ):
        process_simulator = ProcessSimulator(
            data_sources=datasources,
            case_id_provider=IncreasingCaseIdProvider(),
            max_concurrent_cases=ConstantCountProvider(1),
            initial_payload=initial_payload,
        )

        events = []
        completed_cases = set()
        max_event_count = max(sample_size, 1) * max(trace_length_target, 1) * 5

        while len(completed_cases) < sample_size and len(events) < max_event_count:
            event = process_simulator.simulate()
            if event is None or not hasattr(event, "activity"):
                continue

            events.append(event)
            if event.activity in end_activity_names:
                completed_cases.add(event.caseid)

        return events

    def _format_topology_summary(
        self,
        graph,
        activity_names,
        payload_threshold,
        payload_target_ratio,
        payload_ratio_tolerance,
        payload_expected_ratio,
        initial_payload_delta,
        payload_iterations,
        payload_sample_size,
        payload_target_reached,
        trace_entropy,
        trace_entropy_target,
        trace_entropy_tolerance,
        most_likely_trace_probability,
        entropy_concentration,
        entropy_target_reached,
        payload_entropy_target,
        payload_entropy_tolerance,
        payload_entropy,
        payload_contributions,
        payload_success_target_reached,
        payload_entropy_target_reached,
    ):
        lines = []
        lines.append("nodes:")
        ordered_nodes = sorted(graph.nodes.values(), key=lambda node: (node.level, node.name))
        for node in ordered_nodes:
            lines.append(f"  - {node.name} (level={node.level})")

        lines.append("edges:")
        sorted_edges = sorted(graph.edge_list(), key=lambda edge: (graph.nodes[edge[0]].level, edge[0], edge[1]))
        for src, dst in sorted_edges:
            transition_count = graph.transition_count(src, dst)
            lines.append(f"  - {src} -> {dst} (transitions={transition_count})")

        lines.append("")
        lines.append("ASCII topology:")
        lines.append(
            f"Trace entropy: normalized={trace_entropy:.4f} "
            f"(target={trace_entropy_target:.4f}±{trace_entropy_tolerance:.4f}), "
            f"mostLikelyTrace={most_likely_trace_probability * 100:.2f}%, "
            f"concentration={entropy_concentration:.4f}, "
            f"targetReached={entropy_target_reached}"
        )
        lines.append(
            f"Payload optimization: threshold>{payload_threshold}, "
            f"successfulCases={payload_expected_ratio * 100:.2f}% of {payload_sample_size} cases "
            f"(target={payload_target_ratio}%±{payload_ratio_tolerance}%), "
            f"initialDelta={initial_payload_delta}, iterations={payload_iterations}, "
            f"targetReached={payload_target_reached}"
        )
        lines.append(
            f"Payload entropy: normalized={payload_entropy:.4f} "
            f"(target={payload_entropy_target:.4f}±{payload_entropy_tolerance:.4f}), "
            f"successTargetReached={payload_success_target_reached}, "
            f"entropyTargetReached={payload_entropy_target_reached}"
        )
        lines.append("Expected payload contribution by step:")
        contributions_by_step = {}
        for (src, _, _), contribution in payload_contributions.items():
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

            lines.append("")
            lines.append(node.name)
            successors = sorted(
                graph.successors(node.name),
                key=lambda name: (graph.nodes[name].level, name)
            )
            for successor in successors:
                for transition_index in range(1, graph.transition_count(node.name, successor) + 1):
                    activity = activity_names[(node.name, successor, transition_index)]
                    payload_delta = graph.payload_delta(node.name, successor, transition_index)
                    probability = graph.transition_probability(node.name, successor, transition_index)
                    contribution = payload_contributions.get(
                        (node.name, successor, transition_index),
                        0.0,
                    )
                    lines.append(
                        f"  +-- {activity} (p={probability:.4f}, +{payload_delta}) --> {successor}"
                    )
        return "\n".join(lines)

    def _format_optimization_summary(self, optimization_result):
        score = optimization_result.best_score
        metrics = optimization_result.best_metrics
        return (
            f"iterations={optimization_result.iterations}\n"
            f"score={score.total:.3f}\n"
            f"tracePenalty={score.trace_length_penalty:.3f}\n"
            f"distinctPenalty={score.distinct_traces_penalty:.3f}\n"
            f"withinTarget={score.is_within_target}\n"
            f"avgTraceLen={metrics.avg_trace_length:.2f}\n"
            f"distinctTraces={metrics.distinct_traces_count}\n"
            f"traceLenMin={metrics.min_trace_length}\n"
            f"traceLenMax={metrics.max_trace_length}\n"
            f"traceLenInIntervalRatio={metrics.traces_in_length_interval_ratio:.3f}"
        )

    def _format_optimization_log(self, optimization_log):
        lines = []
        for index, entry in enumerate(optimization_log, start=1):
            content = ", ".join(f"{key}={value}" for key, value in entry.items())
            lines.append(f"{index:03d}: {content}")
        return "\n".join(lines)

    def _write_topology_log_file(
        self,
        topology_summary: str,
        optimization_summary: str,
        optimization_log: str,
        entropy_optimization_log: str,
        payload_optimization_log: str,
    ):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_path = os.path.join(log_dir, f"topology-optimization-{timestamp}.log")
        with open(log_path, "w") as log_file:
            log_file.write("[topology] Final topology\n")
            log_file.write(topology_summary)
            log_file.write("\n\n[topology] Optimization summary\n")
            log_file.write(optimization_summary)
            log_file.write("\n\n[topology] Complete optimization log\n")
            log_file.write(optimization_log)
            log_file.write("\n\n[topology] Complete trace entropy optimization log\n")
            log_file.write(entropy_optimization_log)
            log_file.write("\n\n[topology] Complete payload optimization log\n")
            log_file.write(payload_optimization_log)
            log_file.write("\n")
        return log_path
