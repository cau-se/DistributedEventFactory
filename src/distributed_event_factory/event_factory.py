import os
import yaml

from src.distributed_event_factory.parser.parser_registry import ParserRegistry
from src.distributed_event_factory.core.datasource import EndDataSource

class EventFactory:
    def __init__(self):
        self.sinks = dict()
        self.simulations = dict()
        self.datasources = dict()
        self.datasources["<end>"] = EndDataSource()
        self.parser = ParserRegistry()

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

if __name__ == '__main__':
    EventFactory("")