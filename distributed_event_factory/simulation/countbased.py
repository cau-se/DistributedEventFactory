from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.data.count_provider import CountProvider
from distributed_event_factory.simulation.abstract_simulation import Simulation
from distributed_event_factory.simulation.process_simulation import ProcessSimulator


class CountBasedSimulation(Simulation):

    def __init__(self, simulation_steps: int, case_id_provider: CaseIdProvider, max_concurrent_cases: CountProvider):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.simulation_steps = simulation_steps
        self.sinks = dict()
        self.max_concurrent_cases = max_concurrent_cases

    def run_simulation(self, datasources, sinks, hook=lambda: None):
        self.setup_sinks(sinks)
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=datasources,
            max_concurrent_cases=self.max_concurrent_cases
        )

        for i in range(self.simulation_steps):
            event = process_simulator.simulate()
            self.send_event(event)
            hook()
