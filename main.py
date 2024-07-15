import os

from provider.activity.activity_emission_provider import UniformActivityEmissionProvider, \
    UniformActivityEmissionProviderFactory
from provider.activity.activity_generation_provider import DistinctActivityGenerationProvider
from provider.data.case_provider import IncreasingCaseIdProvider
from provider.generic.count_provider import StaticCountProvider
from provider.load.load_provider import GradualIncreasingLoadProvider
from provider.sender.send_provider import PrintConsoleSendProvider, KafkaSender, KafkaSendProvider
from provider.sensor.sensor_topology import GenericSensorTopologyProvider
from provider.transition.duration_provider import GaussianDurationProvider
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.transition.transition_probability_provider import DrawWithoutReplacementTransitionProvider
from simulation.simulation import Simulation

if __name__ == '__main__':
    bootstrap_server = "kube1-1:30376"#os.environ["BOOTSTRAP_SERVER"]
    topic = 'topic'#os.environ["TOPIC"]

    simulation = Simulation(
        number_of_sensors_provider=StaticCountProvider(5),
        sensor_topology_provider=
        GenericSensorTopologyProvider(
            next_state_provider=DistinctNextStateProvider(),
            transition_probability_provider=DrawWithoutReplacementTransitionProvider(),
            transition_count_provider=StaticCountProvider(count=3),
            duration_provider=GaussianDurationProvider(mu=10, sigma=1),
            send_provider=PrintConsoleSendProvider(), #KafkaSendProvider()
            activity_emission_provider=UniformActivityEmissionProviderFactory()
        ),
        case_id_provider=IncreasingCaseIdProvider(),
        load_provider=GradualIncreasingLoadProvider(10, 3, 10)
    )
    simulation.start()
