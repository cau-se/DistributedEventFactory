from datetime import datetime, timedelta
from typing import Callable, List
from uuid import uuid4
import random as rd
from behavior_modifier.modifier_list import BaseBehaviorModifier
from network.node_data_processor import NodeDataProcessor
from sensors.sensors import SensorManager
from utils.markov_chain import MarkovChain
from utils.utils_types import SensorLog


class Node:

    def __init__(self,
                 node_id: int,
                 node_data_processor: NodeDataProcessor,
                 cache_length: int = 100
                 ):

        self.id: int = node_id
        self.node_data_processor = node_data_processor

        self.data: SensorLog = None

        self.sensor_log_cache: List[SensorLog] = []
        self.behavior_modifiers_list: List[BaseBehaviorModifier] = []

        self.current_cache_index: int = 0
        self.CACHE_LENGTH: int = cache_length

        self.refresh_data()

    def refresh_data(self) -> None:
        """
        This method updates the data property with the next sensor log in the cache.
        """
        if self.current_cache_index == len(self.sensor_log_cache):
            self.reset_cache_and_apply_modifiers()

        current_data: SensorLog = self.sensor_log_cache[self.current_cache_index]
        self.data = current_data
        self.current_cache_index += 1

    def add_behavior_modifier(self, modifier: BaseBehaviorModifier) -> None:
        """
        This method takes in a modifier object and adds it to the behavior_modifiers_list property.
        :param modifier: Instance of the BaseBehaviorModifier
        :return: None
        """
        self.behavior_modifiers_list.append(modifier)

    def reset_cache_and_apply_modifiers(self):
        """
        This method clears the sensor_log_cache and calls
        simulate_and_process_results method and applies all the behavior modifiers on the sensor log cache.
        :return:
        """
        self.sensor_log_cache.clear()
        self.current_cache_index = 0
        self.sensor_log_cache = self.node_data_processor.generate_cache(self.CACHE_LENGTH)

        for modifier in self.behavior_modifiers_list:
            self.sensor_log_cache = modifier.mutate_cache(self.sensor_log_cache)

    def get_filtered_sensor_cache(self, filter_func: Callable[[SensorLog], List[SensorLog]]) -> List[SensorLog]:
        """
        Returns a filtered list of SensorLog objects from the sensor log cache.

        :param filter_func: A callable that takes a SensorLog object
                            and returns a boolean value indicating whether
                            to include the object in the filtered list.
        :type filter_func: Callable[[SensorLog], bool]

        :return: A list of SensorLog objects that meet the criteria of the filter function.
        :rtype: List[SensorLog]
        """
        return list(filter(filter_func, self.sensor_log_cache))

    def __str__(self) -> str:
        """
        Returns a string representation of the Node object
        :return: name of the node
        """
        return f"NODE: {self.id}"

    def __len__(self) -> int:
        """
        Returns the current length of the sensor_log_cache property
        :return: current position in cache
        """
        return self.current_cache_index
