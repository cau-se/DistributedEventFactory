import random
import datetime
from typing import Generator, Any, List

from sensors.sensors import BaseSensor


# Physical sensor

class TemperatureSensor(BaseSensor):
    def __init__(self):
        super().__init__("Temperature_Sensor")

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            temperature = random.uniform(-50, 50)
            yield temperature

# Chemical sensor

class GasSensor(BaseSensor):
    def __init__(self):
        super().__init__("Gas_Sensor")

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            gas_concentration = random.uniform(0, 100)
            yield gas_concentration

# Biological sensor
class BioSensor(BaseSensor):
    def __init__(self):
        super().__init__("Bio_Sensor")

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            organism_activity = random.uniform(0, 1)
            yield organism_activity

# Optical sensor

class CameraSensor(BaseSensor):
    width: int
    height: int
    def __init__(self, width: int, height: int):
        super().__init__("Camera_Sensor")
        self.width = width
        self.height = height

    def get_data(self) ->  Generator[list[tuple[int, int, int]], Any, None]:
        while True:
            pixels = []
            for i in range(self.width * self.height):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                pixels.append((r, g, b))
            yield pixels

# Motion sensor

class AccelerometerSensor(BaseSensor):
    def __init__(self):
        super().__init__("Accelerometer_Sensor")

    def get_data(self) ->  Generator[tuple[float, float, float], Any, None]:
        while True:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            z = random.uniform(-1, 1)
            yield (x, y, z)
# Audio sensor
class AudioSensor(BaseSensor):
    def __init__(self):
        super().__init__("Audio_Sensor")

    def get_data(self) ->   Generator[float, Any, None]:
        while True:
            sound_level = random.uniform(0, 1)
            yield sound_level

# Pressure sensor

class PressureSensor(BaseSensor):
    def __init__(self):
        super().__init__("Pressure_Sensor")

    def get_data(self) ->    Generator[float, Any, None]:
        while True:
            pressure = random.uniform(0, 1000)
            yield pressure

# Proximity sensor
class InfraredSensor(BaseSensor):
    def __init__(self):
        super().__init__("Infrared_Sensor")

    def get_data(self) ->    Generator[float, Any, None]:
        while True:
            pressure = random.uniform(0, 1000)
            yield pressure

# Wifi sensors.py

class WifiSensor(BaseSensor):
    def __init__(self):
        super().__init__("Wifi_Sensor")

    def get_data(self) -> Generator[tuple[str, int], Any, None]:
        while True:
            mac_address = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
            signal_strength = random.randint(-100, -30)
            yield mac_address, signal_strength


# List Sensors
class SingleValueSensor(BaseSensor):
    elements: List[str] 
    def __init__(self, elements):
        super().__init__("Wifi_Sensor")
        self.elements = elements

    def get_data(self) ->  Generator[Any, Any, None]:
        while True:
            yield random.choice(self.elements)
