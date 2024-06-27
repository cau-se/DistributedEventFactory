from abc import abstractmethod
import random


class TransitionProbabilityProvider:

    @abstractmethod
    def get_transition_probabilities(self, number_of_transitions):
        pass


class DrawWithoutReplacementTransitionProvider(TransitionProbabilityProvider):

    def get_transition_probabilities(self, number_of_transitions):
        random_numbers = []
        remaining_prob = 1.0
        for i in range(number_of_transitions - 1):
            random_value = round(random.random() * remaining_prob, 2)
            remaining_prob -= random_value
            random_numbers.append(random_value)

        if remaining_prob > 0:
            random_numbers.append(round(remaining_prob, 2))

        return random_numbers
