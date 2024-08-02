from provider.sink.console.console_sink import PrintConsoleSinkProvider
from provider.sink.kafka.kafka_sink import KafkaSinkProvider
from provider.sink.sink_provider import SinkProvider
from provider.sink.ui.terminal_ui_sink import TerminalGuiSinkProvider


class SinkProviderRegistry:

    def get(self, config) -> SinkProvider:
        registry = dict()
        registry["kafka"] = lambda config: KafkaSinkProvider(bootstrap_server=config["bootstrapServer"], topic=config["topic"])
        registry["ui"] = lambda config: TerminalGuiSinkProvider()
        registry["console"] = lambda config: PrintConsoleSinkProvider()
        return registry[config["type"]](config)