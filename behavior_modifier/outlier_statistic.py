from typing import List

from scipy import stats
import numpy as np
import random
from utils.types import SensorLog


class OutlierDetector:
    def __init__(self, sensor_logs: List[SensorLog]):
        self.sensor_logs = sensor_logs

    def add_statistical_outliers(self, sensor_type: str, threshold: float):
        sensor_values = [log.sensor_value for log in self.sensor_logs if log.sensor_name == sensor_type]
        mean = np.mean(sensor_values)
        std_dev = np.std(sensor_values)

        for log in self.sensor_logs:
            if log.sensor_name == sensor_type:
                z_score = (log.sensor_value - mean) / std_dev
                if np.abs(z_score) > threshold:
                    log.status = "Outlier"

    def add_outliers(self, frequency: float, sensor_type: str):
        for log in self.sensor_logs:
            if log.sensor_name == sensor_type:
                if random.random() < frequency:
                    log.sensor_value = "Outlier"