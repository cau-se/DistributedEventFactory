import random
from typing import List
import numpy


class SensorSelector:

    def __init__(self, probability_distribution):
        self.probability_distribution = probability_distribution

    def get_next_sensor(self):
        return numpy.random.choice(len(self.probability_distribution), p=numpy.array(self.probability_distribution))


class NumberOfSensorsTaker:

    def __init__(self, probability_distribution):
        self.probability_distribution = probability_distribution

    def get(self, number_of_sensors) -> SensorSelector:
        distribution = self.probability_distribution[0:number_of_sensors - 1]
        remaining_probability = 1.0 - sum(distribution)
        distribution.append(remaining_probability)
        return SensorSelector(distribution)


class ProbabilityDistributionGenerator:
    def __init__(self, matrix: List[List[float]]):
        self.probability_distribution_iterator = iter(matrix)

    def get(self) -> NumberOfSensorsTaker:
        return NumberOfSensorsTaker(next(self.probability_distribution_iterator))


class DrawWithoutReplacementTransitionProvider:

    def __init__(self, transition_array_length, transition_indices):
        self.transition_array_length = transition_array_length
        self.transition_indices_provider = transition_indices

    def get_transition_probabilities(self) -> NumberOfSensorsTaker:
        transition_indices = self.transition_indices_provider.get_next_states(self.transition_array_length)
        random_numbers = [0.0] * self.transition_array_length
        remaining_prob = 1.0
        for i in range(len(transition_indices) - 1):
            random_value = round(random.random() * remaining_prob, 2)
            remaining_prob -= random_value
            random_numbers[transition_indices[i]] = random_value

        if remaining_prob > 0:
            random_numbers[transition_indices[len(transition_indices) - 1]] = round(remaining_prob, 2)
        return NumberOfSensorsTaker(random_numbers)
