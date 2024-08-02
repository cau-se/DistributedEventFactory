import json

from kafka import KafkaProducer

from core.event import AbstractEvent
from provider.sink.sink_provider import Sink, SinkProvider

class KafkaSink(Sink):
    def __init__(self, bootstrap_server_url, client_id, topic, partition):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server_url,
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

    def __init__(self, bootstrap_server, topic):
        self.bootstrapServer = bootstrap_server
        self.topic = topic

    def get_sender(self, id) -> Sink:
        return KafkaSink(bootstrap_server_url=self.bootstrapServer,
                         client_id=str(id),
                         partition=str(id),
                         topic=self.topic)