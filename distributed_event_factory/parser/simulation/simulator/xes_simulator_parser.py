from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator


class XesSimulationParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return XesProcessSimulator(config["filePath"])
