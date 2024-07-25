import json

from kafka import KafkaProducer

from core.event import AbstractEvent
from provider.sink.sink_provider import Sink, SinkProvider

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

class KafkaSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return KafkaSink(bootstrap_server_url="",
                         client_id=f"{id}",
                         topic="topic")