from abc import ABC, abstractmethod


class ActivitySelectionProvider(ABC):

    @abstractmethod
    def emit_activity(self):
        pass


class ActivitySelectionProviderFactory:

    @abstractmethod
    def get_activity_provider(self) -> ActivitySelectionProvider:
        pass
