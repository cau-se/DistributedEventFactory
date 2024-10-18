from queue import Queue

from distributed_event_factory.provider.sink.http.http_sink import TimeFrame


class SinkQueue:
    def __init__(self):
        self.queue: Queue = Queue()

    def begin_timeframe(self, duration: int):
        self.timeframe = TimeFrame(duration=1000)

    def add_event(self, event):
        self.timeframe.add_event(event)

    def end_timeframe(self):
        self.queue.put(self.timeframe)

    def get(self):
        return self.queue.get()
