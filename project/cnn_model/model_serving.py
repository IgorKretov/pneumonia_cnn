from tensorflow.keras.models import load_model
import numpy as np
import cv2


def process_image(image_path):
    """process an image and return it as a numpy array in a specific shape
    which can be fed into a CNN model for prediction
    """
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (196, 196))
    img = img/255.0
    img = np.reshape(img, (1, 196, 196, 1))
    return img


def predict(model_path, img_array):
    """load the pre-trained CNN model,
    predict the probability of pneumonia of a given image array,
    and return the predicted class and value
    """
    loaded_model = load_model(model_path)
    y_hat = loaded_model.predict(img_array)
    predicted_value = y_hat[0][0]
    if predicted_value < 0.5:
        return ('normal', round(predicted_value * 100, 3))
    else:
        return ('pneumonia', round(predicted_value * 100, 3))
