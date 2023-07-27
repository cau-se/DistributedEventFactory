from network.cluster import Cluster
from network.markov_chain_node_data_processor import MarkovChainNodeDataProcessor
from network.websocket_node_data_processor import WebsocketNodeDataProcessor
from network.node import Node
from tests.scenarios.weather_scenario import WEATHER_SENSOR_MANAGER, WEATHER_TRANSITION_MATRIX

ws_node_data_processor = WebsocketNodeDataProcessor("ws://localhost:8080")
ws_node = Node(node_id=1, cache_length=10, node_data_processor=ws_node_data_processor)

data_processor: MarkovChainNodeDataProcessor = \
    MarkovChainNodeDataProcessor(
        9999,
        sensor_manager=WEATHER_SENSOR_MANAGER,
        transition_matrix=WEATHER_TRANSITION_MATRIX,
    )

mc_node = Node(9999, data_processor, cache_length=300)

cluster: Cluster = Cluster([ws_node, mc_node])
cluster.start("localhost:8081", tick_speed=0.5)
