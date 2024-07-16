from abc import abstractmethod
import random

from provider.transition.next_state_provider import NextStateProvider


class TransitionProbabilityProvider:

    @abstractmethod
    def get_transition_probabilities(self):
        pass


class DrawWithoutReplacementTransitionProvider(TransitionProbabilityProvider):

    def __init__(self, transition_array_length, transition_indices):
        self.transition_array_length = transition_array_length
        self.transition_indices_provider = transition_indices

    def get_transition_probabilities(self):
        transition_indices = self.transition_indices_provider.get_next_states(self.transition_array_length)
        random_numbers = [0.0] * self.transition_array_length
        remaining_prob = 1.0
        for i in range(len(transition_indices) - 1):
            random_value = round(random.random() * remaining_prob, 2)
            remaining_prob -= random_value
            # TODO here: Das hat zur Folge, dass die Transitionen geordnet sind, hier müsste konsequenterweise ein zufälliger Index genommen werden,
            # Das Verhalten darf aber auch auf einer höhren Ebene umgesetzt werden
            random_numbers[transition_indices[i]] = random_value

        if remaining_prob > 0:
            random_numbers[transition_indices[len(transition_indices) - 1]] = round(remaining_prob, 2)
        return random_numbers
