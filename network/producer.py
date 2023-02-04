import asyncio
import json
from datetime import datetime, timedelta
import random as rd
from typing import List, Callable, Any
from uuid import uuid4

from behavior_modifier.modifier_list import BaseBehaviorModifier
from sensors.sensors import SensorManager
from utils.markov_chain import MarkovChain
from utils.utils_types import SensorLog


class Node:
    """
    The Node class is a representation of a node in a simulation of a sensor network.
    It has several properties,
    including data (of type SensorLog),
    id (an integer),
    markov_chain (of type MarkovChain),
    sensor_log_cache (a list of SensorLog objects),
    sensors_names (a list of strings),
    sensor_manager (of type SensorManager)
    """

    def __init__(self,
                 node_id: int,
                 sensor_manager: SensorManager,
                 transition_matrix: List[List[float]] = None,
                 duration_matrix: List[List[float | tuple[float, float]]] = None
                 ):
        """
        Initializes a new Node object.
        :param node_id: The id of the node
        :param sensors_names: List of the Sensor Names, Corresponding to the Sensor Manager
        :param sensor_manager: Instance of SensorManager
        :param transition_matrix: initialize the markov_chain
        """

        self.sensors_names: List[str] = sensor_manager.get_sensor_names()
        self.sensor_manager: SensorManager = sensor_manager

        self.id: int = node_id

        self.data: SensorLog = None
        self.markov_chain: MarkovChain = None

        if duration_matrix is None:
            duration_matrix = [[1.0 for _ in self.sensors_names] for _ in self.sensors_names]

        self.duration_matrix: List[List[float | tuple[float, float]]] = duration_matrix

        self.sensor_log_cache: List[SensorLog] = []
        self.behavior_modifiers_list: List[BaseBehaviorModifier] = []

        self.current_cache_index: int = 0
        self.STARTING_SENSOR_INDEX: int = 0
        self.CACHE_LENGTH: int = 100

        self.init_markov_chain(self.sensors_names, transition_matrix)
        self.reset_cache_and_apply_modifiers()

    def init_markov_chain(self, sensors: List[str], transition_matrix: List[List[float]]):
        """
        This method takes in sensors and transition_matrix and creates a MarkovChain object
        which is assigned to the markov_chain property.
        :param sensors: List of the sensor_names (states)
        :param transition_matrix: The transition matrix
        :return:
        """
        self.markov_chain = MarkovChain(sensors, transition_matrix)

    def simulate_and_process_results(self) -> None:
        """
        This method uses the markov_chain object to simulate a sequence of
        sensor states and creates SensorLog objects for each state.
        These objects are appended to the sensor_log_cache property.
        :return:
        """
        execution_list = self.markov_chain.simulate(
            current_state=self.STARTING_SENSOR_INDEX,
            num_steps=self.CACHE_LENGTH
        )

        uuid = str(uuid4())[:8]
        previous_state = self.STARTING_SENSOR_INDEX
        previous_timestamp = datetime.now()
        i = 0
        for state in execution_list:
            if state == self.sensors_names[self.STARTING_SENSOR_INDEX]:
                uuid = str(uuid4())[:8]
                i = 0
                previous_state = self.STARTING_SENSOR_INDEX
                previous_timestamp = datetime.now()

            duration = self.duration_matrix[previous_state][self.sensors_names.index(state)]

            if isinstance(duration, tuple):
                duration = rd.uniform(duration[0], duration[1])
            timestamp = previous_timestamp + timedelta(minutes=duration)

            sensor = self.sensor_manager.get_sensor(state)
            sensor_generator = sensor.get_data()
            sensor_value = next(sensor_generator)

            sensor_log = SensorLog(
                sensor_value=sensor_value,
                case_id=f"{uuid}_{i}",
                timestamp=timestamp,
                sensor_name=state,
                status="valid",
                generated_by=f"NODE: {self.id}"
            )

            self.sensor_log_cache.append(sensor_log)
            previous_state = self.sensors_names.index(state)
            previous_timestamp = timestamp
            i += 1

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
        self.simulate_and_process_results()

        for modifier in self.behavior_modifiers_list:
            self.sensor_log_cache = modifier.mutate_cache(self.sensor_log_cache)

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

    def visualize_markov_chain(self):
        self.markov_chain.visualize()


class Cluster:
    """
    The Cluster class is a representation of a cluster of nodes in a sensor network.
    It has a single property, join_function, which is a callable function that takes in a list of SensorLog objects and
    returns a single SensorLog object. It also has a single method, __init__,
    which takes in a list of Node objects and initializes a new Cluster object.
    """

    def __init__(self, nodes: List[Node], join_function: Callable[[List[SensorLog]], SensorLog]):
        self.nodes: List[Node] = nodes
        self.join_function: Callable[[List[SensorLog]], SensorLog] = join_function

    def get_data(self) -> str:
        """
        This Function gets called in every tick and returns the current data from the selected node
        :return: the stringify version of the dataclass[SensorLog]
        """
        # refresh the data in every node
        for node in self.nodes:
            node.refresh_data()

        data: SensorLog = self.join_function([node.data for node in self.nodes])
        data.timestamp = str(data.timestamp)
        return json.dumps(data.__dict__)
