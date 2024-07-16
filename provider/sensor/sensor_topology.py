import abc
from abc import ABC
from typing import List

from core.sensor import Sensor, GenericSensor, StartSensor, EndSensor
from core.sensor_id import SensorId, START_SENSOR_ID, END_SENSOR_ID
from provider.activity.activity_emission_provider import ActivityEmissionProviderFactory
from provider.activity.activity_generation_provider import ActivityGenerationProvider
from provider.sender.send_provider import SendProvider
from provider.transition.duration_provider import DurationProvider, StaticDurationProvider, UniformDurationProvider
from provider.transition.transition_provider import GenericTransitionProvider, TransitionProvider


class SensorTopologyProvider:
    @abc.abstractmethod
    def get_sensors(self, number_of_sensors) -> List[Sensor]:
        pass


class GenericSensorTopologyProvider(SensorTopologyProvider):

    def __init__(
            self,
            transition_provider,
            duration_provider,
            send_provider,
            activity_generation_provider,
            activity_emission_provider
    ):
        self.transition_provider: TransitionProvider = transition_provider
        self.duration_provider: DurationProvider = duration_provider
        self.send_provider: SendProvider = send_provider
        self.activity_generation_provider: ActivityGenerationProvider = activity_generation_provider
        self.activity_emission_provider: ActivityEmissionProviderFactory = activity_emission_provider

    def get_sensors(self, number_of_sensors):
        sensors: List[Sensor] = []

        sensors.append(StartSensor(transition_provider=self.transition_provider, sender=self.send_provider.get_sender(START_SENSOR_ID.get_name())))
        for i in range(number_of_sensors):
            sensor_id = SensorId(str(i))
            sensors.append(
                GenericSensor(
                    sensor_id=sensor_id,
                    transition_provider=self.transition_provider,
                    duration_provider=self.duration_provider,
                    sender=self.send_provider.get_sender(sensor_id.get_name()),
                    activity_emission_provider=self.activity_emission_provider.get_activity_provider(
                        potential_activities=self.activity_generation_provider.get_activities()
                    )
                )
            )
        sensors.append(EndSensor(sender=self.send_provider.get_sender(END_SENSOR_ID.get_name())))

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
