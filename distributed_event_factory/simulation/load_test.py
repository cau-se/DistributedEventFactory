from typing import Dict
from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.load.load_provider import LoadProvider
from distributed_event_factory.provider.sink.http.http_sink import HttpSink
from distributed_event_factory.provider.sink.sink_provider import Sink
from distributed_event_factory.simulation.process_simulation import ProcessSimulator

class LoadTestSimulation:
    def __init__(
            self,
            load_provider: LoadProvider,
            time_frame_duration: int,
            case_id_provider: CaseIdProvider,
    ):
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider
        self.time_frame_duration = time_frame_duration

    def start(self, sinks):
        for sink in sinks:
            sinks[sink].start_timeframe()

    def end(self, sinks):
        for sink in sinks:
            sinks[sink].end_timeframe()

    def run_simulation(self, sinks: Dict[str, HttpSink], data_sources: Dict[str, DataSource]):
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=data_sources
        )
        while True:
            self.start(sinks)
            for i in range(self.load_provider.get_load_value()):
                event = process_simulator.simulate()
                if event:
                    sinks[event.node].send(event)
            self.end(sinks)
