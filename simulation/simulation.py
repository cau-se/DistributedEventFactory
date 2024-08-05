from simulation.event_loop import EventLoop
from simulation.process_simulator import ProcessSimulator
from provider.data.case_provider import CaseIdProvider
from provider.generic.count_provider import CountProvider
from provider.load.load_provider import LoadProvider
from provider.datasource.sensor_topology import DataSourceTopologyProvider


class Simulation:

    def __init__(
            self,
            number_of_data_sources_provider: CountProvider,
            data_source_topology_provider: DataSourceTopologyProvider,
            case_id_provider: CaseIdProvider,
            event_loop: EventLoop
    ):
        self.number_of_data_sources_provider: CountProvider = number_of_data_sources_provider
        self.data_source_topology_provider: DataSourceTopologyProvider = data_source_topology_provider
        self.case_id_provider: CaseIdProvider = case_id_provider
        self.event_loop = event_loop

    def start(self):
        number_of_data_sources = self.number_of_data_sources_provider.get()
        data_sources = self.data_source_topology_provider.get_sensor_topology(number_of_data_sources)
        process_simulator = ProcessSimulator(
            data_sources=data_sources,
            case_id_provider=self.case_id_provider,
        )
        self.event_loop.run(process_simulator)
