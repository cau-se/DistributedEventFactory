import json
from typing import List, Callable, Any, Type

from network.event_sender import EventSender
from network.network_protocol_factory import BaseNetworkProtocol, NetworkProtocolFactory
from network.network_protocols import WebSocket
from network.network_protocols import Kafka
from network.node import Node
from provider.data.data_provider import NodeDataProvider, DataProvider
from provider.load.load_provider import GradualIncreasingLoadProvider, LoadProvider
from provider.sender.sender_provider import PrintConsole, SenderProvider
from utils.utils_types import GeneratedEvent


class Cluster:
    """
    The Cluster class is a representation of a cluster of nodes in a sensor network.
    It has a single property, join_function, which is a callable function that takes in a list of SensorLog objects and
    returns a single SensorLog object. It also has a single method, __init__,
    which takes in a list of Node objects and initializes a new Cluster object.
    """
    def __init__(
            self,
            nodes: List[Node],
            join_function: Callable[[List[GeneratedEvent]], GeneratedEvent] = None,
            protocolName='websocket',
            sender_provider: SenderProvider = None,
            data_provider: DataProvider =None,
            load_provider: LoadProvider =None
    ):
        self.nodes: List[Node] = nodes

        node_errors = self.validate_nodes()
        if len(node_errors) > 0:
            raise Exception(node_errors)

        self.join_function: Callable[[List[GeneratedEvent]], GeneratedEvent] = join_function

        self.network_factory = NetworkProtocolFactory()
        # create default network protocol
        self.network_factory.register_protocol('kafka', Kafka)
        self.network_factory.register_protocol('websocket', WebSocket)
        self.network: BaseNetworkProtocol = self.network_factory.create_protocol(protocolName)
        self.sender_provider = sender_provider,
        self.data_provider = data_provider,
        self.load_provider = load_provider

    def register_network_protocol(self, network_name: str, protocol: Type[BaseNetworkProtocol], use_protocol=True):
        self.network_factory.register_protocol(network_name, protocol)

        if use_protocol:
            self.network = self.network_factory.create_protocol(network_name)

    def start(self):
        """
        Start the cluster on a given url
        :param url:
        :param tick_speed:
        :return:
        """
        sender = EventSender()
        sender.run(
            sender_provider=PrintConsole(),
            data_provider=NodeDataProvider(nodes=self.nodes, join_function=self.join_function),
            load_provider=GradualIncreasingLoadProvider(
                tick_count_til_maximum_reached=60,
                minimal_load=0,
                maximal_load=100
            )
        )


    def get_data(self) -> GeneratedEvent:
        """
        This Function gets called in every tick and returns the current data from the selected node
        :return: the stringify version of the dataclass[SensorLog]
        """
        # refresh the data in every node
        for node in self.nodes:
            node.refresh_data()

        if self.join_function is not None:
            data: GeneratedEvent = self.join_function([node.data for node in self.nodes if node.data])
            data.timestamp = str(data.timestamp)
            return data

    def validate_nodes(self) -> List[Exception]:
        """
        Check if the nodes are valid
        :return:
        """
        error_list: List[Exception] = []
        if len(self.nodes) > len(set([node.id for node in self.nodes])):
            error_list.append(Exception("All nodes must have a unique id"))

        return error_list
