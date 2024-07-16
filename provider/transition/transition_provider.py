from abc import ABC, abstractmethod
import numpy as np
from provider.transition.transition_probability_provider import TransitionProbabilityProvider


class TransitionProvider(ABC):

    @abstractmethod
    def get_next_sensor(self) -> int:
        pass


class GenericTransitionProvider(TransitionProvider):

    def __init__(self, next_sensor_probabilities_provider: TransitionProbabilityProvider):
        self.next_sensor_probabilities_provider = next_sensor_probabilities_provider

    def get_next_sensor(self) -> int:
        next_sensor_probabilities = self.next_sensor_probabilities_provider.get_transition_probabilities()
        return np.random.choice(len(next_sensor_probabilities), p=np.array(next_sensor_probabilities))

