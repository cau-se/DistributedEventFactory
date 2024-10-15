from abc import ABC, abstractmethod
import numpy

class TransitionProvider(ABC):
    @abstractmethod
    def get_transition(self):
        pass


class ChoiceTransitionProvider(TransitionProvider):

    def __init__(self, probability_distribution):
        self.probability_distribution = probability_distribution

    def get_transition(self) -> int:
        return numpy.random.choice(len(self.probability_distribution), p=numpy.array(self.probability_distribution))


class NextSensorChooseProvider:
    def __init__(self, number_of_data_sources):
        self.number_of_sensors = number_of_data_sources

    def get(self, probability_distribution) -> ChoiceTransitionProvider:
        distribution = probability_distribution[0:self.number_of_sensors - 1]
        remaining_probability = 1.0 - sum(distribution)
        distribution.append(remaining_probability)
        return ChoiceTransitionProvider(distribution)



