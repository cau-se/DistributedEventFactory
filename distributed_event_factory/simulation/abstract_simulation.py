import string
from abc import ABC
from typing import Dict

from distributed_event_factory.core.abstract_datasource import DataSource


class Simulation(ABC):

    def __init__(self):
        self.datasource_sink_mapping: Dict[string, string] = dict()

    def send_event(self, event):
        if "<any>" in self.datasource_sink_mapping:
            for sink in self.datasource_sink_mapping["<any>"]:
                sink.send(event)
        elif event.group in self.datasource_sink_mapping:
            for sink in self.datasource_sink_mapping[event.group]:
                sink.send(event)
        else:
            print(f"Skip event. No sink configured. Event: {event}")

    def setup_datasource_sink_mapping(self, sinks):
        for sink in sinks:
            if sinks[sink].data_source_ref:
                for data_source in sinks[sink].data_source_ref:
                    self._add_sink_to_datasource(data_source, sinks[sink])

    def _add_sink_to_datasource(self, data_source, sink):
        if data_source not in self.datasource_sink_mapping:
            self.datasource_sink_mapping[data_source] = []
        self.datasource_sink_mapping[data_source].append(sink)
