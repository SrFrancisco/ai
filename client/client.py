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
MAX_VAL_SERVO = 0.7
MIN_VAL_SERVO = -0.7

# Define prediction threshold
PREDICTION_THRESHOLD = 70.0

CLASS_TO_COLOR = {
    "Cardboard": (0, 0, 1),  
    "Glass": (0, 1, 0),      
    "Metal": Color('orange'),
    "Plastic": Color('orange') 
}

class Bin:
    def __init__(self, servo):
        self.servo = servo

    def open(self):
        self.servo.value = MIN_VAL_SERVO
    
    def close(self):
        self.servo.value = MAX_VAL_SERVO


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
        max_distance = ultrasonic.distance

        # Create Servo object
        servo = Servo(19)
        servo.value = MAX_VAL_SERVO

        bin = Bin(servo)

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

                bin.open()
                # clicar no botao para retreinar se necessario
                distance = track_distance(ultrasonic, max_distance)
                label = perform_action(distance)
                print("Deposited in", label)

                bin.close()

                rgb_led.color = (0, 0, 0)  # Turn off LED

            else:
                rgb_led.color = (0, 0, 0)  # Turn off LED

            # If prediction accuracy is below threshold, ask if user wants to retrain the model
            if prediction.confidence < PREDICTION_THRESHOLD:
                print("Prediction accuracy is below threshold.")
                rgb_led.color = (1, 0, 0)
                # print("Press the retrain button within 5 seconds to retrain the model.")
                
                # Wait for the retrain button press within 5 seconds
                # if capture_button.wait_for_press(timeout=5):
                #     bin.open()
                #     distance = track_distance(ultrasonic, max_distance)
                #     label = perform_action(distance)
                #     retrain_model(stub, image_data, label)
                #     bin.close()
                #     print("Model retrained successfully.")

                # else:
                bin.open()

                distance = track_distance(ultrasonic, max_distance)
                label = perform_action(distance)
                print("Deposited in", label)

                bin.close()

                rgb_led.color = (0, 0, 0)  # Turn off LED

                # print("Retrain option not selected.")

            else:
                print("Prediction accuracy is above threshold. No retraining needed.")

if __name__ == "__main__":
    main()
