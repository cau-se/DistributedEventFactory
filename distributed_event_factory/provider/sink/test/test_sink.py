from typing import List

from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.sink_provider import Sink

class TestSink(Sink):
    def __init__(self, data_source_ref):
        super().__init__(data_source_ref)
        self.event_log: List[Event] = []

    def send(self, event: Event) -> None:
        self.event_log.append(event)

    def contains_event(self, event):
        return event in self.event_log