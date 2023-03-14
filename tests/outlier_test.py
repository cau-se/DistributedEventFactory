import random
from datetime import timedelta

from typing import List

from network.cluster import Node
from sensors.sensor_collection import SingleValueSensor, WifiSensor
from sensors.sensors import SensorManager
from utils.utils_types import SensorLog

import matplotlib.pyplot as plt
import datetime
import numpy as np


class OutlierGeneratorModifier:
    def __init__(self, sensor_logs: List[SensorLog]):
        self.sensor_logs = sensor_logs
        self.outlier_timestamp_delta_range = (-timedelta(hours=1), timedelta(hours=1))
        self.outlier_value_range = (-10, 10)

    def generate_outliers(self, outlier_prob: float = 0.05):
        for log in self.sensor_logs:
            if random.random() < outlier_prob:
                # Generate outlier timestamp
                outlier_timestamp_delta = random.uniform(*self.outlier_timestamp_delta_range)
                outlier_timestamp = log.timestamp + outlier_timestamp_delta

                # Generate outlier sensor value
                outlier_value = random.uniform(*self.outlier_value_range)

                # Update log with outlier values
                log.timestamp = outlier_timestamp
                log.sensor_value = outlier_value
                log.status = "OUTLIER"


sensor_manager: SensorManager = SensorManager()
sensor_manager.add_sensor(SingleValueSensor(["Door Open"], "DOOR_SENSOR"))
sensor_manager.add_sensor(WifiSensor("WIFI_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["PRODUCE_AISLE"], "PRODUCE_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["MEAT_AISLE"], "MEAT_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["BAKERY_AISLE"], "BAKERY_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["DAIRY_AISLE"], "DAIRY_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["FROZEN_FOOD_AISLE"], "FROZEN_FOOD_AISLE_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["CHECKOUT"], "CHECKOUT_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["CREDIT_CARD"], "CREDIT_CARD_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["EXIT"], "EXIT_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["CASH"], "CASH_SENSOR"))
sensor_manager.add_sensor(SingleValueSensor(["SELF_CHECKOUT"], "SELF_CHECKOUT_SENSOR"))

transition_matrix: List[List[float]] = [
    [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # DOOR_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.00, 0.00, 0.10],  # WIFI_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.00, 0.10, 0.00],  # PRODUCE_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.10, 0.00, 0.00],  # MEAT_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.10, 0.00, 0.00, 0.00],  # BAKERY_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.10, 0.00, 0.00, 0.00, 0.00],  # DAIRY_AISLE_SENSOR
    [0.00, 0.00, 0.20, 0.20, 0.20, 0.20, 0.10, 0.00, 0.00, 0.05, 0.00, 0.05],  # FROZEN_FOOD_AISLE_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],  # CHECKOUT_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.00, 0.00, 0.00, 0.90, 0.00, 0.00],  # CREDIT_CARD_SENSOR
    [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # EXIT_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00],  # CASH_SENSOR
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00]  # SELF_CHECKOUT_SENSOR
]