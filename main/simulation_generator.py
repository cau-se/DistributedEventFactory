from typing import List

from provider.generic.count_provider import StaticCountProvider, UniformCountProvider
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.provider_registry import ProviderRegistry
from provider.sensor.sensor_provider import AbstractSensorProvider
from provider.transition.transition_probability_provider import DrawWithoutReplacementTransitionProvider
from provider.transition.transition_provider import AbstractTransitionProvider
from sensors.sensors import SensorManager, BaseSensor
from provider.transition.duration_provider import GaussianDurationProvider
from utils.transition_matrix_builder import TransitionMatrixBuilder


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
    for i in range(30):
        simulation_generator = SimulationGenerator(
            ProviderRegistry(
                sensor_provider=AbstractSensorProvider(
                    number_of_sensors_provider=UniformCountProvider(20),
                    events_per_sensor_provider=UniformCountProvider(5)),
                transition_provider=AbstractTransitionProvider(
                    duration_provider=GaussianDurationProvider(mu=10, sigma=1),
                    transition_probability_provider=DrawWithoutReplacementTransitionProvider(),
                    next_state_provider=DistinctNextStateProvider(),
                    transition_count_provider=StaticCountProvider(count=1),
                )
            )
        )
        simulation_generator.get_transition_matrix()
        cluster = Cluster();
        cluster.start()
        #print(simulation_generator.get_transition_matrix().print_transition_matrix())
        #print(simulation_generator.get_transition_matrix().print_duration_matrix())
