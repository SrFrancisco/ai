
import logging
import random

import grpc
import teste_pb2
import teste_pb2_grpc


with grpc.insecure_channel("localhost:5004") as channel:
    stub = teste_pb2_grpc.TestServiceStub(channel)
    response = stub.HelloWorld(teste_pb2.HelloWorldRequest())
    print("Returned", response.hello)