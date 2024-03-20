SERVER_PORT="192.168.30.158:5004"

import grpc
import teste_pb2
import teste_pb2_grpc
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
SERVO_PIN = 19
US_ECHO_PIN = 17
US_TRIGGER_PIN = 4

# Fixed values
MAX_VAL_SERVO = 1
MIN_VAL_SERVO = -1
MIN_DISTANCE = 0.25

# Define prediction threshold
PREDICTION_THRESHOLD = 70.0

CLASS_TO_COLOR = {
    "Cardboard": (0, 0, 1),  
    "Glass": (0, 1, 0),      
    "Metal": Color('yellow'),
    "Plastic": Color('yellow') 
}

class Bin:
    def __init__(self, servo):
        self.servo = servo

    def open(self):
        self.servo.value = MIN_VAL_SERVO
        sleep(2)
    
    def close(self):
        sleep(1)
        self.servo.value = MAX_VAL_SERVO


def main():
    with grpc.insecure_channel(SERVER_PORT) as channel:
        stub = teste_pb2_grpc.TestServiceStub(channel)
        
        # Create Button objects
        capture_button = Button(CAPTURE_BUTTON_PIN)
        retrain_button = Button(RETRAIN_BUTTON_PIN)

        # Create RGBLED object
        rgb_led = RGBLED(red=LED_RED_PIN, green=LED_GREEN_PIN, blue=LED_BLUE_PIN)

        # Create DistanceSensor object
        ultrasonic = DistanceSensor(echo=US_ECHO_PIN, trigger=US_TRIGGER_PIN)

        # Create Servo object
        servo = Servo(SERVO_PIN)
        servo.value = MAX_VAL_SERVO

        bin = Bin(servo)

        while True:
            print(" ===== Smart bin is ready =====")
            print("Press a button to continue...")
            print()
            capture_button.wait_for_press()
            
            # Capture the image
            image_data = capture_image() 
            
            # Predict the image
            print("Predicting image...")
            prediction = predict_image(stub, image_data)
            print("---- Prediction ----")
            print(prediction)
            print()
            
            if prediction.confidence >= PREDICTION_THRESHOLD and prediction.label in CLASS_TO_COLOR:
                print(">>>", prediction.label)
                rgb_led.color = CLASS_TO_COLOR[prediction.label] 

                bin.open()

                # TODO: wait for retraining button
                distance = track_distance(ultrasonic, MIN_DISTANCE)
                label = perform_action(distance)
                print("Deposited in", label)

                bin.close()

                rgb_led.color = (0, 0, 0)  # Turn off LED

            # If prediction accuracy is below threshold, retrain model
            elif prediction.confidence < PREDICTION_THRESHOLD:
                print("Prediction accuracy is below threshold.")

                rgb_led.color = (1, 0, 0)  # Red LED

                bin.open()

                distance = track_distance(ultrasonic, MIN_DISTANCE)
                label = perform_action(distance)
                rgb_led.color = CLASS_TO_COLOR[label]
                print("Deposited in", label)

                # retrain_model(stub, image_data, label)
                print("Model went to retraining. It will predict better tomorrow.")

                bin.close()

                sleep(1)

                rgb_led.color = (0, 0, 0)  # Turn off LED

            else:
                print("Something went wrong.")

            print()
            print()

if __name__ == "__main__":
    main()
