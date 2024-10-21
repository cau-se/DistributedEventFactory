from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.simulation.countbased import CountBasedSimulation


class CountBasedSimulationParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return CountBasedSimulation(
            simulation_steps=config["steps"],
            case_id_provider=self.dependencies["caseId"].parse(config["caseId"])
        )