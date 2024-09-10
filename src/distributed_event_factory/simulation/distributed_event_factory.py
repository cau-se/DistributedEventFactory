import yaml

from src.distributed_event_factory.provider.provider_registry import ProviderRegistry
from src.distributed_event_factory.simulation.simulation import Simulation


class DistributedEventFactory:

    def __init__(self, configuration_file):
        self.configuration_file = configuration_file

    def start(self):
        with open(self.configuration_file) as file:
            configuration = yaml.safe_load(file)
        registry = ProviderRegistry(configuration)

        simulation = Simulation(
            number_of_data_sources_provider=registry.get("numberOfDataSources"),
            case_id_provider=registry.get("caseId"),
            event_loop=registry.get("eventLoop"),
            data_source_topology_provider=registry.get("dataSourceTopology"),
        )
        simulation.start()
