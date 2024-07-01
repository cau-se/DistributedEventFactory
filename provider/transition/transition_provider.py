import abc
import numpy as np
from typing import List
from core.sensor_id import SensorId


class TransitionProvider:

    @abc.abstractmethod
    def get_next_sensor(self):
        pass


class GenericTransitionProvider(TransitionProvider):

    def __init__(self, next_sensors, next_sensor_probabilities):
        self.next_sensors: List[SensorId] = next_sensors
        self.next_sensor_probabilities = next_sensor_probabilities

    def get_next_sensor(self) -> SensorId:
        i = np.random.choice(len(self.next_sensors), p=np.array(self.next_sensor_probabilities))
        return self.next_sensors[i]
