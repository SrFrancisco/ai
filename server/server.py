from concurrent import futures
import logging
import math
import time

import grpc
import teste_pb2
import teste_pb2_grpc

class TestService(teste_pb2_grpc.TestService):
    def __init__(self) -> None:
        super().__init__()

    def HelloWorld(self, request, context):
        print("REC Hello world")
        return teste_pb2.HelloWorldResponse(hello=True)

    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    teste_pb2_grpc.add_TestServiceServicer_to_server(TestService(), server)
    print("Started Server on")
    server.add_insecure_port("[::]:5004")
    server.start()
    server.wait_for_termination()

if __name__=="__main__":
    serve()