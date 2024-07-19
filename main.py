from provider.provider_registry import ProviderRegistry
from simulation.simulation import Simulation
import yaml

if __name__ == '__main__':
    with open('simulator.yml') as file:
        configuration = yaml.safe_load(file)
    registry = ProviderRegistry(configuration)

    simulation = Simulation(
        number_of_sensors_provider=registry.get("numberOfSensors"),
        case_id_provider=registry.get("caseId"),
        load_provider=registry.get("loadProfile"),
        sensor_topology_provider=registry.get("sensorTopology"),
    )
    simulation.start()
