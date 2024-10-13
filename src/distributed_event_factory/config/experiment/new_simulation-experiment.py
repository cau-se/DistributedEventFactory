import os

import yaml

from distributed_event_factory.parser.simulation.load.gradual_load_parser import GradualLoadParser
from distributed_event_factory.parser.parser_registry import ParserRegistry
from distributed_event_factory.core.datasource import EndDataSource

if __name__ == '__main__':
    sinks = dict()
    simulations = dict()
    datasources = dict()
    datasources["<end>"] = EndDataSource()
    parser = ParserRegistry()
    parser.load_parser.add_dependency("gradual", GradualLoadParser())

    for filename in os.listdir("../assemblyline"):
        with open("../assemblyline/" + filename) as file:
            configuration = yaml.safe_load(file)
            kind = configuration['kind']
            name = configuration['name']
            parsed_object = parser.kind_parser.parse(configuration)
            if kind == "simulation":
                simulations[name] = parsed_object
            elif kind == "datasource":
                datasources[name] = parsed_object
            elif kind == "sink":
                sinks[name] = parsed_object

    for simulation in simulations:
        simulations[simulation].run_simulation(datasources, sinks)
