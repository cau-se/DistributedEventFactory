from provider.sink.console.console_sink import PrintConsoleSinkProvider
from provider.sink.kafka.kafka_sink import KafkaSinkProvider
from provider.sink.sink_provider import SinkProvider
from provider.sink.ui.terminal_ui_sink import TerminalGuiSinkProvider


class SinkProviderRegistry:

    def get(self, config) -> SinkProvider:
        registry = dict()
        registry["kafka"] = KafkaSinkProvider()
        registry["ui"] = TerminalGuiSinkProvider()
        registry["console"] = PrintConsoleSinkProvider()
        return registry[config]