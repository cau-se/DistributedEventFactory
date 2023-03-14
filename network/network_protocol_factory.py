from abc import ABC, abstractmethod
from typing import Type, Dict, Callable


class BaseNetworkProtocol(ABC):
    """
    A class for handling network protocol connections.
    """

    @abstractmethod
    def run(self, url: str, data_function: Callable[[None], str], tick_sleep: float) -> None:
        """
        Send data over the connection.
        :param url: Url od the application.
        :param data_function: this function returns the data for the network. Normally cluster.get_data()
        :param tick_sleep: time between the network ticks
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
