import json

from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider
import requests

class TimeFrame:
    def __init__(self, duration):
        self.duration = duration
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

class LoadTestHttpSink(Sink):

    def __init__(self, url, frame_duration, data_source_ref):
        super().__init__(data_source_ref)
        self.timeframe = None
        self.url = url
        self.frame_duration = frame_duration

    def start_timeframe(self):
        self.timeframe = TimeFrame(duration=self.frame_duration*1000) # conversion microseconds to milliseconds

    def add_event(self, event):
        self.timeframe.add_event(event)

    def end_timeframe(self):
        requests.post(
            url=self.url + "/register",
            data=self.timeframe.toJson(),
            headers={'Content-Type': 'application/json'}
        )

    def start(self):
        requests.post(url=self.url + "/start")

    def send(self, event: Event) -> None:
        self.timeframe.add_event(event)
