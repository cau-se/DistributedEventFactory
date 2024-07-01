import sys
from abc import abstractmethod

import core.sensor
from core.sensor import GenericSensor
from provider.transition.duration_provider import StaticDurationProvider, GaussianDurationProvider
from provider.transition.transition_probability_provider import DrawWithoutReplacementTransitionProvider
from provider.transition.transition_provider import GenericTransitionProvider
from sensors.sensor_collection import SingleValueSensor
import random
from string import ascii_uppercase as alphabet


class SensorProvider:

    @abstractmethod
    def get_sensors(self):
        pass


class AbstractSensorProvider(SensorProvider):
    def __init__(self, number_of_sensors_provider, events_per_sensor_provider):
        self.potential_event_names = self.init_sensor_names()
        self.number_of_sensors_provider = number_of_sensors_provider
        self.events_per_sensor_provider = events_per_sensor_provider

    def init_sensor_names(self):
        potential_sensor_names = []
        for char in alphabet:
            for char2 in alphabet:
                potential_sensor_names.append("Event " + char + char2)
        return iter(potential_sensor_names)

    def get_next_event_name(self):
        return next(self.potential_event_names)

    def get_events_per_sensor(self):
        sensor_values = []
        no_events = self.events_per_sensor_provider.get()
        for i in range(no_events):
            sensor_values.append(self.get_next_event_name())
        return sensor_values

    def get_random(self, array):
        return array[int(random.uniform(0, len(array) - 1))]

    def get_sensors(self):
        sensors = []
        for i in range(self.number_of_sensors_provider.get()):
            events_per_sensor = self.get_events_per_sensor()
            sensors.append(SingleValueSensor(events_per_sensor, "Sensor " + str(i)))
        return sensors


class NewSensorProvider(SensorProvider):
    def __init__(self, sensor_names):
        self.sensor_names = sensor_names,

    def init_sensor_names(self):
        potential_sensor_names = []
        for char in alphabet:
            for char2 in alphabet:
                potential_sensor_names.append("Event " + char + char2)
        return iter(potential_sensor_names)

    def get_next_event_name(self):
        return next(self.potential_event_names)

    def get_events_per_sensor(self):
        sensor_values = []
        no_events = self.events_per_sensor_provider.get()
        for i in range(no_events):
            sensor_values.append(self.get_next_event_name())
        return sensor_values

    def get_random(self, array):
        return array[int(random.uniform(0, len(array) - 1))]

    def get_sensors(self):
        sensors = []
        for sensor_name in self.sensor_names:
            sensors.append(
                GenericSensor(
                    sensor_name,
                    GenericTransitionProvider(
                        next_sensors=sensor_name,
                        next_sensor_probabilities=
                        DrawWithoutReplacementTransitionProvider()
                        .get_transition_probabilities(
                            len(self.sensor_names)
                        )
                    ),
                    GaussianDurationProvider(mu=10, sigma=2)
                )
            )
        return sensors
