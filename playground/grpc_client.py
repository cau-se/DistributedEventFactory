import grpc
from proto import data_pb2, data_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = data_pb2_grpc.DataStreamStub(channel)

for response in stub.SendData(data_pb2.DataRequest()):
    print(response.value)