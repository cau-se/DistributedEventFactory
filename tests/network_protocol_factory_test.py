from typing import List, Callable, Any

from network.network_protocol_factory import NetworkProtocolFactory, BaseNetworkProtocol
from network.network_protocols import WebSocket, WebRTC, ServerSentEvent
from network.producer import Node, Cluster
from utils.types import SensorLog

factory = NetworkProtocolFactory()
factory.register_protocol('websocket', WebSocket)
# factory.register_protocol('sse', ServerSentEvent)
# factory.register_protocol('webrtc', WebRTC)

network: BaseNetworkProtocol = factory.create_protocol('websocket')
# network: BaseNetworkProtocol = factory.create_protocol('sse')
# network: BaseNetworkProtocol = factory.create_protocol('webrtc')


nodes: List[Node] = [Node(i) for i in range(5)]
node_join_function: Callable[[List[SensorLog]], Any] = lambda data: data
cluster: Cluster = Cluster(nodes, node_join_function)

network.run("localhost:8000", cluster=cluster)