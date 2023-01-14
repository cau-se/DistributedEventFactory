from abc import ABC
from typing import Any, Generator


#
class BaseSensor(ABC):
    name: str
    def __init__(self, name: str):
        """
        Initialize a sensor with a name

        :param name:  name of the sensor
        """
        self.name = name

    def get_name(self) -> str:
        """
        Get the name of the sensor
        :return: name of the sensor
        """
        return self.name

    def get_data(self) ->  Generator[Any, Any, Any]:
        pass

class SensorManager:
    sensors: dict[str, BaseSensor] = {}
    def __init__(self):
        """
        Initialize an empty sensor manager
        """
        pass

    def add_sensor(self, sensor: BaseSensor):
        """
        Add a sensor to the manager
        :param sensor: sensor to add
        """
        self.sensors[sensor.get_name()] = sensor

    def get_sensor(self, name: str) -> BaseSensor:
        """
        Get a sensor by name

        :param name: name of the sensor to retrieve
        :return: sensor with the given name, or None if it doesn't exist
        """
        return self.sensors.get(name, None)