import time

from scheduled_futures import ScheduledThreadPoolExecutor
from network.process_simulator import ProcessSimulator
from provider.data.case_provider import CaseIdProvider, IncreasingCaseIdProvider
from provider.generic.count_provider import CountProvider, StaticCountProvider
from provider.load.load_provider import LoadProvider, GradualIncreasingLoadProvider
from provider.sender.send_provider import PrintConsole, PrintConsoleSendProvider
from provider.sensor.sensor_topology import SensorTopologyProvider, GenericSensorTopologyProvider
from provider.transition.duration_provider import GaussianDurationProvider
from provider.transition.next_state_provider import DistinctNextStateProvider
from provider.transition.transition_probability_provider import DrawWithoutReplacementTransitionProvider


class Simulation:
    def __init__(self, number_of_sensors_provider, sensor_topology_provider, case_id_provider, load_provider):
        self.number_of_sensors_provider: CountProvider = number_of_sensors_provider
        self.sensor_topology_provider: SensorTopologyProvider = sensor_topology_provider
        self.case_id_provider: CaseIdProvider = case_id_provider
        self.load_provider: LoadProvider = load_provider

    def start(self):
        number_of_sensors = self.number_of_sensors_provider.get()
        sensors = self.sensor_topology_provider.get_sensors(number_of_sensors)
        process_simulator = ProcessSimulator(
            sensors=sensors,
            case_id_provider=self.case_id_provider,
        )

        with ScheduledThreadPoolExecutor() as executor:
            while True:
                scheduler = executor.schedule(process_simulator.simulate, period=1/self.load_provider.get_load_value())
                time.sleep(1)
                scheduler.cancel()


if __name__ == '__main__':
    simulation = Simulation(
        number_of_sensors_provider=StaticCountProvider(20),
        sensor_topology_provider=GenericSensorTopologyProvider(
            next_state_provider=DistinctNextStateProvider(),
            transition_probability_provider=DrawWithoutReplacementTransitionProvider(),
            transition_count_provider=StaticCountProvider(count=3),
            duration_provider=GaussianDurationProvider(mu=10, sigma=1),
            send_provider=PrintConsoleSendProvider()
        ),
        case_id_provider=IncreasingCaseIdProvider(),
        load_provider=GradualIncreasingLoadProvider(10, 1, 100)
    )
    simulation.start()