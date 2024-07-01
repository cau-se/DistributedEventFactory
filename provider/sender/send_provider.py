import abc
import json

from kafka import KafkaProducer
from utils.utils_types import GeneratedEvent


class Sender:

    @abc.abstractmethod
    def send(self, event: GeneratedEvent):
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

    def send(self, event: GeneratedEvent):
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.case_id,
            partition=0
        ).add_callback(lambda record_metadata: print(record_metadata))


class PrintConsole(Sender):

    def __init__(self, id):
        self.id = id

    def send(self, event: GeneratedEvent):
        print("Sensor" + self.id + ": " + str(event))


class SendProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sender:
        pass


class PrintConsoleSendProvider(SendProvider):
    def get_sender(self, id) -> Sender:
        return PrintConsole(id)
