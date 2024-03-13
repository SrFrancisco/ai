import grpc
import teste_pb2
import teste_pb2_grpc

def main():
    with grpc.insecure_channel("localhost:5004") as channel:
        stub = teste_pb2_grpc.TestServiceStub(channel)
        while True:
            user_input = input("Enter 'A' to retrain the model: ")
            if user_input == 'A':
                image_data = read_image_as_bytes('../assets/glass3.jpeg')  # Change to what camera gives us
                label = "cardboard" # Change to input catched by the sensor on to which bin the trash corresponds to
                request = teste_pb2.RetrainRequest(image_data=image_data, label=label)
                response = stub.RetrainModel(request)
                print(response.message)
            else:
                image_data = read_image_as_bytes('../assets/glass3.jpeg')  # Change to what camera gives us
                request = teste_pb2.ImageRequest(image_data=image_data)
                response = stub.PredictImage(request)
                print("Predicted class:", response.prediction)

def read_image_as_bytes(file_path):
    with open(file_path, 'rb') as f:
        image_bytes = f.read()
    return image_bytes

if __name__ == "__main__":
    main()
