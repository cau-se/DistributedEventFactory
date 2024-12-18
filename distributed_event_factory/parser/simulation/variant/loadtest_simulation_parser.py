from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.simulation.loadtest import LoadTestSimulation


class LoadTestSimulationParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return LoadTestSimulation(
            case_id_provider=self.dependencies["caseId"].parse(config["caseId"]),
            load_provider=self.dependencies["load"].parse(config["load"]),
            generated_timeframes_until_start=config["genTimeframesTilStart"],
            max_concurrent_cases=self.dependencies["maxConcurrentCases"].parse(config["maxConcurrentCases"])
        )