import os

from provider.provider_registry import ProviderRegistry
from simulation.simulation import Simulation
from dotenv import load_dotenv
import yaml

if __name__ == '__main__':
    load_dotenv()
    config_file = os.environ["CONFIG_FILE"]

    with open(config_file) as file:
        configuration = yaml.safe_load(file)
    registry = ProviderRegistry(configuration)

    simulation = Simulation(
        number_of_data_sources_provider=registry.get("numberOfDataSources"),
        case_id_provider=registry.get("caseId"),
        event_loop=registry.get("eventLoop"),
        data_source_topology_provider=registry.get("dataSourceTopology"),
    )
    simulation.start()
