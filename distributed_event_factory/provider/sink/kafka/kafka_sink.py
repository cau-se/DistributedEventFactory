import json
import string

from process_mining_core.datastructure.core.event import Event
from distributed_event_factory.provider.sink.kafka.partition.partition_provider import PartitionProvider
from distributed_event_factory.provider.sink.sink_provider import Sink

class KafkaSink(Sink):
    def __init__(self, bootstrap_server_url: string, client_id: string, topic: string,
                 partition_provider: PartitionProvider, data_source_ref):
        super().__init__(data_source_ref)
        from kafka import KafkaProducer

        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_server_url,
            client_id=client_id,
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )
        self.topic = topic
        self.partition_provider = partition_provider

    def send(self, event: Event) -> None:
        self.producer.send(
            self.topic,
            value=json.dumps(event.__dict__),
            key=event.get_case(),
            partition=self.partition_provider.get_partition(event)).add_callback(lambda data: print(data))
