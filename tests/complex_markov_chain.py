from typing import List

from sensors.sensor_collection import SingleValueSensor, WifiSensor
from sensors.sensors import SensorManager

from utils.markov_chain import MarkovChain
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

sensor_names: List[str] = sensor_manager.get_sensor_names()

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
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00]   # SELF_CHECKOUT_SENSOR
]

builder = TransitionMatrixBuilder()
builder.add_state("DOOR_SENSOR", p=0.0).to("WIFI_SENSOR", p=1.0, t=(1, 5))

builder.add_state("WIFI_SENSOR", p=0.0)\
    .to("PRODUCE_AISLE_SENSOR", p=0.2)\
    .to("MEAT_AISLE_SENSOR", p=0.2)\
    .to("BAKERY_AISLE_SENSOR", p=0.2)\
    .to("DAIRY_AISLE_SENSOR", p=0.1)\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2)\
    .to("CHECKOUT_SENSOR", p=0.05)\
    .to("SELF_CHECKOUT_SENSOR", p=0.05)

builder.add_state("PRODUCE_AISLE_SENSOR", p=0.2)\
    .to("DAIRY_AISLE_SENSOR", p=0.2)\
    .to("MEAT_AISLE_SENSOR", p=0.2)\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2)\
    .to("CHECKOUT_SENSOR", p=0.2)

builder.add_state("MEAT_AISLE_SENSOR", p=0.2)\
    .to("PRODUCE_AISLE_SENSOR", p=0.2)\
    .to("BAKERY_AISLE_SENSOR", p=0.2)\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2)\
    .to("CHECKOUT_SENSOR", p=0.2)

builder.add_state("BAKERY_AISLE_SENSOR", p=0.2)\
    .to("PRODUCE_AISLE_SENSOR", p=0.2)\
    .to("MEAT_AISLE_SENSOR", p=0.2)\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2)\
    .to("CHECKOUT_SENSOR", p=0.2)

builder.add_state("DAIRY_AISLE_SENSOR", p=0.2)\
    .to("PRODUCE_AISLE_SENSOR", p=0.2)\
    .to("MEAT_AISLE_SENSOR", p=0.2)\
    .to("FROZEN_FOOD_AISLE_SENSOR", p=0.2)\
    .to("CHECKOUT_SENSOR", p=0.2)

builder.add_state("FROZEN_FOOD_AISLE_SENSOR", p=0.2)\
    .to("PRODUCE_AISLE_SENSOR", p=0.2)\
    .to("MEAT_AISLE_SENSOR", p=0.2)\
    .to("DAIRY_AISLE_SENSOR", p=0.2)\
    .to("CHECKOUT_SENSOR", p=0.2)

builder.add_state("CHECKOUT_SENSOR", p=0.0)\
    .to("CASH_SENSOR", p=1)

builder.add_state("CREDIT_CARD_SENSOR", p=0.0)\
    .to("EXIT_SENSOR", p=1)

builder.add_state("EXIT_SENSOR", p=0.0)\
    .to("WIFI_SENSOR", p=1)

builder.add_state("CASH_SENSOR", p=0.0)\
    .to("EXIT_SENSOR", p=1)

builder.add_state("SELF_CHECKOUT_SENSOR", p=0.0)\
    .to("EXIT_SENSOR", p=1)

print(builder.to_duration_matrix())

markov_chain = MarkovChain(sensor_names, builder.to_transition_matrix())
markov_chain.simulate(0, 10)
markov_chain.visualize()