import time

from scheduled_futures import ScheduledThreadPoolExecutor
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.load.load_provider import LoadProvider
from distributed_event_factory.simulation.abstract_simulation import Simulation
from distributed_event_factory.simulation.process_simulation import ProcessSimulator

class StreamSimulation(Simulation):
    def __init__(
            self,
            load_provider: LoadProvider,
            case_id_provider: CaseIdProvider,
    ):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider
        self.sinks = dict()

    def run_simulation(self, datasources, sinks, hook):
        self.setup_sinks(sinks)
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=datasources
        )
        while True:
            with ScheduledThreadPoolExecutor() as executor:
                scheduler = executor.schedule(
                    lambda: self.send_event(process_simulator.simulate()),
                    period=1/self.load_provider.get_load_value()
                )
                hook()
                time.sleep(1)
                scheduler.cancel()
