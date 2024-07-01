import random
from typing import List

from network.cluster import Cluster
from network.markov_chain_node_data_processor import MarkovChainNodeDataProcessor
from network.node import Node
from provider.data.data_provider import NodeDataProvider
from provider.generic.count_provider import StaticCountProvider, UniformCountProvider
from provider.load.load_provider import GradualIncreasingLoadProvider
from provider.sender.send_provider import PrintConsole
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.provider_registry import ProviderRegistry
from provider.sensor.sensor_provider import AbstractSensorProvider
from provider.transition.transition_probability_provider import DrawWithoutReplacementTransitionProvider
from provider.transition.transition_provider import AbstractTransitionProvider
from sensors.sensors import SensorManager, BaseSensor
from provider.transition.duration_provider import GaussianDurationProvider
from utils.transition_matrix_builder import TransitionMatrixBuilder
from utils.utils_types import GeneratedEvent


def node_join_function(data: List[GeneratedEvent]) -> GeneratedEvent:
    return random.choice(data)

class SimulationGenerator:
    def __init__(self, provider_registry):
        self.provider_registry: ProviderRegistry = provider_registry
        self.sensor_manager: SensorManager = SensorManager()
        self.transition_matrix: TransitionMatrixBuilder = TransitionMatrixBuilder()
        self._build_sensors()
        self._add_transitions_to_sensors()

    def _build_sensors(self):
        sensors: List[BaseSensor] = self.provider_registry.get_sensor_provider().get_sensors()
        for sensor in sensors:
            self.sensor_manager.add_sensor(sensor)
            self.transition_matrix.add_state(sensor.get_name())

    def _add_transitions_to_sensors(self):
        providers = self.provider_registry
        for state in self.transition_matrix.get_states():
            transitions = providers.transition_provider.get_transition(self.sensor_manager.get_sensor_names())
            for transition in transitions:
                self.transition_matrix.add_transition(
                    state,
                    transition.next_state,
                    transition.probability,
                    transition.duration)

    def get_transition_matrix(self):
        return self.transition_matrix


if __name__ == '__main__':

    simulation_generator = SimulationGenerator(
        ProviderRegistry(
            sensor_provider=AbstractSensorProvider(
                number_of_sensors_provider=UniformCountProvider(20),
                events_per_sensor_provider=UniformCountProvider(5)),
            transition_provider=AbstractTransitionProvider(
                duration_provider=GaussianDurationProvider(mu=10, sigma=1),
                transition_probability_provider=DrawWithoutReplacementTransitionProvider(),
                next_state_provider=DistinctNextStateProvider(),
                transition_count_provider=StaticCountProvider(count=5),
            )
        )
    )
    nodes = []
    data_processor: MarkovChainNodeDataProcessor = MarkovChainNodeDataProcessor(
        1,
        sensor_manager=simulation_generator.sensor_manager,
        transition_matrix=simulation_generator.get_transition_matrix().to_transition_matrix(),
        duration_matrix=simulation_generator.get_transition_matrix().to_duration_matrix()
    )
    node = Node(1, data_processor, cache_length=300)
    nodes.append(node)
    cluster = Cluster(
        nodes=nodes,
        join_function=node_join_function,
        sender_provider = PrintConsole(),
        data_provider = NodeDataProvider(nodes=nodes, join_function=node_join_function),
        load_provider = GradualIncreasingLoadProvider(
            tick_count_til_maximum_reached=60,
            minimal_load=0,
            maximal_load=100
        )
    )

    print(simulation_generator.get_transition_matrix().print_transition_matrix())
    cluster.start()
        #print(simulation_generator.get_transition_matrix().print_duration_matrix())
