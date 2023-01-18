from typing import List
from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
from utils.types import SensorLog


class OutlierDetectorAutoencoder:
    def __init__(self, sensor_logs: List[SensorLog]):
        self.sensor_logs = sensor_logs
        self.autoencoder = self._build_autoencoder()

    def _build_autoencoder(self):
        input_layer = Input(shape=(2,))
        encoded = Dense(1, activation='linear')(input_layer)
        decoded = Dense(1, activation='linear')(encoded)
        autoencoder = Model(input_layer, decoded)
        autoencoder.compile(optimizer='adam', loss='mean_squared_error')
        return autoencoder

    def add_autoencoder_outliers(self, sensor_type: str, threshold: float):
        sensor_values = [log.sensor_value for log in self.sensor_logs if log.sensor_name == sensor_type]
        float_values = []

        for val in sensor_values:
            if type(val) == tuple:
                float_values.append(float(val[0]))
            else:
                float_values.append(float(val))

        self.autoencoder.fit(np.array(float_values), np.array(float_values), epochs=10, batch_size=32)

        for log in self.sensor_logs:
            if log.sensor_name == sensor_type:
                error = self.autoencoder.evaluate(np.array([float(log.sensor_value)]),
                                                  np.array([float(log.sensor_value)]), verbose=0)
                if error > threshold:
                    log.status = "Outlier"
