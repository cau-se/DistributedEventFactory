import json
from queue import Queue

from distributed_event_factory.core.event import AbstractEvent
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

class HttpSink(Sink):

    def __init__(self, url, frame_duration):
        self.url = url
        self.frame_duration = frame_duration

    def start_timeframe(self):
        self.timeframe = TimeFrame(duration=self.frame_duration)

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

    def send(self, event: AbstractEvent) -> None:
        self.timeframe.add_event(event)

class HttpSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return HttpSink()