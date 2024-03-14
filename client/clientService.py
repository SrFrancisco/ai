import grpc
import teste_pb2
import teste_pb2_grpc
import picamera
import io
from gpiozero import Button

def capture_image_as_bytes():
    with picamera.PiCamera() as camera:
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image_bytes = stream.read()

    return image_bytes

def predict_image(stub, image_data):
    request = teste_pb2.ImageRequest(image_data=image_data)
    response = stub.PredictImage(request)

    return response.prediction

def retrain_model(stub, image_data):
    label = input("Enter the correct label for the image: ")
    request = teste_pb2.RetrainRequest(image_data=image_data, label=label)
    response = stub.RetrainModel(request)
    print(response.message)