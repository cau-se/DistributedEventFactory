import json
import string

from distributed_event_factory.core.event import AbstractEvent
from distributed_event_factory.provider.sink.kafka.partition.partition_provider import ConstantPartitionProvider, \
    PartitionProvider
from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider


class KafkaValidationSink(Sink):
    def __init__(
            self,
            bootstrap_server_url,
            client_id,
            topic,
            partition_provider,
            validation_topic,
            validation_split
    ):
        from kafka import KafkaProducer

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server_url,
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic
        self.partition_provider = partition_provider
        self.validation_topic = validation_topic
        self.validation_split = validation_split

    def send(self, event: AbstractEvent) -> None:
        if hash(event.get_case()) % self.validation_split == 0:
            send_topic = self.validation_topic
            send_partition = ConstantPartitionProvider(partition=0)
        else:
            send_topic = self.topic
            send_partition = self.partition_provider

        self.producer.send(
            send_topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=send_partition.get_partition(event)
        ).add_callback(lambda record_metadata: print(record_metadata))


class KafkaValidationSinkProvider(SinkProvider):
    def __init__(
            self,
            bootstrap_server: string,
            topic: string,
            partition_provider: PartitionProvider,
            validation_topic: string,
            validation_split: string
    ):
        self.bootstrapServer = bootstrap_server
        self.topic = topic
        self.partition_provider = partition_provider
        self.validation_topic = validation_topic
        self.validation_split = validation_split

    def get_sender(self, id) -> Sink:
        return KafkaValidationSink(
            bootstrap_server_url=self.bootstrapServer,
            client_id=str(id),
            topic=self.topic,
            partition_provider=self.partition_provider,
            validation_topic=self.validation_topic,
            validation_split=self.validation_split
        )
