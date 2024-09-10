from abc import abstractmethod, ABC
import time

from scheduled_futures import ScheduledThreadPoolExecutor


class EventLoop(ABC):

    @abstractmethod
    def run(self, process_simulator):
        pass

    def get_number_of_generated_events(self):
        pass


class DebugEventLoop(EventLoop):

    def __init__(self):
        self.tick_count = 0

    def run(self, process_simulator):
        while True:
            self.tick_count += 1
            process_simulator.simulate()

    def get_number_of_generated_events(self):
        return self.tick_count


class LoadEventLoop(EventLoop):
    def __init__(self, load_provider):
        self.load_provider = load_provider

    def run(self, process_simulator):
        with ScheduledThreadPoolExecutor() as executor:
            while True:
                scheduler = executor.schedule(
                    process_simulator.simulate,
                    period=1/self.load_provider.get_load_value()
                )
                time.sleep(1)
                scheduler.cancel()

    def get_number_of_generated_events(self):
        pass

