from abc import ABC, abstractmethod

class TransitionProvider(ABC):

    @abstractmethod
    def get_next_sensor(self) -> int:
        pass


class TransitionProviderFactory:

    @abstractmethod
    def get(self, number_of_sensors):
        pass
