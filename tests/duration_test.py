from typing import List, Callable, Any

from behavior_modifier.modifier_list import OutlierBehaviorModifier
from network.markov_chain_node_data_processor import MarkovChainNodeDataProcessor
from network.cluster import Node, Cluster
from tests.supermarket_scenario import SUPERMARKET_BUILDER, SUPERMARKET_SENSOR_MANAGER
from utils.utils_types import SensorLog, OutlierCategory
import random as rd

data_processor: MarkovChainNodeDataProcessor = MarkovChainNodeDataProcessor(
    1,
    sensor_manager=SUPERMARKET_SENSOR_MANAGER,
    transition_matrix=SUPERMARKET_BUILDER.to_transition_matrix(),
    duration_matrix=SUPERMARKET_BUILDER.to_duration_matrix()
)

node = Node(1, data_processor, cache_length=300)

for log in node.sensor_log_cache:
    print(log.sensor_value, log.timestamp.isoformat())


def get_data():
    while True:
        mac_address = ':'.join(['{:02x}'.format(rd.randint(0, 255)) for _ in range(6)])
        signal_strength = rd.randint(-100, -30)
        yield mac_address, signal_strength


print(next(get_data()))
