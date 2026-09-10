from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.simulation.process_simulation_object_centric import ProcessSimulationObjectCentric

class ObjectCentricSimulationParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return ProcessSimulationObjectCentric()
