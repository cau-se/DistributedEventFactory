from provider.provider_registry import ProviderRegistry
from simulation.simulation import Simulation
import yaml

if __name__ == '__main__':
    with open('proposed.yml') as file:
        configuration = yaml.safe_load(file)
    registry = ProviderRegistry(configuration)

    simulation = Simulation(
        number_of_data_sources_provider=registry.get("numberOfDataSources"),
        case_id_provider=registry.get("caseId"),
        event_loop=registry.get("eventLoop"),
        data_source_topology_provider=registry.get("dataSourceTopology"),
    )
    simulation.start()
