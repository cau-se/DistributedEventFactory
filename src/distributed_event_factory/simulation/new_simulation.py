import time

from scheduled_futures import ScheduledThreadPoolExecutor
from src.distributed_event_factory.provider.data.case_provider import CaseIdProvider
from src.distributed_event_factory.provider.load.load_provider import LoadProvider
from src.distributed_event_factory.simulation.new_process_simulation import NewProcessSimulator

class NewSimulation:
    def send_event(self, event):
        self.sinks[event.node].send(event)

    def __init__(
            self,
            load_provider: LoadProvider,
            time_frame_duration: int,
            case_id_provider: CaseIdProvider,
    ):
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider
        self.time_frame_duration = time_frame_duration
        self.sinks = dict()

    def start(self):
        for sink in self.sinks:
            self.sinks[sink].start_timeframe()

    def end(self):
        for sink in self.sinks:
            self.sinks[sink].end_timeframe()

    def send_event(self, event):
        self.sinks[event.node].send(event)

    def run_simulation(self, datasources, sinks):
        for sink in sinks:
            for data_source in sinks[sink].data_source_ref:
                self.sinks[data_source] = sinks[sink]
        process_simulator = NewProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=datasources
        )
        while True:
            with ScheduledThreadPoolExecutor() as executor:
                #self.start()
                scheduler = executor.schedule(
                    lambda: self.send_event(process_simulator.simulate()),
                    period=1/self.load_provider.get_load_value()
                )
                time.sleep(1)
                #self.end()
                scheduler.cancel()
