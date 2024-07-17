import abc
from abc import abstractmethod
import random
from typing import List


class TransitionProbabilityProvider:

    @abstractmethod
    def get_transition_probabilities(self):
        pass




class MatrixBasedTransitionProvider(TransitionProbabilityProvider):

    def __init__(self, transition_matrix: List[List[float]]):
        self.transition_matrix = transition_matrix
        self.transition_iterator = iter(transition_matrix)

    def get_transition_probabilities(self) -> List[float]:
        return next(self.transition_iterator)


class TransitionProbabilityProviderFactory(abc.ABC):

    @abc.abstractmethod
    def get(self, number_of_sensors):
        pass


class DrawWithoutReplacementTransitionProbabilityProviderFactory(TransitionProbabilityProviderFactory):

    def __init__(self, transition_indices_provider):
        self.transition_indices_provider = transition_indices_provider

    def get(self, number_of_sensors):
        return DrawWithoutReplacementTransitionProvider(number_of_sensors, self.transition_indices_provider)
