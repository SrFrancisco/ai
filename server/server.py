SERVER_PORT="0.0.0.0:5004"

import grpc
import logging
import os
from modelTrain import retrain_model
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
        print("predicted",predicted_class, "acc", predicted_accuracy)
        return teste_pb2.ImageResponse(label=predicted_class, confidence=float(predicted_accuracy))
    
    def RetrainModel(self, request, context):
        print("Received image")
        image_data = request.image_data
        label = request.label
        image = Image.open(BytesIO(image_data))

        add_image_and_label_to_dataset(image, label)

        print("Image was added to backlog")
        return teste_pb2.RetrainResponse(message="Image added to the training data")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    #model_path = '../simple_keras.keras'
    model_path = '../server/retrained_model.keras'
    service = TestService(model_path)
    teste_pb2_grpc.add_TestServiceServicer_to_server(service, server)
    print("Started Server on", SERVER_PORT)
    server.add_insecure_port(SERVER_PORT)
    server.start()

    while True:
        value = input("('retrain' or 'exit') ")
        if value == 'retrain':
            print("Training model")
            retrain_model()
            print("Updating model to use")
            service.model = tf.keras.models.load_model(model_path)
            print("Ready!")

        elif value == 'exit':
            server.stop(grace=True)   
            return

if __name__ == "__main__":
    serve()
