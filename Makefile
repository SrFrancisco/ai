install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	@echo
	@echo ------------------- DONE -------------------
	@echo Before running the program please activate the
	@echo python virtual environment with
	@echo    source .venv/bin/activate
	@echo 
	@echo It's also necessary to compile the protos

compile:
	python3 -m grpc_tools.protoc -I./protos --python_out=./server --pyi_out=./server --grpc_python_out=./server ./protos/teste.proto
	python3 -m grpc_tools.protoc -I./protos --python_out=./client --pyi_out=./client --grpc_python_out=./client ./protos/teste.proto

clean:
	rm server/teste_pb2.py server/teste_pb2.pyi server/teste_pb2_grpc.py client/teste_pb2.py client/teste_pb2.pyi client/teste_pb2_grpc.py