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
            case_id_provider: CaseIdProvider,
    ):
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider

    def start(self, sinks):
        for sink in sinks:
            sinks[sink].start_timeframe()

    def end(self, sinks):
        for sink in sinks:
            sinks[sink].end_timeframe()

    def run_simulation(self, data_sources: Dict[str, DataSource], sinks: Dict[str, HttpSink]):
        mapped_sinks = dict()
        for sink in sinks:
            for data_source in sinks[sink].data_source_ref:
                mapped_sinks[data_source] = sinks[sink]
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=data_sources
        )
        while True:
            self.start(mapped_sinks)
            for i in range(int(self.load_provider.get_load_value())):
                event = process_simulator.simulate()
                if event:
                    mapped_sinks[event.node].send(event)
            self.end(mapped_sinks)
