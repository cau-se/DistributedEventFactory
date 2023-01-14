import json

from network.network_protocol_factory import BaseNetworkProtocol
import asyncio
from typing import List, Callable, Any
import websockets
from network.producer import Node, Cluster
from utils.types import SensorLog
import random as rd

class WebSocket(BaseNetworkProtocol):
    """
    A class for handling WebSocket connections.
    """

    cluster: Cluster
    def __init__(self):
        super().__init__()

    def run(self, url: str, cluster: Cluster):
        print(f"Server started at {url}")
        self.cluster = cluster
        split_url: List[str] = url.split(":")
        start_server = websockets.serve(self.network_handler, split_url[0], split_url[1])
        asyncio.get_event_loop().run_until_complete(start_server)
        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            print("Event-Loop closed")

    async def network_handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        print("Client Connected")
        try:
            while True:
                await asyncio.sleep(1)
                await websocket.send(self.cluster.get_data())
        except websockets.exceptions.ConnectionClosedOK as e:
            print("Client Disconnected")
        except websockets.exceptions.ConnectionClosedError as e:
            print("Server Error -> ", e)

class ServerSentEvent(BaseNetworkProtocol):
    def __init__(self):
        pass

    def run(self, url: str, cluster: Cluster):
        pass

    def network_handler(self) -> SensorLog:
        pass


class WebRTC(BaseNetworkProtocol):
    def __init__(self):
        pass

    def run(self, data: SensorLog):
        pass

    def network_handler(self) -> SensorLog:
        pass