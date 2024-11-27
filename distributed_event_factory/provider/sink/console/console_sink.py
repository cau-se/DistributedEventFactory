from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider


class PrintConsole(Sink):

    def __init__(self, id, data_source_ref):
        super().__init__(data_source_ref)
        self.id = id

    def send(self, event: Event) -> None:
        print("Sensor " + event.node + ": " + str(event))

    def start_timeframe(self):
        pass

    def end_timeframe(self):
        pass

class PrintConsoleSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return PrintConsole(id)
