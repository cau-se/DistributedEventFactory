from core.event import AbstractEvent
from provider.sink.sink_provider import Sink, SinkProvider

class PrintConsole(Sink):

    def __init__(self, id):
        self.id = id

    def send(self, event: AbstractEvent) -> None:
        print("Sensor " + self.id + ": " + str(event))


class PrintConsoleSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return PrintConsole(id)

