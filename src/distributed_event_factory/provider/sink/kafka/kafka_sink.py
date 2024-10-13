import json
import string

from scheduled_futures import ScheduledThreadPoolExecutor

from distributed_event_factory.core.event import AbstractEvent
from distributed_event_factory.provider.sink.kafka.partition.partition_provider import PartitionProvider
from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider


class KafkaSink(Sink):
    def __init__(self, bootstrap_server_url: string, client_id: string, topic: string, partition_provider: PartitionProvider):
        from kafka import KafkaProducer

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server_url,
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic
        self.partition_provider = partition_provider
        self.executor = ScheduledThreadPoolExecutor()

    def kSend(self, event):
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=self.partition_provider.get_partition(event))

    def send(self, event: AbstractEvent) -> None:
        #self.executor.submit(lambda: self.kSend(event))
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=self.partition_provider.get_partition(event))
        #.add_callback(lambda record_metadata: print(record_metadata)))


class KafkaSinkProvider(SinkProvider):

    def __init__(self, bootstrap_server: string, topic: string, partition_provider: PartitionProvider):
        self.bootstrapServer = bootstrap_server
        self.topic = topic
        self.partition_provider = partition_provider

    def get_sender(self, id) -> Sink:
        return KafkaSink(
            bootstrap_server_url=self.bootstrapServer,
            client_id=str(id),
            partition_provider=self.partition_provider,
            topic=self.topic
        )
