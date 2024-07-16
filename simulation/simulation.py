import time

from scheduled_futures import ScheduledThreadPoolExecutor

from simulation.process_simulator import ProcessSimulator
from provider.data.case_provider import CaseIdProvider
from provider.generic.count_provider import CountProvider
from provider.load.load_provider import LoadProvider
from provider.datasource.sensor_topology import SensorTopologyProvider


class Simulation:

    def __init__(
            self,
            number_of_sensors_provider,
            sensor_topology_provider,
            case_id_provider,
            load_provider
    ):
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

        while True:
            process_simulator.simulate()
        # Make Event Loop interchangable because it does not show the Errors
        #with ScheduledThreadPoolExecutor() as executor:
        #    while True:
        #        scheduler = executor.schedule(
        #            process_simulator.simulate,
        #            period=1 / self.load_provider.get_load_value()
        #        )
        #        time.sleep(1)
        #        scheduler.cancel()
