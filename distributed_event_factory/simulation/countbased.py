from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.data.count_provider import CountProvider
from distributed_event_factory.simulation.abstract_process_simulator import ProcessSimulator
from distributed_event_factory.simulation.abstract_simulation import Simulation


class CountBasedSimulation(Simulation):

    def __init__(self, simulation_steps: int, case_id_provider: CaseIdProvider, max_concurrent_cases: CountProvider):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.simulation_steps = simulation_steps
        self.sinks = dict()
        self.max_concurrent_cases = max_concurrent_cases

    # TODO hrei: Check that the correct process simulator is used here
    def run(self, process_simulator, steps, hook):
        for i in range(steps):
            self.send_event(process_simulator.simulate())
        return

    def run_simulation(
        self,
        process_simulator: ProcessSimulator,
        data_sources,
        sinks,
        hook=lambda: None
    ):
        self.setup_datasource_sink_mapping(sinks)
        #for data_source in data_sources:
        #    process_simulator.add_datasource(name=data_source, data_source=data_sources[data_source])
        self.run(process_simulator, int(self.simulation_steps), hook)
