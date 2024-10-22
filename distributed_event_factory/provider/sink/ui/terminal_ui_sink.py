from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider
from distributed_event_factory.view.terminal import Terminal

class TerminalGui(Sink):
    def __init__(self, terminal):
        self.terminal: Terminal = terminal

    def send(self, event: Event):
        self.terminal.print(event)

class UiSink(Sink):
    def __init__(self, id, data_source_ref):
        self.ui = Terminal(title=id, start_position=0)
        self.data_source_ref = data_source_ref

    def send(self, event: Event) -> None:
        self.ui.print(event)


class TerminalGuiSinkProvider(SinkProvider):
    def __init__(self):
        self.i = -1

    def get_sender(self, id) -> Sink:
        self.i += 1
        return TerminalGui(Terminal(title=id, start_position=self.i))