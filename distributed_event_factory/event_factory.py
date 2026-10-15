import os

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
from distributed_event_factory.topology.optimizer.pipeline import TopologyPipeline
from distributed_event_factory.topology.optimizer.reporter import TopologyReporter
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

        pipeline = TopologyPipeline(
            datasource_generator=generator,
            datasource_parser=self.parser.datasource_parser,
            topology_optimizer=optimizer,
        )
        result = pipeline.run(topology_spec, simulate_fn)
        self.datasources = result.datasources
        TopologyReporter(generator).report(result, topology_spec)

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
