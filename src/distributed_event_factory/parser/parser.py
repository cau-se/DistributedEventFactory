from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def add_dependency(self, key: str, dependency):
        pass

    @abstractmethod
    def parse(self, config):
        pass