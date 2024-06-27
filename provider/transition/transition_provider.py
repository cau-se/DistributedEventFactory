from abc import abstractmethod

from dataclasses import dataclass
from typing import List

from provider.generic.count_provider import CountProvider
from provider.transition.duration_provider import DurationProvider
from provider.transition.next_state_provider import NextStateProvider
from provider.transition.transition_probability_provider import TransitionProbabilityProvider


@dataclass
class Transition:
    next_state: str
    probability: float
    duration: DurationProvider


class TransitionProvider:

    @abstractmethod
    def get_transition(self, possible_transitions) -> List[Transition]:
        pass


class AbstractTransitionProvider(TransitionProvider):
    def __init__(self, duration_provider, next_state_provider, transition_probability_provider, transition_count_provider):
        self.duration_provider: DurationProvider = duration_provider
        self.next_state_provider: NextStateProvider = next_state_provider
        self.transition_probability_provider: TransitionProbabilityProvider = transition_probability_provider
        self.transition_count_provider: CountProvider = transition_count_provider

    def get_transition(self, possible_transitions) -> List[Transition]:
        transitions = []
        next_states: List[str] = self.next_state_provider.get_next_states(
            possible_transitions,
            self.transition_count_provider.get(max=len(possible_transitions) - 1))
        probabilities = self.transition_probability_provider.get_transition_probabilities(len(next_states))

        for next_state, probability in zip(next_states, probabilities):
            transitions.append(Transition(next_state, probability, self.duration_provider))

        return transitions
