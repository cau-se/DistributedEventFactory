from core.event import AbstractEvent
from provider.sink.sink_provider import Sink, SinkProvider
from view.terminal import Terminal


class TerminalGui(Sink):
    def __init__(self, terminal):
        self.terminal: Terminal = terminal

    def send(self, event: AbstractEvent):
        self.terminal.print(event)


class TerminalGuiSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return TerminalGui(Terminal(title=id))