from abc import ABC, abstractmethod
from typing import Any, Generator, Type, List



class BaseSensor(ABC):
    def __init__(self, name: str):
        """
        Initialize a datasource with a name

        :param name:  name of the datasource
        """
        self.name: str = name

    def get_name(self) -> str:
        """
        Get the name of the datasource
        :return: name of the datasource
        """
        return self.name

    @abstractmethod
    def get_data(self) -> Generator[Any, Any, Any]:
        pass

class SensorManager:
    def __init__(self):
        """
        Initialize an empty datasource manager
        """
        self.sensors: dict[str, BaseSensor] = {}
        pass

    def add_sensor(self, sensor: BaseSensor):
        """
        Add a datasource to the manager
        :param sensor: datasource to add
        """
        self.sensors[sensor.get_name()] = sensor

    def get_sensor(self, name: str) -> BaseSensor:
        """
        Get a datasource by name

        :param name: name of the datasource to retrieve
        :return: datasource with the given name, or None if it doesn't exist
        """
        return self.sensors.get(name, None)

    def get_sensor_names(self) -> List[str]:
        return [v.get_name() for _,v in self.sensors.items()]

    def get_sensors(self) -> List[BaseSensor]:
        return [v for _,v in self.sensors.items()]