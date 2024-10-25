from abc import ABC


class Simulation(ABC):
    def __init__(self):
        self.sinks = dict()

    def send_event(self, event):
        if event.node in self.sinks:
            for sink in self.sinks[event.node]:
                sink.send(event)
        else:
            print("Skip event. No sink configured")

    def setup_sinks(self, sinks):
        for sink in sinks:
            for data_source in sinks[sink].data_source_ref:
                if data_source not in self.sinks:
                    self.sinks[data_source] = []
                self.sinks[data_source].append(sinks[sink])