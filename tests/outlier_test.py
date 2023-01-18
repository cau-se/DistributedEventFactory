from typing import List
from behavior_modifier.outlier_autoencoder import OutlierDetectorAutoencoder
from behavior_modifier.outlier_statistic import OutlierDetector
from network.producer import Node
from sensors.sensor_collection import WifiSensor, SingleValueSensor
from sensors.sensors import SensorManager

sensor_manager: SensorManager = SensorManager()
sensor_manager.add_sensor(WifiSensor("WifiSensor_A"))
sensor_manager.add_sensor(WifiSensor("WifiSensor_B"))
sensor_manager.add_sensor(SingleValueSensor(["A1", "A2", "A3", "A4"], "SingularValue_A"))
sensor_manager.add_sensor(SingleValueSensor(["B1", "B2", "B3", "B4"], "SingularValue_B"))

sensor_names: List[str] = sensor_manager.get_sensor_names()

transition_matrix: List[List[float]] = [
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25],
    [0.25, 0.25, 0.25, 0.25]
]

node0: Node = Node(1, sensors_names=sensor_names, sensor_manager=sensor_manager, transition_matrix=transition_matrix)
node1: Node = Node(2, sensors_names=sensor_names, sensor_manager=sensor_manager, transition_matrix=transition_matrix)
node2: Node = Node(3, sensors_names=sensor_names, sensor_manager=sensor_manager, transition_matrix=transition_matrix)
node3: Node = Node(4, sensors_names=sensor_names, sensor_manager=sensor_manager, transition_matrix=transition_matrix)
node4: Node = Node(5, sensors_names=sensor_names, sensor_manager=sensor_manager, transition_matrix=transition_matrix)

nodes = [node0, node1, node2, node3, node4]

for node in nodes:
    node.refresh_data()
    print(node.id, str(node), node.data.debug)