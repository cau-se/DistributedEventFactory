from abc import ABC


class Simulation(ABC):
    def __init__(self):
        self.datasource_sink_mapping = dict()

    def send_event(self, event):
        if event.node in self.datasource_sink_mapping:
            for sink in self.datasource_sink_mapping[event.node]:
                sink.send(event)
        else:
            print(f"Skip event. No sink configured. Event: {event}")

    def setup_datasource_sink_mapping(self, sinks):
        for sink in sinks:
            if sinks[sink].data_source_ref:
                for data_source in sinks[sink].data_source_ref:
                    if data_source not in self.datasource_sink_mapping:
                        self.datasource_sink_mapping[data_source] = []
                    self.datasource_sink_mapping[data_source].append(sinks[sink])