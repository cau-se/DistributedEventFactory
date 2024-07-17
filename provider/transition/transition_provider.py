from abc import ABC, abstractmethod
from typing import List

import numpy as np
from provider.transition.transition_probability_provider import TransitionProbabilityProviderFactory

class TransitionProvider(ABC):

    @abstractmethod
    def get_next_sensor(self) -> int:
        pass




class TransitionProviderFactory:

    @abstractmethod
    def get(self, number_of_sensors):
        pass


class UniformTransitionProviderFactory(TransitionProviderFactory):

    def __init__(self, next_sensor_probabilities_provider_factory: TransitionProbabilityProviderFactory):
        self.next_sensor_probabilities_provider_factory = next_sensor_probabilities_provider_factory

    def get(self, number_of_sensors):
        return UniformTransitionProvider(
            next_sensor_probabilities=self.next_sensor_probabilities_provider_factory.get(number_of_sensors).get_transition_probabilities()
        )
