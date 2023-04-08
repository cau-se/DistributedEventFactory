import json
from typing import List, Callable, Any, Type

from network.network_protocol_factory import BaseNetworkProtocol, NetworkProtocolFactory
from network.network_protocols import WebSocket
from network.node import Node
from utils.utils_types import SensorLog


class Cluster:
    """
    The Cluster class is a representation of a cluster of nodes in a sensor network.
    It has a single property, join_function, which is a callable function that takes in a list of SensorLog objects and
    returns a single SensorLog object. It also has a single method, __init__,
    which takes in a list of Node objects and initializes a new Cluster object.
    """

    def __init__(self, nodes: List[Node], join_function: Callable[[List[SensorLog]], SensorLog] = None):
        self.nodes: List[Node] = nodes
        self.join_function: Callable[[List[SensorLog]], SensorLog] = join_function

        self.network_factory = NetworkProtocolFactory()
        self.network_factory.register_protocol('websocket', WebSocket)
        self.network: BaseNetworkProtocol = self.network_factory.create_protocol("websocket")

    def register_network_protocol(self, network_name: str, protocol: Type[BaseNetworkProtocol], use_protocol=True):
        self.network_factory.register_protocol(network_name, protocol)

        if use_protocol:
            self.network = self.network_factory.create_protocol(network_name)

    def start(self, url: str, tick_speed: float = 1):
        self.network.run(url, self.get_data, tick_speed)

    def get_data(self) -> str:
        """
        This Function gets called in every tick and returns the current data from the selected node
        :return: the stringify version of the dataclass[SensorLog]
        """
        # refresh the data in every node
        for node in self.nodes:
            node.refresh_data()

        if self.join_function is not None:
            data: SensorLog = self.join_function([node.data for node in self.nodes])
            data.timestamp = str(data.timestamp)
            return json.dumps(data.__dict__)
        else:
            nodes_data: List[SensorLog] = [node.data for node in self.nodes]
            for i in range(len(nodes_data)):
                nodes_data[i].timestamp = str(nodes_data[i].timestamp)
            return json.dumps([data.__dict__ for data in nodes_data])
