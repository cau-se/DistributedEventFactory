from abc import abstractmethod
import random
from typing import List


class ProbabilityDistributionProvider:

    @abstractmethod
    def get_next_states(self, number_of_data_sources) -> List[int]:
        pass


def get_random_distinct(max_length, count) -> List[int]:
    random_elements: List[int] = []
    if count > max_length:
        raise ValueError("Count must be smaller than array length")
    while len(random_elements) < count:
        next_element = int(random.uniform(0, max_length))
        if next_element not in random_elements:
            random_elements.append(next_element)
    return random_elements


class DistinctProbabilityDistributionProvider(ProbabilityDistributionProvider):
    def __init__(self, number_of_next_state_provider):
        self.number_of_next_state_provider = number_of_next_state_provider

    def get_next_states(self, possible_next_state) -> List[int]:
        number_of_next_state = self.number_of_next_state_provider.get()
        return get_random_distinct(possible_next_state, number_of_next_state)
