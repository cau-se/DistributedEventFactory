from abc import ABC, abstractmethod

from provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, NextSensorChooseProvider
from provider.transition.transition_matrix_creation_strategy import RandomTransitionMatrixCreationStrategy, \
    RandomTransitionMatrixProviderRegistry


class TransitionProvider(ABC):
    @abstractmethod
    def get(self, number_of_sensors) -> NextSensorProvider:
        pass


class TransitionProviderRegistry:
    def __init__(self):
        self.randomTransitionMatrixProviderRegistry = RandomTransitionMatrixProviderRegistry()

    def get(self, type: str, args) -> TransitionProvider:
        registry = dict()
        registry["matrix"] = lambda config: MatrixBasedTransitionProvider(config["matrix"])
        registry["generateMatrix"] = lambda config: (
            GenerativeTransitionProvider(provider=
                self.randomTransitionMatrixProviderRegistry.get(
                    config["strategy"]["type"],
                    config["strategy"]["args"]
                )
            )
        )
        return registry[type](args)


class GenerativeTransitionProvider(TransitionProvider):
    def __init__(self, provider: RandomTransitionMatrixCreationStrategy):
        self.provider = provider

    def get(self, number_of_sensors):
        return self.provider.next(number_of_sensors)


class MatrixBasedTransitionProvider(TransitionProvider):
    def __init__(self, matrix):
        self.probability_distribution_iterator = iter(matrix)

    def get(self, number_of_sensors):
        return NextSensorChooseProvider(number_of_sensors).get(
            next(self.probability_distribution_iterator))
