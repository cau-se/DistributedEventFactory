import os

from provider.activity.activity_emission_provider import UniformActivityEmissionProvider, \
    UniformActivityEmissionProviderFactory
from provider.activity.activity_generation_provider import DistinctActivityGenerationProvider, \
    ListBasedActivityGenerationProvider
from provider.data.case_provider import IncreasingCaseIdProvider
from provider.generic.count_provider import StaticCountProvider
from provider.load.load_provider import GradualIncreasingLoadProvider
from provider.sender.send_provider import PrintConsoleSendProvider, KafkaSendProvider
from provider.sensor.sensor_topology import GenericSensorTopologyProvider
from provider.transition.duration_provider import GaussianDurationProvider
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.transition.transition_probability_provider import DrawWithoutReplacementTransitionProvider
from provider.transition.transition_provider import GenericTransitionProvider
from simulation.simulation import Simulation

if __name__ == '__main__':
    bootstrap_server = "kube1-1:30376"  # os.environ["BOOTSTRAP_SERVER"]
    topic = 'topic'  # os.environ["TOPIC"]

    transition_provider = GenericTransitionProvider(
        next_sensor_probabilities_provider=DrawWithoutReplacementTransitionProvider(
            transition_array_length=6,
            transition_indices=DistinctNextStateProvider(
                number_of_next_state_provider=StaticCountProvider(count=3)
            )
        )
    )

    simulation = Simulation(
        number_of_sensors_provider=StaticCountProvider(5),
        sensor_topology_provider=GenericSensorTopologyProvider(
            transition_provider=transition_provider,
            duration_provider=GaussianDurationProvider(mu=10, sigma=1),
            send_provider=PrintConsoleSendProvider(),  # KafkaSendProvider()
            activity_emission_provider=UniformActivityEmissionProviderFactory(),
            activity_generation_provider=ListBasedActivityGenerationProvider(
                sensor_id_activity_map=[
                    ["1", "2", "3"],
                    ["4", "5", "6"],
                    ["7", "8", "9"],
                    ["10", "11", "12"],
                    ["13", "14", "15"]
                ]
            ),
            # DistinctActivityGenerationProvider(
            #    number_of_activities_provider=StaticCountProvider(5)
            # )
        ),
        case_id_provider=IncreasingCaseIdProvider(),
        load_provider=GradualIncreasingLoadProvider(10, 3, 10)
    )
    simulation.start()
