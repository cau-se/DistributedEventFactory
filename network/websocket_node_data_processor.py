from typing import List

import websocket

from network.node_data_processor import NodeDataProcessor
from utils.utils_types import SensorLog
import rel


class WebsocketNodeDataProcessor(NodeDataProcessor):
    def __init__(self, url: str):
        self.sensor_cache: List[SensorLog] = []
        self.url = url
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(url,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        ws.run_forever(dispatcher=rel, reconnect=5)
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()

    def on_message(self, ws, message):
        self.sensor_cache.append(message)

    def on_error(self, ws, error):
        print(f"ERROR IN CONNECTION: {self.url}", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"CONNECTION CLOSED: {self.url}")

    def on_open(self, ws):
        print(f"CONNECTION CLOSED: {self.url}")

    def generate_cache(self, cache_length: int) -> List[SensorLog]:
        return self.sensor_cache
