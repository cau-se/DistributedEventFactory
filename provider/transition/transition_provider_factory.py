import random
import numpy
from abc import ABC, abstractmethod


class NextSensorProvider:

    def __init__(self, probability_distribution):
        self.probability_distribution = probability_distribution

    def get_next_sensor(self):
        return numpy.random.choice(len(self.probability_distribution), p=numpy.array(self.probability_distribution))


class RandomProbabilityDistributionGenerator:
    def __init__(self, number_of_sensors):
        self.number_of_sensors = number_of_sensors

    def get(self, probability_distribution) -> NextSensorProvider:
        distribution = probability_distribution[0:self.number_of_sensors - 1]
        remaining_probability = 1.0 - sum(distribution)
        distribution.append(remaining_probability)
        return NextSensorProvider(distribution)


class RandomTransitionMatrixProvider:

    def __init__(self, transition_indices):
        self.transition_indices_provider = transition_indices

    def next(self, number_of_sensors) -> NextSensorProvider:
        transition_indices = self.transition_indices_provider.get_next_states(number_of_sensors)
        random_numbers = [0.0] * number_of_sensors
        remaining_prob = 1.0
        for i in range(len(transition_indices) - 1):
            random_value = round(random.random() * remaining_prob, 2)
            remaining_prob -= random_value
            random_numbers[transition_indices[i]] = random_value

        if remaining_prob > 0:
            random_numbers[transition_indices[len(transition_indices) - 1]] = round(remaining_prob, 2)
        return RandomProbabilityDistributionGenerator(number_of_sensors).get(random_numbers)


class TransitionProvider(ABC):
    @abstractmethod
    def get(self, number_of_sensors) -> NextSensorProvider:
        pass


class RandomTransitionProvider(TransitionProvider):
    def __init__(self, provider: RandomTransitionMatrixProvider):
        self.provider = provider

    def get(self, number_of_sensors):
        return self.provider.next(number_of_sensors)


class MatrixBasedTransitionProvider(TransitionProvider):
    def __init__(self, matrix):
        self.probability_distribution_iterator = iter(matrix)

    def get(self, number_of_sensors):
        return RandomProbabilityDistributionGenerator(number_of_sensors).get(next(self.probability_distribution_iterator))
