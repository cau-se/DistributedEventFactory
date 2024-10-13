from src.distributed_event_factory.simulation.new_simulation import NewSimulation

class SimulationParser:

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return NewSimulation(
            load_provider=self.dependencies["load"].parse(config["load"]),
            time_frame_duration=config["timeFrameDuration"],
            case_id_provider=self.dependencies["caseId"].parse(config["caseId"]),
        )
