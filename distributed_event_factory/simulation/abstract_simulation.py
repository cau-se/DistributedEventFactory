from abc import ABC


class Simulation(ABC):
    def __init__(self):
        self.datasource_sink_mapping = dict()
        self.post_processors = []

    def setup_post_processors(self, post_processors):
        self.post_processors = list(post_processors.values())

    def process_event(self, event):
        processed_event = event
        for post_processor in self.post_processors:
            if processed_event is None:
                return None
            processed_event = post_processor.process(processed_event)
        return processed_event

    def send_event(self, event):
        processed_event = self.process_event(event)
        if processed_event is None:
            return

        if processed_event.node in self.datasource_sink_mapping:
            for sink in self.datasource_sink_mapping[processed_event.node]:
                sink.send(processed_event)
        else:
            print(f"Skip event. No sink configured. Event: {processed_event}")

    def setup_datasource_sink_mapping(self, sinks):
        for sink in sinks:
            if sinks[sink].data_source_ref:
                for data_source in sinks[sink].data_source_ref:
                    if data_source not in self.datasource_sink_mapping:
                        self.datasource_sink_mapping[data_source] = []
                    self.datasource_sink_mapping[data_source].append(sinks[sink])
