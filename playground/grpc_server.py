import grpc
from concurrent import futures
from proto import data_pb2, data_pb2_grpc

class DataStreamServicer(data_pb2_grpc.DataStreamServicer):
    def SendData(self, request, context):
        for i in range(1, 6):
            yield data_pb2.Data(value=i)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
data_pb2_grpc.add_DataStreamServicer_to_server(DataStreamServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()