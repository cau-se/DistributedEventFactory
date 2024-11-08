from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.simulation.abstract_simulation import Simulation
from distributed_event_factory.simulation.process_simulation import ProcessSimulator


class CountBasedSimulation(Simulation):

    def __init__(self, simulation_steps: int, case_id_provider: CaseIdProvider):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.simulation_steps = simulation_steps
        self.sinks = dict()

    def run_simulation(self, datasources, sinks, hook=lambda: None):
        super().setup_sinks(sinks)
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=datasources
        )

        for i in range(self.simulation_steps):
            event = process_simulator.simulate()
            print(event)
            self.send_event(event)
            hook()
