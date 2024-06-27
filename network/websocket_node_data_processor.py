import json
import threading
import simple_websocket
from network.node_data_processor import NodeDataProcessor
from utils.utils_types import GeneratedEvent
import copy
from typing import List


def parse_message_to_sensor_log(m: dict) -> GeneratedEvent:
    return GeneratedEvent(
        sensor_name=m["sensor_name"],
        timestamp=m["timestamp"],
        sensor_value=m["sensor_value"],
        case_id=m["case_id"],
        status=m["status"],
        generated_by=m["generated_by"]
    )


class WebsocketNodeDataProcessor(NodeDataProcessor):
    def __init__(self, url: str):
        super().__init__()
        self.websocket_sensor_cache: List[GeneratedEvent | List[GeneratedEvent]] = []

        self.URL: str = url
        self.CACHE_IS_READY: bool = False
        self.PROCESSOR_HAS_ERROR: bool = False
        self.PROCESSOR_CONNECTION_HAS_CLOSED: bool = False
        self.PROCESSOR_CONNECTION_IS_OPEN: bool = False
        self.CURRENT_CACHE_LENGTH: int = 0

        try:
            self.ws = simple_websocket.Client(self.URL)
        except ConnectionRefusedError as e:
            self.PROCESSOR_HAS_ERROR = True

    def init_websocket_thread_connection(self) -> None:
        # if self.PROCESSOR_HAS_ERROR:
        #     return
        try:
            while True:
                data: str = self.ws.receive()
                if data:
                    self.on_message(data)

        except (KeyboardInterrupt, EOFError, simple_websocket.ConnectionClosed):
            self.ws.close()
            self.on_error("KeyboardInterrupt, EOFError, simple_websocket.ConnectionClosed")

    def init_cache_generation(self) -> None:
        ws_run = threading.Thread(target=self.init_websocket_thread_connection)
        ws_run.start()

    def on_message(self, message: str):
        message_load: dict | list[dict] = json.loads(message)

        if isinstance(message_load, list):
            temp_sensor_logs: list[GeneratedEvent] = []
            for m in message_load:
                temp_sensor_logs.append(parse_message_to_sensor_log(m))
            self.websocket_sensor_cache.append(temp_sensor_logs)
        else:
            self.websocket_sensor_cache.append(parse_message_to_sensor_log(message_load))

        self.CURRENT_CACHE_LENGTH = len(self.websocket_sensor_cache)

        if self.CURRENT_CACHE_LENGTH <= self.CACHE_LENGTH:
            self.CACHE_IS_READY = False
        else:
            self.CACHE_IS_READY = True

    def on_error(self, error):
        print(f"ERROR IN CONNECTION: {self.URL}", error)
        self.PROCESSOR_HAS_ERROR = True
        self.PROCESSOR_CONNECTION_HAS_CLOSED = True

    def on_open(self):
        print(f"CONNECTION ESTABLISHED WITH CLUSTER: {self.URL}")
        self.PROCESSOR_CONNECTION_IS_OPEN = True
        self.PROCESSOR_HAS_ERROR = False

    def generate_cache(self, cache_length: int) -> List[GeneratedEvent] | None:
        if self.CACHE_IS_READY:
            try:
                cache_to_use = copy.deepcopy(self.websocket_sensor_cache[:self.CACHE_LENGTH])
                del self.websocket_sensor_cache[:self.CACHE_LENGTH]
                return cache_to_use

            except IndexError as e:
                print(e)
                return None

        else:
            return None

