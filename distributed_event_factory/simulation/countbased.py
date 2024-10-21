from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.simulation.process_simulation import ProcessSimulator


class CountBasedSimulation:

    def __init__(
            self,
            simulation_steps: int,
            case_id_provider: CaseIdProvider,
    ):
        self.case_id_provider = case_id_provider
        self.simulation_steps = simulation_steps
        self.sinks = dict()

    def send_event(self, event):
        self.sinks[event.node].send(event)

    def run_simulation(self, datasources, sinks):
        for sink in sinks:
            for data_source in sinks[sink].data_source_ref:
                self.sinks[data_source] = sinks[sink]
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=datasources
        )

        for i in range(self.simulation_steps):
            self.send_event(process_simulator.simulate())
