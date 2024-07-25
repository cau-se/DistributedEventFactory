from abc import ABC, abstractmethod
import random

from provider.generic.count_provider_registry import CountProviderRegistry
from provider.transition.next_sensor_provider import NextSensorProvider, NextSensorChooseProvider
from provider.transition.next_state_provider import DistinctProbabilityDistributionProvider


class TransitionMatrixCreationStrategy(ABC):
    @abstractmethod
    def next(self, number_of_sensors) -> NextSensorProvider:
        pass


class RandomTransitionMatrixCreationStrategy(TransitionMatrixCreationStrategy):

    def __init__(self, probability_distribution):
        self.transition_indices_provider = probability_distribution

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
        return NextSensorChooseProvider(number_of_sensors).get(random_numbers)


class RandomTransitionMatrixProviderRegistry:

    def __init__(self):
        self.number_of_next_sensors_provider_registry = CountProviderRegistry()

    def get(self, type: str, args) -> RandomTransitionMatrixCreationStrategy:
        registry = dict()
        registry["random"] = lambda config: (
            RandomTransitionMatrixCreationStrategy(
                probability_distribution=
                # TODO here: dafür brauchen wir ne registry
                DistinctProbabilityDistributionProvider(
                    number_of_next_state_provider=
                    self.number_of_next_sensors_provider_registry.get(
                        config["numberOfTransitions"]
                    )
                )
            )
        )
        return registry[type](args)
