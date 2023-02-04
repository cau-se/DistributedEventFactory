from typing import List, Callable, Any

from behavior_modifier.modifier_list import OutlierBehaviorModifier, NoiseBehaviorModifier, RandomizeBehaviorModifier
from network.network_protocol_factory import NetworkProtocolFactory, BaseNetworkProtocol
from network.network_protocols import WebSocket, WebRTC, ServerSentEvent
from network.producer import Node, Cluster
from sensors.sensor_collection import WifiSensor, SingleValueSensor
from sensors.sensors import SensorManager
from utils.utils_types import SensorLog, OutlierCategory
import random as rd

factory = NetworkProtocolFactory()
factory.register_protocol('websocket', WebSocket)
# factory.register_protocol('sse', ServerSentEvent)
# factory.register_protocol('webrtc', WebRTC)

network: BaseNetworkProtocol = factory.create_protocol('websocket')
# network: BaseNetworkProtocol = factory.create_protocol('sse')
# network: BaseNetworkProtocol = factory.create_protocol('webrtc')


sensor_manager: SensorManager = SensorManager()
sensor_manager.add_sensor(SingleValueSensor(["Door Open"], "DOOR_SENSOR"))
sensor_manager.add_sensor(WifiSensor("WIFI_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["PRODUCE_AISLE"], "PRODUCE_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["MEAT_AISLE"], "MEAT_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["BAKERY_AISLE"], "BAKERY_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["DAIRY_AISLE"], "DAIRY_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["FROZEN_FOOD_AISLE"], "FROZEN_FOOD_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["CHECKOUT"], "CHECKOUT_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["CREDIT_CARD"], "CREDIT_CARD_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["EXIT"], "EXIT_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["CASH"], "CASH_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["SELF_CHECKOUT"], "SELF_CHECKOUT_SENSOR"))

sensor_names: List[str] = sensor_manager.get_sensor_names()

transition_matrix: List[List[float]] = [
    [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # DOOR_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.00, 0.00, 0.10],  # WIFI_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.00, 0.10, 0.00],  # PRODUCE_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.10, 0.00, 0.00],  # MEAT_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.10, 0.00, 0.00, 0.00],  # BAKERY_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.10, 0.00, 0.00, 0.00, 0.00],  # DAIRY_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.05, 0.00, 0.05],  # FROZEN_FOOD_AISLE_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],  # CHECKOUT_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.00, 0.00, 0.00, 0.90, 0.00, 0.00],  # CREDIT_CARD_SENSOR
    [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # EXIT_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00],  # CASH_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00]   # SELF_CHECKOUT_SENSOR
]

nodes: List[Node] = [
    Node(
        i, sensor_manager=sensor_manager, transition_matrix=transition_matrix
    ) for i in range(5)
]

nodes[0].add_behavior_modifier(OutlierBehaviorModifier(type=OutlierCategory.COLLECTIVE_OUTLIERS, frequency=0.1))
nodes[0].add_behavior_modifier(NoiseBehaviorModifier(frequency=0.3))

nodes[1].add_behavior_modifier(NoiseBehaviorModifier(frequency=0.1))
nodes[2].add_behavior_modifier(RandomizeBehaviorModifier())

node_join_function: Callable[[List[SensorLog]], SensorLog] = lambda data: rd.choice(data)

cluster: Cluster = Cluster(nodes, node_join_function)

network.run("localhost:8000", cluster=cluster)
