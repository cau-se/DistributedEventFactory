from typing import Dict
from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.load.load_provider import LoadProvider
from distributed_event_factory.provider.sink.http.http_sink import LoadTestHttpSink
from distributed_event_factory.simulation.abstract_simulation import Simulation
from distributed_event_factory.simulation.process_simulation import ProcessSimulator

class LoadTestSimulation(Simulation):
    def __init__(
            self,
            load_provider: LoadProvider,
            case_id_provider: CaseIdProvider,
            generated_timeframes_until_start: int
    ):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.load_provider = load_provider
        self.generated_timeframes_until_start = generated_timeframes_until_start

    def start_timeframe(self, sinks):
        for sink in sinks:
            for s in sinks[sink]:
                s.start_timeframe()

    def end_timeframe(self, sinks):
        for sink in sinks:
            for s in sinks[sink]:
                s.end_timeframe()

    def start_simulation(self, sinks):
        for sink in sinks:
            for s in sinks[sink]:
                s.start()

    def run_simulation(self, data_sources: Dict[str, DataSource], sinks: Dict[str, LoadTestHttpSink], hook = lambda: None):
        self.setup_sinks(sinks)
        process_simulator = ProcessSimulator(
            case_id_provider=self.case_id_provider,
            data_sources=data_sources
        )
        iteration = 0
        while True:
            if iteration == self.generated_timeframes_until_start:
                self.start_simulation(self.sinks)
            self.start_timeframe(self.sinks)
            for _ in range(int(self.load_provider.get_load_value())):
                self.send_event(process_simulator.simulate())
                hook()
            self.end_timeframe(self.sinks)
            iteration = iteration + 1
