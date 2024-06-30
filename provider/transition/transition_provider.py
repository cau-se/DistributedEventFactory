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


class TransitionProvider:

    @abstractmethod
    def get_transition(self) -> Transition:
        pass


class AbstractTransitionProvider(TransitionProvider):
    def __init__(self, duration_provider, next_state_provider, transition_probability_provider, transition_count_provider, possible_transitions):
        self.duration_provider: DurationProvider = duration_provider
        self.next_state_provider: NextStateProvider = next_state_provider
        self.transition_probability_provider: TransitionProbabilityProvider = transition_probability_provider
        self.transition_count_provider: CountProvider = transition_count_provider
        self.possible_transitions = possible_transitions

    def get_transition(self) -> Transition:
        transitions = []
        next_states: List[str] = self.next_state_provider.get_next_states(
            self.possible_transitions,
            self.transition_count_provider.get(max=len(self.possible_transitions) - 1))
        probabilities = self.transition_probability_provider.get_transition_probabilities(len(next_states))

        for next_state, probability in zip(next_states, probabilities):
            transitions.append(Transition(next_state, probability, self.duration_provider))

        # TODO here
        return transitions[0]
