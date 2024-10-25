from abc import ABC, abstractmethod
from typing import List

from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.core.datasource_id import DataSourceId
from distributed_event_factory.provider.event.event_data import EventData

class DataSource(ABC):

    @abstractmethod
    def emit_event(self, case, activity_name, timestamp) -> None:
        pass

    @abstractmethod
    def get_event_data(self) -> EventData:
        pass

    @abstractmethod
    def get_id(self) -> DataSourceId:
        pass

    @abstractmethod
    def get_event_log(self) -> List[Event]:
        pass
