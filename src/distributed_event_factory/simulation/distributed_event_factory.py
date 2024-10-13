import yaml

from src.distributed_event_factory.provider.provider_registry import ProviderRegistry
from src.distributed_event_factory.simulation.simulation import Simulation

class DistributedEventFactory:

    def __init__(
            self,
            number_of_data_sources_provider,
            case_id_provider,
            event_loop,
            data_source_topology_provider
    ):
        self.simulation = Simulation(
            number_of_data_sources_provider=number_of_data_sources_provider,
            event_loop=event_loop,
            case_id_provider=case_id_provider,
            data_source_topology_provider=data_source_topology_provider
        )

    @classmethod
    def from_config_file(cls, configuration_file):
        with open(configuration_file) as file:
            configuration = yaml.safe_load(file)
        registry = ProviderRegistry(configuration)
        return cls(
            number_of_data_sources_provider=registry.get("numberOfDataSources"),
            case_id_provider=registry.get("caseId"),
            event_loop=registry.get("eventLoop"),
            data_source_topology_provider=registry.get("dataSourceTopology"),
        )

    def start(self):
        self.simulation.start()
