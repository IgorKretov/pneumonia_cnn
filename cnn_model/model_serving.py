import cv2
import numpy as np
from tensorflow.keras.models import load_model


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
    if np.argmax(y_hat[0]) == 0:
        p_normal = round(y_hat[0][0] * 100, 3)
        return ('normal', p_normal)
    else:
        p_pneumonia = round(y_hat[0][1] * 100, 3)
        return ('pneumonia', p_pneumonia)
