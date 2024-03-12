import grpc
import teste_pb2
import teste_pb2_grpc

def main():
    with grpc.insecure_channel("localhost:5004") as channel:
        stub = teste_pb2_grpc.TestServiceStub(channel)
        image_data = read_image_as_bytes('../assets/glass3.jpeg') #TODO passar para receber pela camara do raspberry
        request = teste_pb2.ImageRequest(image_data=image_data)
        response = stub.PredictImage(request)
        print("Predicted class:", response.prediction)

def read_image_as_bytes(file_path):
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    return image_bytes

if __name__ == "__main__":
    main()
