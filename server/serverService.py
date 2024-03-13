import numpy as np

classes = ['Cardboard', 'Glass', 'Metal', 'Plastic']

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
