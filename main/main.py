from typing import List

from behavior_modifier.modifier_list import OutlierBehaviorModifier
from network.markov_chain_node_data_processor import MarkovChainNodeDataProcessor
from network.cluster import Node, Cluster
from tests.scenarios.supermarket_scenario import SUPERMARKET_BUILDER, SUPERMARKET_SENSOR_MANAGER
from utils.utils_types import GeneratedEvent, OutlierCategory
import random
import os

nodes: List[Node] = []

for i in range(50):
    data_processor: MarkovChainNodeDataProcessor = MarkovChainNodeDataProcessor(
        i,
        sensor_manager=SUPERMARKET_SENSOR_MANAGER,
        transition_matrix=SUPERMARKET_BUILDER.to_transition_matrix(),
        duration_matrix=SUPERMARKET_BUILDER.to_duration_matrix()
    )

    node = Node(i, data_processor, cache_length=300)

    if i < 2:
        node.add_behavior_modifier(
            OutlierBehaviorModifier(OutlierCategory.CONTEXTUAL_OUTLIERS, 0.1)
        )

    nodes.append(node)


def node_join_function(data: List[GeneratedEvent]) -> GeneratedEvent:
    return random.choice(data)


def start_load_generation(bootstrap_server_url, events_per_second, protocol_name):
    cluster: Cluster = Cluster(nodes, node_join_function, protocol_name)
    tick_speed = 1 / events_per_second
    cluster.start(bootstrap_server_url, tick_speed=tick_speed)


if __name__ == '__main__':
    bootstrap_server_url = os.environ['BOOTSTRAP_SERVER_URL']
    events_per_second = int(os.environ['EVENTS_PER_SECOND'])
    protocol_name = os.environ['PROTOCOL_NAME']


