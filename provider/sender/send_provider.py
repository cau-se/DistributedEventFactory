import abc
import json

from kafka import KafkaProducer

from core.event import Event
from view.terminal import Terminal


class Sender:

    @abc.abstractmethod
    def send(self, event: Event):
        pass


class KafkaSender(Sender):

    def __init__(self, bootstrap_server_url, client_id, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server_url,
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic

    def send(self, event: Event):
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.case_id,
            partition=0
        ).add_callback(lambda record_metadata: print(record_metadata))


class PrintConsole(Sender):

    def __init__(self, id):
        self.id = id

    def send(self, event: Event):
        print("Sensor" + self.id + ": " + str(event))


class TerminalGui(Sender):
    def __init__(self, terminal):
        self.terminal: Terminal = terminal

    def send(self, event: Event):
        self.terminal.print(event)


class SendProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sender:
        pass


class PrintConsoleSendProvider(SendProvider):
    def get_sender(self, id) -> Sender:
        return PrintConsole(id)


class TerminalGuiSendProvider(SendProvider):
    def get_sender(self, id) -> Sender:
        return TerminalGui(Terminal(title=id))
