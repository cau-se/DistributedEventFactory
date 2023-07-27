from datetime import datetime, timedelta
from typing import List
from uuid import uuid4
import random as rd
from behavior_modifier.modifier_list import BaseBehaviorModifier
from network.node_data_processor import NodeDataProcessor
from sensors.sensors import SensorManager
from utils.markov_chain import MarkovChain
from utils.utils_types import SensorLog


class MarkovChainNodeDataProcessor(NodeDataProcessor):

    def __init__(self, node_id: int, sensor_manager: SensorManager, transition_matrix: List[List[float]] = None,
                 duration_matrix: List[List[float | tuple[float, float]]] = None):
        super().__init__()
        self.node_id = node_id

        self.sensors_names: List[str] = sensor_manager.get_sensor_names()
        self.sensor_manager: SensorManager = sensor_manager

        self.markov_chain: MarkovChain = None

        if duration_matrix is None:
            duration_matrix = [[1.0 for _ in self.sensors_names] for _ in self.sensors_names]

        self.duration_matrix: List[List[float | tuple[float, float]]] = duration_matrix

        self.STARTING_SENSOR_INDEX: int = 0

        self.previous_time: datetime = datetime.now()
        self.transition_matrix = transition_matrix

    def init_cache_generation(self):
        self.init_markov_chain(self.sensors_names, self.transition_matrix)

    def init_markov_chain(self, sensors: List[str], transition_matrix: List[List[float]]):
        """
        This method takes in sensors and transition_matrix and creates a MarkovChain object
        which is assigned to the markov_chain property.
        :param sensors: List of the sensor_names (states)
        :param transition_matrix: The transition matrix
        :return:
        """
        self.markov_chain = MarkovChain(sensors, transition_matrix)

    def generate_cache(self, cache_length: int) -> List[SensorLog]:
        """
        This method uses the markov_chain object to simulate a sequence of
        sensor states and creates SensorLog objects for each state.
        These objects are appended to the sensor_log_cache property.
        :return:
        """
        execution_list = self.markov_chain.simulate(
            current_state=self.STARTING_SENSOR_INDEX,
            num_steps=cache_length
        )

        uuid = str(uuid4())[:8]
        previous_state = self.STARTING_SENSOR_INDEX

        i: int = 0
        sensor_log_cache: List[SensorLog] = []

        for state in execution_list:

            if state == self.sensors_names[self.STARTING_SENSOR_INDEX]:
                # New Case
                uuid = str(uuid4())[:8]
                i = 0
                previous_state = self.STARTING_SENSOR_INDEX

            duration = self.duration_matrix[previous_state][self.sensors_names.index(state)]

            if isinstance(duration, tuple):
                duration = rd.uniform(duration[0], duration[1])

            self.previous_time = self.previous_time + timedelta(minutes=duration)
            timestamp = self.previous_time

            sensor = self.sensor_manager.get_sensor(state)
            sensor_generator = sensor.get_data()
            sensor_value = next(sensor_generator)

            sensor_log = SensorLog(
                sensor_value=sensor_value,
                case_id=f"{uuid}_{i}",
                timestamp=timestamp,
                sensor_name=state,
                status="valid",
                generated_by=f"NODE: {self.node_id}"
            )

            sensor_log_cache.append(sensor_log)
            previous_state = self.sensors_names.index(state)
            previous_timestamp = timestamp
            i += 1

        return sensor_log_cache

    def visualize_markov_chain(self):
        self.markov_chain.visualize()
