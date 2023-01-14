import asyncio
import json
from datetime import datetime
import random as rd
from typing import List, Callable, Any
from uuid import uuid4

from utils.markov_chain import MarkovChain
from utils.types import SensorLog


class Node:
    data: SensorLog
    id: int
    markov_chain: MarkovChain
    sensor_log_cache: List[SensorLog]
    sensors_names: List[str]

    STARTING_SENSOR_INDEX: int = 0
    CACHE_LENGTH: int = 100

    def __init__(self, id: int, sensors_names: List[str], transition_matrix: List[List[float]]):
        self.id = id
        self.sensors_names = sensors_names
        if not transition_matrix:
            transition_matrix = self.fill_transition_matrix_if_empty(len(sensors_names))

        self.init_markov_chain(sensors_names, transition_matrix)
        self.refresh_data()

    def fill_transition_matrix_if_empty(self, length: int) -> List[List[float]]:
        return [[ 1 / length for _ in range(length)] for _ in range(length)]


    def init_markov_chain(self,sensors: List[str], transition_matrix: List[List[float]]):
        self.markov_chain = MarkovChain(transition_matrix, sensors)

    def simulate_and_process_results(self):

        execution_list: List[str] = self.markov_chain.simulate(
            current_state=self.STARTING_SENSOR_INDEX,
            num_steps=self.CACHE_LENGTH)

        i = 0
        sensor_logs: list[dict] = []
        uuid = str(uuid4())[:8]
        date_now = datetime.datetime.now()

        for state in execution_list:

            if state == self.sensors_names[self.STARTING_SENSOR_INDEX]:
                i = 0
                uuid = str(uuid4())[:8]

            sensor_log: SensorLog = SensorLog(
                sensor_value=next(sensors_names[states.index(state)]),
                case_id=f"{uuid}_{i}",
                timestamp=date_now,
                sensor_type=state,
                status="valid"
            )
            self.sensor_log_cache.append(sensor_log)
            i = i + 1

    def refresh_data(self):
        self.data = SensorLog(
            sensor_value= str(uuid4())[:8],
            case_id=f"{str(uuid4())[:8]}_{self.id}",
            timestamp= str(datetime.now()),
            sensor_type="Valid",
            status="valid"
        )

class Cluster:
    data: List[SensorLog]
    def __init__(self, nodes: List[Node], join_function: Callable[ [ List[SensorLog] ] , Any]):
        self.nodes = nodes
        self.join_function = join_function

    def get_data(self) -> str:
        for node in self.nodes:
            node.refresh_data()
        self.data = self.join_function([node.data for node in self.nodes])
        return json.dumps(rd.choice(self.data).__dict__)