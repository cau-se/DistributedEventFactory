import time
from scheduled_futures import ScheduledThreadPoolExecutor

from provider.data.data_provider import DataProvider
from provider.load.load_provider import LoadProvider
from provider.sender.send_provider import Sender


class EventSender:
    def run(self, sender_provider: Sender, data_provider: DataProvider, load_provider: LoadProvider) -> None:
        send_action = lambda: sender_provider.send(data_provider.get_data())
        with ScheduledThreadPoolExecutor() as executor:
            while True:
                period = 1 / load_provider.get_load_value()
                scheduler = executor.schedule(send_action, period=period)
                time.sleep(1)
                scheduler.cancel()
