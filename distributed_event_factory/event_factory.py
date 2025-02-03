import os
import yaml

from distributed_event_factory.core.datasource import GenericDataSource
from distributed_event_factory.core.datasource_id import DataSourceId
from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.parser.datasource.event.activity.activity_parser import ActivityParser
from distributed_event_factory.parser.datasource.event.transition.transition_parser import TransitionParser
from distributed_event_factory.parser.parser_registry import ParserRegistry
from distributed_event_factory.parser.simulation.case.case_id_parser import CaseIdParser
from distributed_event_factory.parser.simulation.load.load_parser import LoadParser
from distributed_event_factory.parser.sink.sink_parser import SinkParser
from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider
from distributed_event_factory.provider.event.event_provider import CustomEventDataProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider
from distributed_event_factory.provider.eventselection.generic_probability_event_selection_provider import \
    GenericProbabilityEventSelectionProvider
from distributed_event_factory.provider.sink.sink_provider import Sink
from distributed_event_factory.graph_builder.graph_builder import GraphBuilder
from distributed_event_factory.provider.transition.duration.constant_duration import ConstantDurationProvider
from distributed_event_factory.provider.transition.transition.constant_transition import ConstantTransitionProvider


class EventFactory:
    def __init__(self):
        self.sinks = dict()
        self.simulations = dict()
        self.datasources = dict()
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

    def add_selection_parser(self, key: str, parser: SinkParser):
        self.parser.probability_selection_parser.add_dependency(key, parser)
        return self

    def get_datasource(self, datasource_key):
        return self.datasources[datasource_key]

    def get_sink(self, sink_key):
        return self.sinks[sink_key]

    def add_directory(self, directory):
        for filename in os.listdir(directory):
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
        return self

    def build_sources_with_var(self, total_var):
        builder = GraphBuilder()
        graph, variations = builder.build_graph_var(total_var)
        # prints for development:
        print("The datasources are build like:")
        for node in graph:
            print(graph[node].__str__())
        print("The Graph has " + str(variations) + " variations")

        self.graph_to_datasource(graph)
        return self

    def build_sources_with_length(self, max_length):
        builder = GraphBuilder()
        graph, variations = builder.build_graph_length(max_length)

        #prints for development:
        print("The datasources are build like:")
        for node in graph:
            print(graph[node].__str__())
        print("The Graph has " + str(variations) + " variations")

        self.graph_to_datasource(graph)
        return self

    def graph_to_datasource(self, graph):
        for node in graph:
            child_events = []
            for child in graph[node].get_children():
                child_events.append( CustomEventDataProvider(ConstantDurationProvider(3),ConstantActivityProvider(node + child),ConstantTransitionProvider(child)))
            # creation of event provider
            if len(child_events) == 0:
                child_events.append(CustomEventDataProvider(ConstantDurationProvider(3),ConstantActivityProvider("ending"),ConstantTransitionProvider("<end>")))
            prob = 1 / len(child_events)
            prob_list = len(child_events) * [prob]
            event_sel_provider = GenericProbabilityEventSelectionProvider(prob_list, child_events)


            new_datasource = GenericDataSource(DataSourceId(node),"Test",event_provider=event_sel_provider)
            self.add_datasource(node , new_datasource)
        return self

    def run(self, hook=lambda: None):
        for simulation in self.simulations:
            self.simulations[simulation].run_simulation(self.datasources, self.sinks, hook)