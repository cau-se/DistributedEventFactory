import abc
import json

from kafka import KafkaProducer
from core.event import Event


class Sender:

    @abc.abstractmethod
    def send(self, event: Event) -> None:
        pass


class KafkaSender(Sender):

    def __init__(self, bootstrap_server_url, client_id, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=["kube1-1:30376"],
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic

    def send(self, event: Event) -> None:
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=0
        ).add_callback(lambda record_metadata: print(record_metadata))


class PrintConsole(Sender):

    def __init__(self, id):
        self.id = id

    def send(self, event: Event) -> None:
        print("Sensor" + self.id + ": " + str(event))


class SendProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sender:
        pass


class PrintConsoleSendProvider(SendProvider):
    def get_sender(self, id) -> Sender:
        return PrintConsole(id)

class KafkaSendProvider(SendProvider):
    def get_sender(self, id) -> Sender:


        return KafkaSender(bootstrap_server_url="",
                client_id=f"{id}",
                topic="topic")


