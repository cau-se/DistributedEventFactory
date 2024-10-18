from distributed_event_factory.simulation.countbased_simulation import CountBasedSimulation
from distributed_event_factory.simulation.scheduled_simulation import NewSimulation

class SimulationParser:

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return CountBasedSimulation(
            #load_provider=self.dependencies["load"].parse(config["load"]),
            #time_frame_duration=config["timeFrameDuration"],
            case_id_provider=self.dependencies["caseId"].parse(config["caseId"]),
            simulation_steps=100
        )
