import time

from scheduled_futures import ScheduledThreadPoolExecutor
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.load.load_provider import LoadProvider
from distributed_event_factory.simulation.process_simulation import ProcessSimulator

class StreamSimulation:
    def __init__(
            self,
            load_provider: LoadProvider,
            case_id_provider: CaseIdProvider,
    ):
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider
        self.sinks = dict()

    def send_event(self, sinks, event):
        sinks[event.node].send(event)

    def run_simulation(self, datasources, sinks):
        mapped_sinks = dict()
        for sink in sinks:
            for data_source in sinks[sink].data_source_ref:
                mapped_sinks[data_source] = sinks[sink]

        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=datasources
        )
        while True:
            with ScheduledThreadPoolExecutor() as executor:
                scheduler = executor.schedule(
                    lambda: self.send_event(mapped_sinks, process_simulator.simulate()),
                    period=1/self.load_provider.get_load_value()
                )
                time.sleep(1)
                scheduler.cancel()
