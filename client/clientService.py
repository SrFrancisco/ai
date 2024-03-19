import grpc
import teste_pb2
import teste_pb2_grpc
import io
import subprocess
from gpiozero import Button
from time import sleep

def capture_image():
    command = ["fswebcam", "-r", "640x480", "--no-banner", "image1.jpg"]
    
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

def open_servo():
    pass

def perform_action(distance):
    if 0 <= distance <= 0.09:
        return "Plastic"
    
    elif 0.09 < distance <= 0.19:
        return "Cardboard"
    
    else:
        return "Glass"
    
def track_distance(ultrasonic, min_distance):
    while True:
        new_distance = ultrasonic.distance
        if new_distance < min_distance:
            print(f"Object detected: {new_distance:.4f} m")
            return new_distance
        sleep(0.4)  # Delay to avoid excessive polling and false positives
        
