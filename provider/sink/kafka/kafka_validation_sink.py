import json

from kafka import KafkaProducer

from core.event import AbstractEvent
from provider.sink.sink_provider import Sink, SinkProvider


class KafkaValidationSink(Sink):
    def __init__(
            self,
            bootstrap_server_url,
            client_id,
            topic,
            partition,
            validation_topic,
            validation_split
    ):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server_url,
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic
        self.partition = partition
        self.validation_topic = validation_topic
        self.validation_split = validation_split

    def send(self, event: AbstractEvent) -> None:
        if hash(event.get_case()) % self.validation_split == 0:
            send_topic = self.validation_topic
            send_partition = 0
        else:
            send_topic = self.topic
            send_partition = self.partition

        self.producer.send(
            send_topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=send_partition
        ).add_callback(lambda record_metadata: print(record_metadata))


class KafkaValidationSinkProvider(SinkProvider):
    def __init__(self, bootstrap_server, topic, partition, validation_topic, validation_split):
        self.bootstrapServer = bootstrap_server
        self.topic = topic
        self.partition = partition
        self.validation_topic = validation_topic
        self.validation_split = validation_split

    def get_sender(self, id) -> Sink:
        return KafkaValidationSink(
            bootstrap_server_url=self.bootstrapServer,
            client_id=str(id),
            topic=self.topic,
            partition=self.partition,
            validation_topic=self.validation_topic,
            validation_split=self.validation_split
        )
