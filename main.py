from tf_model.model_serving import *

image_path = '../data_pneumonia_cnn/test_data/person1946_bacteria_4875.jpeg'
img_array = process_image(image_path)


model_path = './pneumonia_cnn.h5'
predicted, prob = predict(model_path, img_array)
print('predicted class: {} \nprobability: {}%'.format(predicted, prob))