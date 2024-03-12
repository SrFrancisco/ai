import grpc
import logging
import os
# Suppress TensorFlow INFO and WARNING messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

# Suppress TF-TRT Warning
logging.getLogger('tensorflow.compiler.tf2tensorrt').setLevel(logging.ERROR)
from concurrent import futures
import teste_pb2
import teste_pb2_grpc
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO


classes = ['Cardboard', 'Glass', 'Metal', 'Plastic']

class TestService(teste_pb2_grpc.TestService):
    def __init__(self, model_path) -> None:
        super().__init__()
        self.model = tf.keras.models.load_model('../simple_keras.keras')

    def PredictImage(self, request, context):
        image_data = request.image_data
        image = Image.open(BytesIO(image_data))
        
        image = preprocess_image(image) # Preprocess image

        prediction = self.model.predict(image) # Predict
        
        predicted_label = postprocess_prediction(prediction)

        return teste_pb2.ImageResponse(prediction=predicted_label)

def preprocess_image(image):    
    image = image.resize((256, 256))
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

def postprocess_prediction(prediction):
    prediction_probabilities = prediction[0] * 100
    predicted_class_index = np.argmax(prediction)
    predicted_class = classes[predicted_class_index]
    predicted_confidence = prediction[0][predicted_class_index] * 100

    prediction_string = f"Prediction probabilities: {prediction_probabilities}\n"
    prediction_string += f"Classes: {classes}\n"
    prediction_string += f"Predicted class: {predicted_class} ({predicted_confidence}%)\n"

    return prediction_string

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_path = '../simple_keras.keras'
    teste_pb2_grpc.add_TestServiceServicer_to_server(TestService(model_path), server)
    print("Started Server on")
    server.add_insecure_port("localhost:5004")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
