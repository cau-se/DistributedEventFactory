import abc
import json

from kafka import KafkaProducer
from core.event import AbstractEvent
from view.terminal import Terminal


class Sink:

    @abc.abstractmethod
    def send(self, event: AbstractEvent) -> None:
        pass

class SinkProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sink:
        pass


class SinkProviderRegistry:

    def get(self, config) -> SinkProvider:
        registry = dict()
        registry["kafka"] = KafkaSinkProvider()
        registry["ui"] = TerminalGuiSinkProvider()
        registry["console"] = PrintConsoleSinkProvider()
        return registry[config]


class KafkaSink(Sink):

    def __init__(self, bootstrap_server_url, client_id, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=["kube1-1:30376"],
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic

    def send(self, event: AbstractEvent) -> None:
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=0
        ).add_callback(lambda record_metadata: print(record_metadata))


class PrintConsole(Sink):

    def __init__(self, id):
        self.id = id

    def send(self, event: AbstractEvent) -> None:
        print("Sensor " + self.id + ": " + str(event))




class PrintConsoleSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return PrintConsole(id)


class KafkaSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return KafkaSink(bootstrap_server_url="",
                         client_id=f"{id}",
                         topic="topic")

class TerminalGuiSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return TerminalGui(Terminal(title=id))


class TerminalGui(Sink):
    def __init__(self, terminal):
        self.terminal: Terminal = terminal

    def send(self, event: AbstractEvent):
        self.terminal.print(event)