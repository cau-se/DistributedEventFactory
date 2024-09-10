from src.distributed_event_factory.core.event import AbstractEvent
from src.distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider


class PrintConsole(Sink):

    def __init__(self, id):
        self.id = id

    def send(self, event: AbstractEvent) -> None:
        print("Sensor " + self.id + ": " + str(event))


class PrintConsoleSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return PrintConsole(id)

