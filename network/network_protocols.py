import json

from network.network_protocol_factory import BaseNetworkProtocol
import asyncio
from typing import List, Callable
import websockets

from utils.utils_types import SensorLog


class WebSocket(BaseNetworkProtocol):
    """
    A class for handling WebSocket connections.
    """

    def __init__(self):
        super().__init__()
        self.data_function = None
        self.TICK_SLEEP = None

    def run(self, url: str, data_function: Callable[[None], str], tick_sleep: float = 0.5):
        print(f"Server started at {url}")
        self.data_function = data_function
        split_url: List[str] = url.split(":")
        start_server = websockets.serve(self.handle_network, split_url[0], split_url[1])
        asyncio.get_event_loop().run_until_complete(start_server)
        self.TICK_SLEEP: float = tick_sleep
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            print("Event-Loop closed")

    async def handle_network(self, websocket: websockets.WebSocketServerProtocol, path: str):
        print("Client Connected")
        try:
            while True:
                await asyncio.sleep(self.TICK_SLEEP)
                await websocket.send(self.data_function())
        except websockets.exceptions.ConnectionClosedOK as e:
            print("Client Disconnected")
        except websockets.exceptions.ConnectionClosedError as e:
            print("Server Error -> ", e)


class ServerSentEvent(BaseNetworkProtocol):
    def __init__(self):
        pass

    def run(self, url: str, data_function: Callable[[None], str], tick_sleep: float = 0.5):
        pass


class WebRTC(BaseNetworkProtocol):
    def __init__(self):
        pass

    def run(self, url: str, data_function: Callable[[None], str], tick_sleep: float = 0.5):
        pass
