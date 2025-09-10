from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.simulation.process_simulation import DefProcessSimulator

class DefSimulationParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return DefProcessSimulator(
            case_id_provider=self.dependencies["caseId"].parse(config["caseId"]),
            max_concurrent_cases=self.dependencies["maxConcurrentCases"].parse(config["maxConcurrentCases"]),
            data_sources=self.dependencies["dataSource"].parse(config["dataSource"])
        )