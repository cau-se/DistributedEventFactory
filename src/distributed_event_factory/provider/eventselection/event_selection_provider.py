from abc import ABC, abstractmethod


class EventSelectionProvider(ABC):
    @abstractmethod
    def get_event_data(self):
        pass
