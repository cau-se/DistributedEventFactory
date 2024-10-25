import json

from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.kafka.partition.partition_provider import ConstantPartitionProvider
from distributed_event_factory.provider.sink.sink_provider import Sink


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

    def send(self, event: Event) -> None:
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
