from provider.sink.console.console_sink import PrintConsoleSinkProvider
from provider.sink.kafka.kafka_sink import KafkaSinkProvider
from provider.sink.kafka.kafka_validation_sink import KafkaValidationSinkProvider
from provider.sink.kafka.partition.partition_registry import PartitionProviderRegistry
from provider.sink.sink_provider import SinkProvider


class SinkProviderRegistry:

    def get_ui(self):
        from provider.sink.ui.terminal_ui_sink import TerminalGuiSinkProvider
        return TerminalGuiSinkProvider()

    def get(self, config) -> SinkProvider:
        registry = dict()
        registry["kafka"] = lambda config: KafkaSinkProvider(
            bootstrap_server=config["bootstrapServer"],
            topic=config["topic"],
            partition_provider=config["partition"]
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
        return registry[config["type"]](config)