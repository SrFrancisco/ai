import grpc
import teste_pb2
import teste_pb2_grpc
import io
import subprocess
from gpiozero import Button
from time import sleep

# Trash cans distances (meters)
TRASH_DISTANCE = 0.25
CLOSER_PLASTIC = 0
FARTHER_PLASTIC = 0.09
CLOSER_CARDBOARD = 0.09
FARTHER_CARDBOARD = 0.19
CLOSER_GLASS = 0.19
FARTHER_GLASS = 0.25

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

def perform_action(ultrasonic, distance):
    if CLOSER_PLASTIC <= distance <= FARTHER_PLASTIC:
        return "Plastic"
    
    elif CLOSER_CARDBOARD < distance <= FARTHER_CARDBOARD:
        return "Cardboard"
    
    elif CLOSER_GLASS < distance <= FARTHER_GLASS:
        return "Glass"
    
    else:
        new_distance = track_distance(ultrasonic)
        return perform_action(ultrasonic, new_distance)
    
def track_distance(ultrasonic):
    while True:
        new_distance = ultrasonic.distance
        if new_distance < TRASH_DISTANCE:
            print(f"Object detected: {new_distance:.4f} m")
            return new_distance
        sleep(0.4)  # Delay to avoid excessive polling and false positives
        
