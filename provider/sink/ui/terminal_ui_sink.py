from core.event import AbstractEvent
from provider.sink.sink_provider import Sink, SinkProvider
from view.terminal import Terminal


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