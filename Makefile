install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
all:
	python3 -m grpc_tools.protoc -I./protos --python_out=./server --pyi_out=./server --grpc_python_out=./server ./protos/teste.proto
	python3 -m grpc_tools.protoc -I./protos --python_out=./client --pyi_out=./client --grpc_python_out=./client ./protos/teste.proto

clean:
	rm server/teste_pb2.py server/teste_pb2.pyi server/teste_pb2_grpc.py client/teste_pb2.py client/teste_pb2.pyi client/teste_pb2_grpc.py