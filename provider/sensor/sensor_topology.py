import abc
from typing import List

from core.sensor import Sensor, GenericSensor
from core.sensor_id import SensorId, START_SENSOR, END_SENSOR
from provider.sender.send_provider import Sender, SendProvider
from provider.transition.duration_provider import DurationProvider
from provider.transition.next_state_provider import NextStateProvider
from provider.transition.transition_probability_provider import TransitionProbabilityProvider
from provider.transition.transition_provider import GenericTransitionProvider


class SensorTopologyProvider:
    @abc.abstractmethod
    def get_sensors(self, number_of_sensors) -> List[Sensor]:
        pass


class GenericSensorTopologyProvider(SensorTopologyProvider):

    def __init__(self, next_state_provider, transition_probability_provider, transition_count_provider,
                 duration_provider, send_provider):
        self.next_state_provider: NextStateProvider = next_state_provider
        self.transition_probability_provider: TransitionProbabilityProvider = transition_probability_provider
        self.transition_count_provider = transition_count_provider
        self.duration_provider: DurationProvider = duration_provider
        self.send_provider: SendProvider = send_provider

    def get_sensors(self, number_of_sensors):
        sensor_ids: List[SensorId] = []
        for i in range(number_of_sensors):
            sensor_ids.append(SensorId(str(i)))
        sensor_ids.append(START_SENSOR)
        sensor_ids.append(END_SENSOR)

        sensors: List[Sensor] = []
        for sensor_id in sensor_ids:
            number_of_next_states = self.transition_count_provider.get()
            sensor_ids_for_transition = self._get_sensor_ids_without_start(sensor_ids)
            new_sensor = GenericSensor(
                sensor_id=sensor_id,
                transition_provider=GenericTransitionProvider(
                    next_sensors=self.next_state_provider.get_next_states(
                        sensor_ids_for_transition,
                        number_of_next_states=number_of_next_states
                    ),
                    next_sensor_probabilities=self.transition_probability_provider.get_transition_probabilities(
                        number_of_next_states)
                ),
                duration_provider=self.duration_provider,
                sender=self.send_provider.get_sender(sensor_id.get_name())
            )
            sensors.append(new_sensor)
        return sensors

    def _get_sensor_ids_without_start(self, sensor_ids):
        # TODO here: Mit richtiger equals methode lösen
        valid_sensor_ids = []
        for sensor_id in sensor_ids:
            if sensor_id.get_name() != START_SENSOR.get_name():
                valid_sensor_ids.append(sensor_id)
        return valid_sensor_ids