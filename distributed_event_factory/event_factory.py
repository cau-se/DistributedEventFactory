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
            self.simulations[simulation].run_simulation(
                self.datasources,
                self.sinks,
                hook=hook,
                post_processors=self.post_processors
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
                end_activity_names
            )

        optimization_result = optimizer.optimize(topology_spec, simulate_fn)
        optimized_datasources = generator.build_datasource_objects(
            optimization_result.best_graph,
            self.parser.datasource_parser
        )
        optimized_datasources["<end>"] = EndDataSource()
        self.datasources = optimized_datasources

        topology_summary = self._format_topology_summary(optimization_result.best_graph)
        optimization_summary = self._format_optimization_summary(optimization_result)
        optimization_log = self._format_optimization_log(optimization_result.optimization_log)

        print("[topology] Final topology:")
        print(topology_summary)
        print("[topology] Optimization summary:")
        print(optimization_summary)
        print("[topology] Complete optimization log:")
        print(optimization_log)

        log_path = self._write_topology_log_file(
            topology_summary=topology_summary,
            optimization_summary=optimization_summary,
            optimization_log=optimization_log,
        )
        print(f"[topology] Full optimization log written to {log_path}")

    def _simulate_for_topology(
        self,
        datasources: dict,
        trace_length_target: int,
        sample_size: int,
        end_activity_names: set
    ):
        process_simulator = ProcessSimulator(
            data_sources=datasources,
            case_id_provider=IncreasingCaseIdProvider(),
            max_concurrent_cases=ConstantCountProvider(1)
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

    def _format_topology_summary(self, graph):
        lines = []
        lines.append("nodes:")
        ordered_nodes = sorted(graph.nodes.values(), key=lambda node: (node.level, node.name))
        for node in ordered_nodes:
            lines.append(f"  - {node.name} (level={node.level})")

        lines.append("edges:")
        sorted_edges = sorted(graph.edge_list(), key=lambda edge: (graph.nodes[edge[0]].level, edge[0], edge[1]))
        for src, dst in sorted_edges:
            lines.append(f"  - {src} -> {dst}")
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

    def _write_topology_log_file(self, topology_summary: str, optimization_summary: str, optimization_log: str):
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
            log_file.write("\n")
        return log_path
