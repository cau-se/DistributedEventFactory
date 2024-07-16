import random
import datetime
from abc import ABC, abstractmethod
from typing import Generator, Any, List
from sensors.sensors import BaseSensor


# Physical datasource
class TemperatureSensor(BaseSensor):
    def __init__(self, name: str = "Temperature_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            temperature = random.uniform(-50, 50)
            yield temperature


# Chemical datasource
class GasSensor(BaseSensor):
    def __init__(self, name: str = "Gas_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            gas_concentration = random.uniform(0, 100)
            yield gas_concentration


# Biological datasource
class BioSensor(BaseSensor):
    def __init__(self, name: str = "Bio_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            organism_activity = random.uniform(0, 1)
            yield organism_activity


# Optical datasource
class CameraSensor(BaseSensor):

    def __init__(self, width: int, height: int, name: str = "Camera_Sensor"):
        super().__init__(name)
        self.width: int = width
        self.height: int = height

    def get_data(self) -> Generator[list[tuple[int, int, int]], Any, None]:
        while True:
            pixels = []
            for i in range(self.width * self.height):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                pixels.append((r, g, b))
            yield pixels


# Motion datasource
class AccelerometerSensor(BaseSensor):
    def __init__(self, name: str = "Accelerometer_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[tuple[float, float, float], Any, None]:
        while True:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            z = random.uniform(-1, 1)
            yield x, y, z


# Audio datasource
class AudioSensor(BaseSensor):
    def __init__(self, name: str = "Audio_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            sound_level = random.uniform(0, 1)
            yield sound_level


# Pressure datasource
class PressureSensor(BaseSensor):
    def __init__(self, name: str = "Pressure_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            pressure = random.uniform(0, 1000)
            yield pressure


# Proximity datasource
class InfraredSensor(BaseSensor):
    def __init__(self, name: str = "Infrared_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[float, Any, None]:
        while True:
            pressure = random.uniform(-273.15, 1000)
            yield pressure


# Wifi sensors.py
class WifiSensor(BaseSensor):
    def __init__(self, name: str = "Wifi_Sensor"):
        super().__init__(name)

    def get_data(self) -> Generator[tuple[str, int], Any, None]:
        while True:
            mac_address = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
            signal_strength = random.randint(-100, -30)
            yield mac_address, signal_strength


# List Sensors
class SingleValueSensor(BaseSensor):

    def __init__(self, elements: List[str], name: str = "Single_Value_Sensor"):
        super().__init__(name)
        self.elements: List[str] = elements

    def get_data(self) -> Generator[Any, Any, None]:
        while True:
            yield random.choice(self.elements)
