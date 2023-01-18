from abc import ABC, abstractmethod
from typing import Type, Dict

from network.producer import Cluster

class BaseNetworkProtocol(ABC):
    """
    A class for handling network protocol connections.
    """
    @abstractmethod
    def run(self, url: str, cluster: Cluster) -> None:
        """
        Send data over the connection.
        :param cluster:
        :param url: Url od the application.
        """

    @abstractmethod
    def handle_network(self) -> None:
        """
        Receive data from the connection.
        :return: The received data.
        """


class NetworkProtocolFactory:
    """
    A factory class for creating instances of different network protocols.
    """

    protocols: Dict[str, Type[BaseNetworkProtocol]]

    def __init__(self):
        self.protocols = {}

    def register_protocol(self, protocol_name: str, protocol_class: Type[BaseNetworkProtocol]):
        """
        Register a new protocol with the factory.
        :param protocol_name: The name of the protocol.
        :param protocol_class: The class of the protocol.
        """

        self.protocols[protocol_name] = protocol_class

    def create_protocol(self, protocol_name: str) -> BaseNetworkProtocol:
        """
        Create an instance of a protocol.
        :param protocol_name: The name of the protocol to create.
        :return: An instance of the specified protocol.
        :raises ValueError: If an invalid protocol name is passed.
        """

        protocol_class: Type[BaseNetworkProtocol] = self.protocols.get(protocol_name)
        if protocol_class is None:
            raise ValueError(f'Invalid protocol: {protocol_name}')
        return protocol_class()


