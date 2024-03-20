import numpy as np
import os
from PIL import Image
import datetime


classes = ['Cardboard', 'Glass', 'Metal', 'Plastic']

TRAINING_DATASET_PATH="../NewImagesDataset" # do not put last /

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

    return predicted_class, predicted_confidence

def add_image_and_label_to_dataset(image:Image, label:str):
    # Logic to add the image and label to your dataset goes here
    os.makedirs(TRAINING_DATASET_PATH, exist_ok=True) 
    for class_ in classes: # check if the subfolders exist and create if not
        os.makedirs(TRAINING_DATASET_PATH+"/"+class_, exist_ok=True)
    image.save(TRAINING_DATASET_PATH+"/"+label+"/"+label+datetime.datetime.now().strftime("%d%m%Y%H%M%S")+".jpg")

