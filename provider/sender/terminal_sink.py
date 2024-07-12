from core.event import Event
from provider.sender.send_provider import SendProvider, Sender
from view.terminal import Terminal


class TerminalGuiSendProvider(SendProvider):
    def get_sender(self, id) -> Sender:
        return TerminalGui(Terminal(title=id))


class TerminalGui(Sender):
    def __init__(self, terminal):
        self.terminal: Terminal = terminal

    def send(self, event: Event):
        self.terminal.print(event)
