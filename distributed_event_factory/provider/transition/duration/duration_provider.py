from abc import abstractmethod

class DurationProvider:

    @abstractmethod
    def get_duration(self):
        pass