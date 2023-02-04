from abc import ABC, abstractmethod
from typing import Any, Generator, Type, List



class BaseSensor(ABC):
    def __init__(self, name: str):
        """
        Initialize a sensor with a name

        :param name:  name of the sensor
        """
        self.name: str = name

    def get_name(self) -> str:
        """
        Get the name of the sensor
        :return: name of the sensor
        """
        return self.name

    @abstractmethod
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

    def get_sensor_names(self) -> List[str]:
        return [v.get_name() for _,v in self.sensors.items()]
