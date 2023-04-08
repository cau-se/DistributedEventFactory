from sensors.sensor_collection import SingleValueSensor
from sensors.sensors import SensorManager
from utils.transition_matrix_builder import TransitionMatrixBuilder

SUPERMARKET_SENSOR_MANAGER: SensorManager = SensorManager()
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Entrance"], "Entrance_and_exit"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter sweets and snacks"], "Sweets_snacks"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Fruit"], "Fruit"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Vegetables"], "Vegetables"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Meat and poultry"], "Meat_poultry"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Canned and dry goods"], "Canned_dry_goods"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Dairy products and eggs"], "Dairy_products_eggs"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Frozen food"], "Frozen_food"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Beverages"], "Beverages"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Baker"], "Baker"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Cash registers"], "Cash_registers"))


SUPERMARKET_BUILDER = TransitionMatrixBuilder()
SUPERMARKET_BUILDER.add_state("Entrance_and_exit", p=0.0)\
    .to(next_state="Sweets_snacks", p=1, t=(1, 2))

SUPERMARKET_BUILDER.add_state("Sweets_snacks", p=0.0)\
    .to(next_state="Entrance_and_exit", p=0.25, t=(1, 2))\
    .to(next_state="Vegetables", p=0.25, t=(1, 2))\
    .to(next_state="Meat_poultry", p=0.25, t=(1, 2))\
    .to(next_state="Canned_dry_goods", p=0.25, t=(1, 2))\

SUPERMARKET_BUILDER.add_state("Fruit", p=0.0)\
    .to(next_state="Vegetables", p=0.5, t=(1, 2)) \
    .to(next_state="Meat_poultry", p=0.5, t=(1, 2))\

SUPERMARKET_BUILDER.add_state("Vegetables", p=0.0)\
    .to(next_state="Fruit", p=1, t=(1, 2)) \

SUPERMARKET_BUILDER.add_state("Meat_poultry", p=0.0)\
    .to(next_state="Canned_dry_goods", p=0.5, t=(1, 2))\
    .to(next_state="Sweets_snacks", p=0.5, t=(1, 2))\


SUPERMARKET_BUILDER.add_state("Canned_dry_goods", p=0.0) \
    .to(next_state="Meat_poultry", p=1/6, t=(1, 2)) \
    .to(next_state="Sweets_snacks", p=1/6, t=(1, 2)) \
    .to(next_state="Cash_registers", p=1/6, t=(1, 2)) \
    .to(next_state="Beverages", p=1/6, t=(1, 2)) \
    .to(next_state="Dairy_products_eggs", p=1/6, t=(1, 2)) \
    .to(next_state="Frozen_food", p=1/6, t=(1, 2)) \

SUPERMARKET_BUILDER.add_state("Dairy_products_eggs", p=0.0)\
    .to(next_state="Canned_dry_goods", p=0.5, t=(1, 2))\
    .to(next_state="Sweets_snacks", p=0.5, t=(1, 2))\

SUPERMARKET_BUILDER.add_state("Frozen_food", p=0.0) \
    .to(next_state="Dairy_products_eggs", p=1/3, t=(1, 2)) \
    .to(next_state="Canned_dry_goods", p=1/3, t=(1, 2)) \
    .to(next_state="Beverages", p=1/3, t=(1, 2)) \

SUPERMARKET_BUILDER.add_state("Beverages", p=0.0)\
    .to(next_state="Frozen_food", p=0.25, t=(1, 2))\
    .to(next_state="Canned_dry_goods", p=0.25, t=(1, 2))\
    .to(next_state="Cash_registers", p=0.25, t=(1, 2))\
    .to(next_state="Baker", p=0.25, t=(1, 2))\


SUPERMARKET_BUILDER.add_state("Baker", p=0.0)\
    .to(next_state="Beverages", p=0.5, t=(1, 2))\
    .to(next_state="Cash_registers", p=0.5, t=(1, 2))\

SUPERMARKET_BUILDER.add_state("Cash_registers", p=0.0)\
    .to("Entrance_and_exit", p=1, t=2)

