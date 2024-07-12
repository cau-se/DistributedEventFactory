import abc
from abc import ABC
from typing import List

from core.sensor import Sensor, GenericSensor, StartSensor, EndSensor
from core.sensor_id import SensorId, START_SENSOR_ID, END_SENSOR_ID
from provider.sender.send_provider import Sender, SendProvider
from provider.transition.duration_provider import DurationProvider, StaticDurationProvider, UniformDurationProvider
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
        sensor_ids.append(START_SENSOR_ID)
        sensor_ids.append(END_SENSOR_ID)

        sensors: List[Sensor] = []
        for sensor_id in sensor_ids:
            number_of_next_states = self.transition_count_provider.get()
            sensor_ids_for_transition = self._get_sensor_ids_without_start(sensor_ids)
            transition_provider = GenericTransitionProvider(
                next_sensors=self.next_state_provider.get_next_states(
                    sensor_ids_for_transition,
                    number_of_next_states=number_of_next_states
                ),
                next_sensor_probabilities=self.transition_probability_provider.get_transition_probabilities(
                    number_of_next_states)
            )
            sender = self.send_provider.get_sender(sensor_id.get_name())

            if sensor_id == START_SENSOR_ID:
                new_sensor = StartSensor(transition_provider=transition_provider, sender=sender)
            elif sensor_id == END_SENSOR_ID:
                new_sensor = EndSensor(sender=sender)
            else:
                new_sensor = GenericSensor(
                    sensor_id=sensor_id,
                    transition_provider=transition_provider,
                    duration_provider=self.duration_provider,
                    sender=sender)

            sensors.append(new_sensor)

        return sensors

    def _get_sensor_ids_without_start(self, sensor_ids):
        # TODO here: Mit richtiger equals methode lösen
        valid_sensor_ids = []
        for sensor_id in sensor_ids:
            if sensor_id.get_name() != START_SENSOR_ID.get_name():
                valid_sensor_ids.append(sensor_id)
        return valid_sensor_ids


class ConcreteSensorTopologyProvider(SensorTopologyProvider, ABC):

    def __init__(self, sender):
        self.sender = sender

    def get_sensors(self, number_of_sensors) -> List[Sensor]:
        all_sensors = [SensorId("1"), SensorId("2"), SensorId("3"), END_SENSOR_ID]

        return [
            StartSensor(
                transition_provider=
                GenericTransitionProvider(
                    next_sensors=all_sensors,
                    next_sensor_probabilities=[0.3, 0.4, 0.3, 0]
                ),
                sender=self.sender.get_sender(id="start")
            ),
            GenericSensor(
                sensor_id=SensorId("1"),
                transition_provider=GenericTransitionProvider(
                    next_sensors=all_sensors,
                    next_sensor_probabilities=[0, 0.5, 0.5, 0]
                ),
                duration_provider=UniformDurationProvider(3, 7),
                sender=self.sender.get_sender(id="1")
            ),
            GenericSensor(
                sensor_id=SensorId("2"),
                transition_provider=GenericTransitionProvider(
                    next_sensors=all_sensors,
                    next_sensor_probabilities=[0.3, 0.7, 0, 0]
                ),
                duration_provider=UniformDurationProvider(1, 10),
                sender=self.sender.get_sender(id="2")
            ),
            GenericSensor(
                sensor_id=SensorId("3"),
                transition_provider=GenericTransitionProvider(
                    next_sensors=all_sensors,
                    next_sensor_probabilities=[0.5, 0, 0, 0.5]
                ),
                duration_provider=StaticDurationProvider(1),
                sender=self.sender.get_sender(id="3")
            ),
            EndSensor(
                sender=self.sender.get_sender(id="end")
            )
        ]
