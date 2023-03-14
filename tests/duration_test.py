from typing import List

from network.cluster import Node
from sensors.sensor_collection import SingleValueSensor, WifiSensor
from sensors.sensors import SensorManager
from utils.transition_matrix_builder import TransitionMatrixBuilder

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

builder = TransitionMatrixBuilder()
builder.add_state("DOOR_SENSOR", p=0.0).to("WIFI_SENSOR", p=1.0, t=(1, 5))

builder.add_state("WIFI_SENSOR", p=0.0)\
    .to("PRODUCE_AISLE_SENSOR", p=0.2, t=(1, 5))\
    .to("MEAT_AISLE_SENSOR", p=0.2, t=(1, 10))\
    .to("BAKERY_AISLE_SENSOR", p=0.2, t=(1, 7))\
    .to("DAIRY_AISLE_SENSOR", p=0.1, t=(1, 5))\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2, t=(1, 3))\
    .to("CHECKOUT_SENSOR", p=0.05, t=(1, 9))\
    .to("SELF_CHECKOUT_SENSOR", p=0.05, t=(1, 5))

builder.add_state("PRODUCE_AISLE_SENSOR", p=0.2, t=(1, 2))\
    .to("DAIRY_AISLE_SENSOR", p=0.2, t=(1, 45))\
    .to("MEAT_AISLE_SENSOR", p=0.2, t=(1, 6))\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2, t=(1, 4))\
    .to("CHECKOUT_SENSOR", p=0.2, t=(1, 7))

builder.add_state("MEAT_AISLE_SENSOR", p=0.2, t=(1, 5))\
    .to("PRODUCE_AISLE_SENSOR", p=0.2, t=(1, 3))\
    .to("BAKERY_AISLE_SENSOR", p=0.2, t=(1, 8))\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2, t=(1, 10))\
    .to("CHECKOUT_SENSOR", p=0.2, t=(1, 15))

builder.add_state("BAKERY_AISLE_SENSOR", p=0.2, t=(1, 14))\
    .to("PRODUCE_AISLE_SENSOR", p=0.2, t=(1, 2))\
    .to("MEAT_AISLE_SENSOR", p=0.2, t=(1, 29))\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2, t=(1, 36))\
    .to("CHECKOUT_SENSOR", p=0.2, t=(1, 11))

builder.add_state("DAIRY_AISLE_SENSOR", p=0.2, t=(1, 5))\
    .to("PRODUCE_AISLE_SENSOR", p=0.2, t=(1, 14))\
    .to("MEAT_AISLE_SENSOR", p=0.2, t=(1, 9))\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2, t=(1, 6))\
    .to("CHECKOUT_SENSOR", p=0.2, t=(1, 8))

builder.add_state("FROZEN_FOOD_AISLE_SENSOR", p=0.2, t=(1, 36))\
    .to("PRODUCE_AISLE_SENSOR", p=0.2, t=(1, 24))\
    .to("MEAT_AISLE_SENSOR", p=0.2, t=(1, 12))\
    .to("DAIRY_AISLE_SENSOR", p=0.2, t=(1, 16))\
    .to("CHECKOUT_SENSOR", p=0.2, t=(1, 13))

builder.add_state("CHECKOUT_SENSOR", p=0.0, t=(1, 36))\
    .to("CASH_SENSOR", p=1, t=(1, 5))

builder.add_state("CREDIT_CARD_SENSOR", p=0.0, t=(1, 15))\
    .to("EXIT_SENSOR", p=1, t=(1, 15))

builder.add_state("EXIT_SENSOR", p=0.0, t=(1, 35))\
    .to("WIFI_SENSOR", p=1, t=(1, 21))

builder.add_state("CASH_SENSOR", p=0.0, t=(1, 5))\
    .to("EXIT_SENSOR", p=1, t=(1, 5))

builder.add_state("SELF_CHECKOUT_SENSOR", p=0.0, t=(1, 5))\
    .to("EXIT_SENSOR", p=1, t=(1, 5))


builder.print_duration_matrix()

