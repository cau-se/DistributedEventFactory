from abc import abstractmethod
import random
from typing import List


class NextStateProvider:

    @abstractmethod
    def get_next_states(self, possible_next_state, number_of_next_states) -> List[str]:
        pass


def get_random_distinct(array, count) -> List[str]:
    random_elements: List[str] = []
    if count > len(array):
        raise ValueError("Count must be smaller than array length")
    while len(random_elements) < count:
        next_element = array[int(random.uniform(0, len(array)))]
        if next_element not in random_elements:
            random_elements.append(next_element)
    return random_elements


class DistinctNextStateProvider(NextStateProvider):

    def get_next_states(self, possible_next_state, number_of_next_states) -> List[str]:
        return get_random_distinct(possible_next_state, number_of_next_states)


class NonLoopNextStateProvider(NextStateProvider):

    def get_next_states(self, possible_next_state, number_of_next_states) -> List[str]:
        raise NotImplementedError