import os
import yaml

from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.parser.datasource.event.activity.activity_parser import ActivityParser
from distributed_event_factory.parser.datasource.event.transition.transition_parser import TransitionParser
from distributed_event_factory.parser.parser_registry import ParserRegistry
from distributed_event_factory.parser.simulation.case.case_id_parser import CaseIdParser
from distributed_event_factory.parser.simulation.load.load_parser import LoadParser
from distributed_event_factory.parser.sink.sink_parser import SinkParser


class EventFactory:
    def __init__(self):
        self.sinks = dict()
        self.simulations = dict()
        self.datasources = dict()
        self.datasources["<end>"] = EndDataSource()
        self.parser = ParserRegistry()

    def add_load_parser(self, key: str, parser: LoadParser):
        self.parser.load_parser.add_dependency(key, parser)

    def add_case_id_parser(self, key: str, parser: CaseIdParser):
        self.parser.case_id_parser.add_dependency(key, parser)

    def add_transition_parser(self, key: str, parser: TransitionParser):
        self.parser.transition_parser.add_dependency(key, parser)

    def add_activity_parser(self, key: str, parser: ActivityParser):
        self.parser.activity_parser.add_dependency(key, parser)

    def add_sink_parser(self, key: str, parser: SinkParser):
        self.parser.sink_parser.add_dependency(key, parser)

    def add_selection_parser(self, key: str, parser: SinkParser):
        self.parser.probability_selection_parser.add_dependency(key, parser)

    def run(self, directory):
        for filename in os.listdir(directory):
            with open(directory + "/" + filename) as file:
                configuration = yaml.safe_load(file)
                kind = configuration['kind']
                name = configuration['name']
                parsed_object = self.parser.kind_parser.parse(configuration)
                if kind == "simulation":
                    self.simulations[name] = parsed_object
                elif kind == "datasource":
                    self.datasources[name] = parsed_object
                elif kind == "sink":
                    self.sinks[name] = parsed_object

        for simulation in self.simulations:
            self.simulations[simulation].run_simulation(self.datasources, self.sinks)
