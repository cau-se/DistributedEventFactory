import json
import time

import kafka

from network.network_protocol_factory import BaseNetworkProtocol
import asyncio
from typing import List, Callable, Any
import websockets
from scheduled_thread_pool_executor import ScheduledThreadPoolExecutor
from kafka import KafkaProducer
from scheduled_futures import ScheduledThreadPoolExecutor

from provider.load.load_provider import GradualIncreasingLoadProvider
from utils.utils_types import GeneratedEvent


class WebSocket(BaseNetworkProtocol):
    """
    A class for handling WebSocket connections.
    """

    def __init__(self):
        super().__init__()
        self.data_function = None
        self.TICK_SLEEP = None

    def run(self, url: str, data_function: Callable[[None], GeneratedEvent], tick_sleep: float = 0.5):
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
                await (
                    websocket.send(
                        json.dumps([data.__dict__ for data in self.data_function()])
                    )
                )
        except websockets.exceptions.ConnectionClosedOK as e:
            print("Client Disconnected")
        except websockets.exceptions.ConnectionClosedError as e:
            print("Server Error -> ", e)


class Kafka(BaseNetworkProtocol):

    def send(self, data_function: Callable[[None], GeneratedEvent], producer: KafkaProducer) -> Any:
        event: GeneratedEvent = data_function()
        (producer.send(self.topic, value=json.dumps(event.__dict__), key=event.case_id, partition=0)
         .add_callback(lambda record_metadata: print(record_metadata)))

    def run(self, url: str, data_function: Callable[[None], GeneratedEvent], tick_sleep: float) -> None:
        producer = KafkaProducer(
            bootstrap_servers=url,
            client_id="supermarket",
            key_serializer=lambda key: str.encode(key),
            value_serializer=lambda value: str.encode(value)
        )

        send_kafka_message = lambda: self.send(data_function, producer)
        print_console = lambda: print(time.time())
        load_provider = GradualIncreasingLoadProvider(
            tick_count_til_maximum_reached=20,
            minimal_load=1000,
            maximal_load=1000
        )

        with ScheduledThreadPoolExecutor() as executor:
            while True:
                scheduler = executor.schedule(print_console, period=1/load_provider.get_load_value())
                time.sleep(1)
                scheduler.cancel()

    def __init__(self):
        self.topic = 'topic5'

