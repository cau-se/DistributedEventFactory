import copy
import time
from copy import deepcopy
from queue import Queue
from threading import Thread, Lock

from scheduled_futures import ScheduledThreadPoolExecutor
from distributed_event_factory.provider.sink.http.http_sink import TimeFrame

class NewSink:

    def begin_timeframe(self, duration: int):
        pass

    def add_event(self, event):
        pass

    def end_timeframe(self):
        pass

    def start(self):
        pass

class ConsoleNewSink(NewSink):

    def __init__(self):
        self.queue: Queue = Queue()

    def begin_timeframe(self, duration: int):
        self.time_frame = TimeFrame(duration)

    def add_event(self, event):
        self.time_frame.add_event(event)

    def end_timeframe(self):
        self.queue.put(self.time_frame)

    def print(self, data):
        print(data)

    def start(self):
        with ScheduledThreadPoolExecutor() as executor:
            while True:
                events = self.queue.get().events
                event_iterator = iter(events)
                events_length = len(events)
                duration = self.time_frame.duration
                if events_length != 0:
                    scheduler = executor.schedule(
                        lambda: self.print(next(event_iterator)),
                        period=duration / events_length
                    )
                    time.sleep(duration)
                    scheduler.cancel()
