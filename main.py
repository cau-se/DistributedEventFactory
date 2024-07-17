import os

from provider.activity.activity_emission_provider import UniformActivityEmissionProvider, \
    UniformActivityEmissionProviderFactory
from provider.activity.activity_generation_provider import DistinctActivityGenerationProvider, \
    ListBasedActivityGenerationProvider
from provider.data.case_provider import IncreasingCaseIdProvider
from provider.datasource.datasource_id_provider import ListBasedSourceIdProvider
from provider.generic.count_provider import StaticCountProvider
from provider.load.load_provider import GradualIncreasingLoadProvider
from provider.sender.send_provider import PrintConsoleSendProvider, KafkaSendProvider
from provider.datasource.sensor_topology import GenericSensorTopologyProvider
from provider.sender.terminal_sink import TerminalGuiSendProvider
from provider.transition.duration_provider import GaussianDurationProvider
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.transition.transition_provider_factory import ProbabilityDistributionGenerator
from simulation.simulation import Simulation

if __name__ == '__main__':
    bootstrap_server = "kube1-1:30376"  # os.environ["BOOTSTRAP_SERVER"]
    topic = 'topic'  # os.environ["TOPIC"]

    simulation = Simulation(
        number_of_sensors_provider=
        StaticCountProvider(4),
        case_id_provider=
        IncreasingCaseIdProvider(),
        load_provider=
        GradualIncreasingLoadProvider(
            tick_count_til_maximum_reached=10,
            minimal_load=3,
            maximal_load=10
        ),
        sensor_topology_provider=
        GenericSensorTopologyProvider(
            data_source_id_provider=
            ListBasedSourceIdProvider(
                ["Manfred", "Julia", "Frank", "Ursula", "Peter", "Inge", "Klaus", "Fritz", "Jochen"]
            ),
            transition_provider_factory=
            #DrawWithoutReplacementTransitionProbabilityProviderFactory(
            #    transition_indices_provider=
            #    DistinctNextStateProvider(
            #        number_of_next_state_provider=StaticCountProvider(count=3)
            #    )
            #)
            ProbabilityDistributionGenerator(
                matrix=[
                     #m   #j   #f   #u   #e
                    [0.5, 0.5, 0.0, 0.0], #START
                    [0.5, 0.5, 0.0, 0.0], #Manfred
                    [0.0, 0.5, 0.5, 0.0], #Julia
                    [0.0, 0.0, 0.5, 0.5], #Frank
                    [0.0, 0.0, 0.0, 0.5], #Ursula
                ]
            ),
            duration_provider=
            GaussianDurationProvider(
                mu=10,
                sigma=1
            ),
            send_provider=
            PrintConsoleSendProvider(),
            #KafkaSendProvider(),
            #TerminalGuiSendProvider(),
            activity_emission_provider=
            UniformActivityEmissionProviderFactory(
                potential_activities_provider=
                ListBasedActivityGenerationProvider(
                    sensor_id_activity_map=[
                        ["1", "2", "3"],
                        ["4", "5", "6"],
                        ["7", "8", "9"],
                        ["10", "11", "12"],
                        ["13", "14", "15"],
                        ["13", "14", "15"],
                        ["16", "17", "18"],
                        ["19"],
                        ["20", "21"],
                        ["25"],
                        ["26", "27", "28"],
                    ]
                )
                #DistinctActivityGenerationProvider(
                #   number_of_activities_provider=StaticCountProvider(5)
                #)
            )
        )
    )
    simulation.start()
