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
from serverService import preprocess_image, postprocess_prediction

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
    
    def RetrainModel(self, request, context):
        image_data = request.image_data
        label = request.label
        image = Image.open(BytesIO(image_data))

        # Assuming you have a function to add this image and label to your dataset
        add_image_and_label_to_dataset(image, label)

        # Assuming you have a function to retrain the model
        retrain_model()

        return teste_pb2.RetrainResponse(message="Model retrained successfully.")

    def add_image_and_label_to_dataset(image, label):
        # Logic to add the image and label to your dataset goes here
        pass

    def retrain_model():
        # Logic to retrain your model goes here
        pass

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
