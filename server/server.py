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
from PIL import Image
from io import BytesIO
from serverService import *

class TestService(teste_pb2_grpc.TestService):
    def __init__(self, model_path) -> None:
        super().__init__()
        self.model = tf.keras.models.load_model(model_path)

    def PredictImage(self, request, context):
        image_data = request.image_data
        image = Image.open(BytesIO(image_data))
        
        image = preprocess_image(image) # Preprocess image

        prediction = self.model.predict(image) # Predict
        
        predicted_class, predicted_accuracy = postprocess_prediction(prediction)

        return teste_pb2.ImageResponse(label=predicted_class, confidence=predicted_accuracy)
    
    def RetrainModel(self, request, context):
        image_data = request.image_data
        label = request.label
        image = Image.open(BytesIO(image_data))

        add_image_and_label_to_dataset(image, label)

        retrain_model()

        return teste_pb2.RetrainResponse(message="Model retrained successfully.")

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
