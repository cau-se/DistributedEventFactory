from abc import abstractmethod


class CountProvider:

    @abstractmethod
    def get(self) -> int:
        pass