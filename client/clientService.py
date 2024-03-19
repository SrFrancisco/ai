import grpc
import teste_pb2
import teste_pb2_grpc
#import picamera
import io
from gpiozero import Button
from time import sleep


import subprocess

def capture_image():
    command = ["fswebcam", "-r", "1280x720", "--no-banner", "image1.jpg"]
    
    try:
        subprocess.run(command, check=True)
        print("Image captured successfully.")
        
        # Read the captured image file as bytes
        with open("image1.jpg", "rb") as f:
            image_bytes = f.read()
        
        return image_bytes

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def capture_image_as_bytes():
    pass 

def predict_image(stub, image_data):
    request = teste_pb2.ImageRequest(image_data=image_data)
    return stub.PredictImage(request)

def retrain_model(stub, image_data,label):
    request = teste_pb2.RetrainRequest(image_data=image_data, label=label)
    response = stub.RetrainModel(request)
    print(response.message)


def perform_action(distance):
    # 0.091 - 0
    if distance <= 0.091:
        return "Plastic"
    
    # 0.189 - 0.091
    elif distance <= 0.189:
        return "Cardboard"
    
    # 0.194 - 0.189
    else:
        return "Glass"
    
def track_distance(ultrasonic, max_distance):
    while True:
        new_distance = ultrasonic.distance
        print(f"Distance: {new_distance:.4f} m")
        if abs(new_distance - max_distance) > 0.007:
            print(f"ChangedDistance: {new_distance:.4f} m")
            return new_distance
        sleep(0.4)  # Delay to avoid excessive polling and false positives
        
