from abc import ABC, abstractmethod
import numpy

class AbstractNextSensorProvider(ABC):
    @abstractmethod
    def get_next_sensor(self):
        pass


class NextSensorProvider(AbstractNextSensorProvider):

    def __init__(self, probability_distribution):
        self.probability_distribution = probability_distribution

    def get_next_sensor(self) -> int:
        return numpy.random.choice(len(self.probability_distribution), p=numpy.array(self.probability_distribution))


class NextSensorChooseProvider:
    def __init__(self, number_of_data_sources):
        self.number_of_sensors = number_of_data_sources

    def get(self, probability_distribution) -> NextSensorProvider:
        distribution = probability_distribution[0:self.number_of_sensors - 1]
        remaining_probability = 1.0 - sum(distribution)
        distribution.append(remaining_probability)
        return NextSensorProvider(distribution)


class DistinctNextSensorProvider(AbstractNextSensorProvider):
    def __init__(self, next_sensor_index):
        self.next_sensor_index = next_sensor_index

    def get_next_sensor(self):
        return self.next_sensor_index

