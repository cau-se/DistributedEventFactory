from typing import List
from behavior_modifier.outlier_autoencoder import OutlierDetectorAutoencoder
from behavior_modifier.outlier_statistic import OutlierDetector
from network.producer import Node
from sensors.sensor_collection import WifiSensor, SingleValueSensor
from sensors.sensors import SensorManager

from keras.layers import Input, Dense
from keras.models import Model
import numpy as np

#list of dict objects
data = [{'a':1, 'b':2}, {'c':3, 'd':4}, {'c':4, 'd':2}, {'e':5, 'f':6}, {'g':7, 'h':8}]

#convert dict objects to list of lists
data = [list(d.values()) for d in data]

#convert dict objects to numpy array
data = np.array(data)

#shape of the data with 2 dimensions
data = data.reshape(data.shape[0], -1)

#define the autoencoder
input_data = Input(shape=(data.shape[1],))
encoded = Dense(2, activation='relu')(input_data)
decoded = Dense(data.shape[1], activation='sigmoid')(encoded)
autoencoder = Model(input_data, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

#train the autoencoder
autoencoder.fit(data, data, epochs=50, batch_size=1, shuffle=True)

#use the encoder to get the compact representation of the data
encoder = Model(input_data, encoded)
encoded_data = encoder.predict(data)

#calculate the reconstruction error for each data point
reconstruction_error = np.mean(np.power(data - autoencoder.predict(data), 2), axis=1)

#threshold for identifying outliers
threshold = np.mean(reconstruction_error) + 2*np.std(reconstruction_error)

#identify the outliers
outliers = np.where(reconstruction_error > threshold)[0]

#remove the outliers from the data
cleaned_data = np.delete(data, outliers, axis=0)

print("Outliers", outliers)
print(cleaned_data)