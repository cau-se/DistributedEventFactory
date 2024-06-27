import abc
import asyncio
import json

import websocket
import websockets
from kafka import KafkaProducer

from network.network_protocols import WebSocket
from utils.utils_types import GeneratedEvent


class SenderProvider:

    @abc.abstractmethod
    def send(self, event: GeneratedEvent):
        pass


class KafkaSender(SenderProvider):

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


class PrintConsole(SenderProvider):
    def send(self, event: GeneratedEvent):
        print(event)

