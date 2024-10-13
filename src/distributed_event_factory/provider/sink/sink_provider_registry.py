from src.distributed_event_factory.provider.sink.console.console_sink import PrintConsoleSinkProvider
from src.distributed_event_factory.provider.sink.http.http_sink import HttpSink, HttpSinkProvider
from src.distributed_event_factory.provider.sink.kafka.kafka_sink import KafkaSinkProvider
from src.distributed_event_factory.provider.sink.kafka.kafka_validation_sink import KafkaValidationSinkProvider
from src.distributed_event_factory.provider.sink.kafka.partition.partition_registry import PartitionProviderRegistry
from src.distributed_event_factory.provider.sink.sink_provider import SinkProvider

class SinkProviderRegistry:

    def get_ui(self):
        from src.distributed_event_factory.provider.sink.ui.terminal_ui_sink import TerminalGuiSinkProvider
        return TerminalGuiSinkProvider()

    def get(self, config) -> SinkProvider:
        registry = dict()
        registry["kafka"] = lambda config: KafkaSinkProvider(
            bootstrap_server=config["bootstrapServer"],
            topic=config["topic"],
            partition_provider=PartitionProviderRegistry().get(config["partition"])
        )
        registry["kafkaValidation"] = lambda config: KafkaValidationSinkProvider(
            bootstrap_server=config["bootstrapServer"],
            topic=config["topic"],
            partition_provider=PartitionProviderRegistry().get(config["partition"]),
            validation_topic=config["validationTopic"],
            validation_split=config["validationSplit"]
        )
        registry["ui"] = lambda config: self.get_ui()
        registry["console"] = lambda config: PrintConsoleSinkProvider()
        registry["console"] = lambda config: PrintConsoleSinkProvider()
        registry["http"] = lambda config: HttpSinkProvider()
        #registry["custom"] lambda config: CustomReceiver()

        return registry[config["type"]](config)