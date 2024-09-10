from src.distributed_event_factory.core.event import AbstractEvent
from src.distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider
from src.distributed_event_factory.view.terminal import Terminal


class TerminalGui(Sink):
    def __init__(self, terminal):
        self.terminal: Terminal = terminal

    def send(self, event: AbstractEvent):
        self.terminal.print(event)


class TerminalGuiSinkProvider(SinkProvider):

    def __init__(self):
        self.i = -1

    def get_sender(self, id) -> Sink:
        self.i += 1
        return TerminalGui(Terminal(title=id, start_position=self.i))