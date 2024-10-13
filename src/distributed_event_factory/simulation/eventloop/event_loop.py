from abc import abstractmethod, ABC
import time
from scheduled_futures import ScheduledThreadPoolExecutor

from src.distributed_event_factory.provider.sink.http.http_sink import TimeFrame, HttpSink


class EventLoop(ABC):
    @abstractmethod
    def run(self, process_simulator):
        pass


class DebugEventLoop(EventLoop):
    def run(self, process_simulator):
        while True:
            process_simulator.simulate()

class AsyncEventLoop(EventLoop):

    def __init__(self, load_provider, time_frame_duration):
        self.load_provider = load_provider
        self.time_frame_duration = time_frame_duration
        self.sink = HttpSink()

    def run(self, process_simulator):
        while True:
            self.sink.begin_timeframe(self.time_frame_duration)
            event_count = self.load_provider.get_load_value()
            for i in range(event_count):
                self.sink.add_event(process_simulator.simulate())
            self.sink.end_timeframe()

            

class LoadEventLoop(EventLoop):
    def __init__(self, load_provider):
        self.load_provider = load_provider

    def run(self, process_simulator):
        with ScheduledThreadPoolExecutor() as executor:
            while True:
                scheduler = executor.schedule(
                    lambda: process_simulator.simulate()(),
                    period=1/self.load_provider.get_load_value()
                )
                time.sleep(1)
                scheduler.cancel()

