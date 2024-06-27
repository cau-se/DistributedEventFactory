import copy
from abc import ABC, abstractmethod
from typing import List
from random import shuffle, randint, random, sample
from utils.utils_types import GeneratedEvent, fisher_yates_shuffle


class BaseBehaviorModifier(ABC):
    @abstractmethod
    def mutate_cache(self, cache: List[GeneratedEvent]) -> List[GeneratedEvent]:
        """
        This method gets called if the node generate a new set
        of sensor logs (the old cache is empty),

        The Node will iterate over all behavior modifier and replace the cache with the
        return value of this function.
        :param cache:
        :return:
        """


class NoiseBehaviorModifier(BaseBehaviorModifier):
    def __init__(self, frequency: float, change_value: float):
        self.frequency = frequency
        self.change_value = change_value

    def mutate_cache(self, cache: List[GeneratedEvent]) -> List[GeneratedEvent]:
        return self.add_noise(cache)

    def add_noise(self, lst: List[GeneratedEvent]):
        """
        Adds noise to a list of SensorLog.

        :param
            lst (list): A list of SensorLog.
            frequency (float): The percentage of elements to add noise to.
            change_value (float): a possibility that the SensorValue is changed

        Returns:
            list: The modified list with added noise.

        """
        num_noise_elements: int = int(len(lst) * self.frequency)

        indices: List[int] = sample(range(len(lst)), num_noise_elements)

        # Copy and insert the selected elements after their original position
        for j in sorted(indices, reverse=True):
            lst[j].status = "NOISE"
            if random() >= self.change_value:
                selected = lst[j].sensor_value
                sensor_value_list = fisher_yates_shuffle(list(selected), int((len(selected) / 2) - 1),
                                                         int(len(selected) - 1))
                new_sensor_value = ''.join(sensor_value_list)
                lst[j].sensor_value = new_sensor_value
                lst[j].status = "NOISE_WITH_VALUE_ERROR"

            lst.insert(j + 1, copy.deepcopy(lst[j]))
        return lst

class OutlierBehaviorModifier(BaseBehaviorModifier):
    def __init__(self, type: str, frequency: float):
        self.frequency = frequency
        self.type = type

    def mutate_cache(self, cache: List[GeneratedEvent]) -> List[GeneratedEvent]:
        return cache


class RandomizeBehaviorModifier(BaseBehaviorModifier):

    def mutate_cache(self, cache: List[GeneratedEvent]) -> List[GeneratedEvent]:
        return fisher_yates_shuffle(cache, self.frequency)




class OutlierGeneratorModifier(BaseBehaviorModifier):
    def mutate_cache(self, cache: List[GeneratedEvent]) -> List[GeneratedEvent]:
        return cache
