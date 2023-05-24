from typing import List, Callable, Any

from behavior_modifier.modifier_list import OutlierBehaviorModifier
from network.markov_chain_node_data_processor import MarkovChainNodeDataProcessor
from network.cluster import Node, Cluster
from tests.supermarket_scenario import SUPERMARKET_BUILDER, SUPERMARKET_SENSOR_MANAGER
from utils.utils_types import SensorLog, OutlierCategory
import random as rd

nodes: List[Node] = []

for i in range(5):
    data_processor: MarkovChainNodeDataProcessor = MarkovChainNodeDataProcessor(
        i,
        sensor_manager=SUPERMARKET_SENSOR_MANAGER,
        transition_matrix=SUPERMARKET_BUILDER.to_transition_matrix(),
        duration_matrix=SUPERMARKET_BUILDER.to_duration_matrix()
    )

    # data_processor= WebsocketNodeDataProcessor("ws:localhost:8001")

    node = Node(i, data_processor, cache_length=300)

    if i < 2:
        node.add_behavior_modifier(
            OutlierBehaviorModifier(OutlierCategory.GLOBAL_OUTLIERS, 0.1)
        )

    nodes.append(node)
nodes[0].node_data_processor.visualize_markov_chain()

# nodes[0].add_behavior_modifier(OutlierBehaviorModifier(OutlierCategory.GLOBAL_OUTLIERS, 0.3))


def node_join_function(data: List[SensorLog]) -> SensorLog:
    return rd.choice(data)


cluster: Cluster = Cluster(nodes)
cluster.start("localhost:8080", tick_speed=0.5)
