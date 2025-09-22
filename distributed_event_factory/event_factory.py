import os
import yaml

from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.parser.datasource.event.activity.activity_parser import ActivityParser
from distributed_event_factory.parser.datasource.event.output.output_parser import OutputParser
from distributed_event_factory.parser.datasource.event.transition.transition_parser import TransitionParser
from distributed_event_factory.parser.object.object_source_parser import ObjectSourceParser
from distributed_event_factory.parser.parser_registry import ParserRegistry
from distributed_event_factory.parser.route.route_parser import RouteParser
from distributed_event_factory.parser.simulation.case.case_id_parser import CaseIdParser
from distributed_event_factory.parser.simulation.load.load_parser import LoadParser
from distributed_event_factory.parser.sink.sink_parser import SinkParser
from distributed_event_factory.parser.stock.stock_parser import StockParser
from distributed_event_factory.parser.workforce.workforce_start_positions import WorkforceStartPositionParser
from distributed_event_factory.provider.sink.sink_provider import Sink
from distributed_event_factory.simulation.abstract_process_simulator import ProcessSimulator
from distributed_event_factory.simulation.process_simulator_config_object_centric import \
    ProcessSimulatorConfigObjectCentric


class EventFactory:

    def __init__(self):
        self.sinks = dict()
        self.simulations = dict()
        self.datasources = dict()
        self.process_simulator: ProcessSimulator = None
        self.datasources["<end>"] = EndDataSource()
        self.parser = ParserRegistry()
        # TODO hrei: Check Whether that is on the correct level
        self.objects = dict()
        self.routes = dict()
        self.stocks = dict()
        self.workforce_start_positions = dict()

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

    def add_process_simulator(self, process_simulator):
        self.process_simulator = process_simulator
        return self

    # TODO hrei: It seams that the following 4 are on the wrong level
    def add_output_parser(self, key: str, parser: OutputParser):
        self.parser.output_parser.add_dependency(key, parser)
        return self

    def add_object_source_parser(self, key: str, parser: ObjectSourceParser):
        self.parser.object_source_parser.add_dependency(key, parser)

    def add_route_parser(self, key: str, parser: RouteParser):
        self.parser.route_parser.add_dependency(key, parser)

    def add_workforce_start_position_parser(self, key: str, parser: WorkforceStartPositionParser):
        self.parser.workforce_start_position_parser.add_dependency(key, parser)

    def add_stock_parser(self, key: str, parser: StockParser):
        self.parser.warehouse_stock_parser.add_dependency(key, parser)


    def get_datasource(self, datasource_key):
        return self.datasources[datasource_key]

    def get_sink(self, sink_key):
        return self.sinks[sink_key]

    def get_object_source(self, object_key):
        return self.objects[object_key]

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

    def add_object(self, name, object_source):
        self.objects[name] = object_source
        return self

    def add_route(self, name, routes):
        self.routes[name] = routes
        return self

    def add_stock(self, name, stock):
        self.stocks[name] = stock
        return self

    def add_workforce_start_positions(self, name, workforce_start_positions):
        self.workforce_start_positions[name] = workforce_start_positions
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
            elif kind == "processSimulator":
                self.add_process_simulator(parsed_object)
            # TODO hrei: These should also be on the level of the process simulator
            elif kind == "object":
                self.add_object(name, parsed_object)
            elif kind == "route":
                self.add_route(name, parsed_object)
            elif kind == "stock":
                self.add_stock(name, parsed_object)
            elif kind == "workforces":
                self.add_workforce_start_positions(name, parsed_object)
        return self

    def run(self, hook=lambda: None):
        process_simulator_config = ProcessSimulatorConfigObjectCentric()
        process_simulator_config.add_objects(self.objects)
        process_simulator_config.add_routes(self.routes)
        process_simulator_config.add_stocks(self.stocks)
        process_simulator_config.add_datasources(self.datasources)
        process_simulator_config.add_workforce_start_position(self.workforce_start_positions)

        self.process_simulator.configure(
            process_simulator_config
        )

        for simulation in self.simulations:
            self.simulations[simulation].run_simulation(
                self.process_simulator,
                self.datasources,
                self.sinks,
                hook
            )
