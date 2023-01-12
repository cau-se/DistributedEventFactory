import asyncio
import json
import random
from typing import List

import websockets


class Node:
    data: int

    def __init__(self, id: int):
        self.id = id
        self.refresh_data()

    def refresh_data(self):
        self.data = random.randint(0, 100)

class Cluster:
    def __init__(self, nodes: List[Node], join_function):
        self.nodes = nodes
        self.join_function = join_function
        self.data = self.join_function([node.data for node in self.nodes])

    async def distribute(self, websocket) -> None:
        while True:
            await asyncio.sleep(1)
            for node in self.nodes:
                node.refresh_data()
            self.data = self.join_function([node.data for node in self.nodes])
            await websocket.send(json.dumps(self.data))



def custom_join(data: List[int]) -> int:
    return max(data)

async def handler(websocket, path):
    nodes = [Node(i) for i in range(5)]
    cluster = Cluster(nodes,custom_join)
    await cluster.distribute(websocket)

start_server = websockets.serve(handler, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()