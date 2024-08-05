from abc import abstractmethod, ABC
import time

from scheduled_futures import ScheduledThreadPoolExecutor


class EventLoop(ABC):

    @abstractmethod
    def run(self, process_simulator):
        pass


class DebugEventLoop(EventLoop):

    def run(self, process_simulator):
        while True:
            process_simulator.simulate()


class LoadEventLoop(EventLoop):
    def __init__(self, load_provider):
        self.load_provider = load_provider

    def run(self, process_simulator):
        with ScheduledThreadPoolExecutor() as executor:
            while True:
                scheduler = executor.schedule(
                    process_simulator.simulate,
                    period=1 / self.load_provider.get_load_value()
                )
                time.sleep(1)
                scheduler.cancel()
