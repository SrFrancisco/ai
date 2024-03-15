import grpc
import teste_pb2
import teste_pb2_grpc
#import picamera
import io
from gpiozero import Button, RGBLED, DistanceSensor,Servo
from clientService import *
from time import sleep

from colorzero import Color
# Define GPIO pin numbers 
CAPTURE_BUTTON_PIN = 23  
RETRAIN_BUTTON_PIN = 24  
LED_RED_PIN = 18
LED_GREEN_PIN = 13
LED_BLUE_PIN = 12

# Define prediction threshold
PREDICTION_THRESHOLD = 70.0

CLASS_TO_COLOR = {
    "Cardboard": (0, 0, 1),  
    "Glass": (0, 1, 0),      
    "Metal": Color('orange'),
    "Plastic": Color('orange') 
}

def main():
    with grpc.insecure_channel("192.168.30.158:5004") as channel:
        stub = teste_pb2_grpc.TestServiceStub(channel)
        
        # Create Button objects
        capture_button = Button(CAPTURE_BUTTON_PIN)
        retrain_button = Button(RETRAIN_BUTTON_PIN)
        # Create RGBLED object
        rgb_led = RGBLED(red=LED_RED_PIN, green=LED_GREEN_PIN, blue=LED_BLUE_PIN)
        # Create DistanceSensor object
        ultrasonic = DistanceSensor(echo=17, trigger=4)
        # Create Servo object
        servo = Servo(19)

        while True:
            capture_button.wait_for_press()
            
            # Capture the image
            image_data = capture_image() 
            
            # Predict the image
            prediction = predict_image(stub, image_data)
            print("Predicted class:", prediction)
            
            if prediction.confidence >= PREDICTION_THRESHOLD and prediction.label in CLASS_TO_COLOR:
                print(">>>", prediction.label ,CLASS_TO_COLOR[prediction.label])
                rgb_led.color = CLASS_TO_COLOR[prediction.label] 
                servo.max()
                sleep(2)
                servo.min()
            else:
                rgb_led.color = (0, 0, 0)  # Turn off LED
            # If prediction accuracy is below threshold, ask if user wants to retrain the model
            if prediction.confidence < PREDICTION_THRESHOLD:
                print("Prediction accuracy is below threshold.")
                print("Press the retrain button within 5 seconds to retrain the model.")
                
                # Wait for the retrain button press within 5 seconds
                if capture_button.wait_for_press(timeout=5):
                    servo.max()
                    distance = track_distance(ultrasonic)
                    label = perform_action(distance)
                    retrain_model(stub, image_data, label)
                    servo.min()
                    print("Model retrained successfully.")
                else:
                    servo.max()
                    sleep(5)
                    servo.min()
                    print("Retrain option not selected.")
            else:
                print("Prediction accuracy is above threshold. No retraining needed.")

if __name__ == "__main__":
    main()
