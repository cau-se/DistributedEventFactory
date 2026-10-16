from abc import ABC


class Simulation(ABC):
    def __init__(self):
        self.datasource_sink_mapping = dict()
        self.post_processors = []

    def setup_post_processors(self, post_processors):
        self.post_processors = list(post_processors.values())

    def process_event(self, event):
        processed_events = self.process_events([event])
        if not processed_events:
            return None
        if len(processed_events) == 1:
            return processed_events[0]
        return processed_events

    def process_events(self, events, start_at=0):
        processed_events = list(events)
        for post_processor in self.post_processors[start_at:]:
            next_events = []
            for event in processed_events:
                result = post_processor.process(event)
                if result is None:
                    continue
                if isinstance(result, (list, tuple)):
                    next_events.extend(item for item in result if item is not None)
                else:
                    next_events.append(result)
            processed_events = next_events
        return processed_events

    def flush_post_processors(self):
        flushed_events = []
        for index, post_processor in enumerate(self.post_processors):
            events = post_processor.flush()
            if events:
                flushed_events.extend(self.process_events(events, start_at=index + 1))
        return flushed_events

    def send_event(self, event):
        for processed_event in self.process_events([event]):
            self._send_processed_event(processed_event)

    def flush_post_processors_to_sinks(self):
        for event in self.flush_post_processors():
            self._send_processed_event(event)

    def _send_processed_event(self, processed_event):
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
