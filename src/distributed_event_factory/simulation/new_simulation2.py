from typing import Dict
from src.distributed_event_factory.core.datasource import DataSource
from src.distributed_event_factory.provider.data.case_provider import CaseIdProvider
from src.distributed_event_factory.provider.load.load_provider import LoadProvider
from src.distributed_event_factory.provider.sink.sink_provider import Sink
from src.distributed_event_factory.simulation.new_process_simulation import NewProcessSimulator


class NewSimulation2:
    def __init__(
            self,
            load_provider: LoadProvider,
            time_frame_duration: int,
            case_id_provider: CaseIdProvider,
            sinks: Dict[str, Sink],
            data_sources: Dict[str, DataSource],
    ):
        self.case_id_provider = case_id_provider
        self.data_sources = data_sources
        self.sinks = sinks
        self.load_provider = load_provider
        self.time_frame_duration = time_frame_duration

    def send_event(self, event):
        self.sinks[event.node].send(event)

    def start(self):
        for sink in self.sinks:
            self.sinks[sink].start_timeframe()

    def end(self):
        for sink in self.sinks:
            self.sinks[sink].end_timeframe()

    def send_event(self, event):
        if event:
            self.sinks[event.node].send(event)

    def run_simulation(self):
        process_simulator = NewProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=self.data_sources
        )
        while True:
            self.start()
            for i in range(self.load_provider.get_load_value()):
                self.send_event(process_simulator.simulate()),
            self.end()
