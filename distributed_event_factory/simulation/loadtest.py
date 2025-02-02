from typing import Dict
from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.data.count_provider import CountProvider
from distributed_event_factory.provider.load.load_provider import LoadProvider
from distributed_event_factory.provider.sink.http.http_sink import LoadTestHttpSink
from distributed_event_factory.simulation.abstract_simulation import Simulation
from distributed_event_factory.simulation.process_simulation import ProcessSimulator


class LoadTestSimulation(Simulation):
    def __init__(
            self,
            load_provider: LoadProvider,
            case_id_provider: CaseIdProvider,
            generated_timeframes_until_start: int,
            max_concurrent_cases: CountProvider
    ):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider
        self.generated_timeframes_until_start = generated_timeframes_until_start
        self.max_concurrent_cases = max_concurrent_cases
        self.sink = []

    def start_timeframe(self, sinks):
        for sink in self.sink:
           sink.start_timeframe()

    def end_timeframe(self, sinks):
        for sink in self.sink:
           sink.end_timeframe()

    def start_simulation(self, sinks):
        for sink in self.sink:
           sink.start()

    def run_simulation(self, data_sources: Dict[str, DataSource], datasource_sink_mapping: Dict[str, LoadTestHttpSink],
                       hook=lambda: None):
        self.setup_datasource_sink_mapping(datasource_sink_mapping)
        for sink in datasource_sink_mapping:
            self.sink.append(datasource_sink_mapping[sink])

        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=data_sources,
            max_concurrent_cases=self.max_concurrent_cases
        )
        iteration = 0
        while True:
            if iteration == self.generated_timeframes_until_start:
                self.start_simulation(self.datasource_sink_mapping)
            self.start_timeframe(self.datasource_sink_mapping)
            for _ in range(int(self.load_provider.get_load_value())):
                self.send_event(process_simulator.simulate())
                hook()
            self.end_timeframe(self.datasource_sink_mapping)
            iteration = iteration + 1
