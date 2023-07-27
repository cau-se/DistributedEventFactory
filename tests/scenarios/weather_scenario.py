from sensors.sensor_collection import SingleValueSensor
from sensors.sensors import SensorManager
from utils.markov_chain import MarkovChain
from utils.transition_matrix_builder import TransitionMatrixBuilder


WEATHER_SENSOR_MANAGER: SensorManager = SensorManager()
WEATHER_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Sonnig"], "Sonnig"))
WEATHER_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Bewölkt"], "Bewölkt"))
WEATHER_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Regnerisch"], "Regnerisch"))


WEATHER_TRANSITION_MATRIX = [
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.3, 0.1, 0.6],
]

