from abc import abstractmethod, ABC
from typing import List

from src.distributed_event_factory.core.datasource_id import DataSourceId, START_SENSOR_ID, END_DATA_SOURCE_ID
from src.distributed_event_factory.core.event import AbstractEvent, StartEvent, EndEvent, Event
from src.distributed_event_factory.provider.event.event_data import EventData
from src.distributed_event_factory.provider.event.event_provider import EventDataProvider, EndEventProvider, \
    StartEventProvider
from src.distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider
from src.distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, \
    AbstractNextSensorProvider


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
    def get_event_log(self) -> List[AbstractEvent]:
        pass


class StartDataSource(DataSource):

    def __init__(self, transition_provider: AbstractNextSensorProvider):
        self.event_log = []
        self.transition_provider = transition_provider

    def get_event_data(self) -> EventDataProvider:
        return StartEventProvider(self.transition_provider).get_event_data()

    def emit_event(self, case, activity, timestamp) -> AbstractEvent:
        return StartEvent(case, self.transition_provider)

    def get_sensor_transition(self) -> tuple[int, int]:
        return 0, self.transition_provider.get_next_sensor()

    def get_id(self) -> DataSourceId:
        return START_SENSOR_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log


class EndDataSource(DataSource):

    def __init__(self):
        self.event_log = []

    def emit_event(self, case, activity, timestamp) -> None:
        event = EndEvent(case)
        self.event_log.append(event)

    def get_event_data(self) -> EventDataProvider:
        return EndEventProvider().get_event_data()

    def get_sensor_transition(self) -> tuple[int, int]:
        raise ValueError("There is no transition on the end datasource")

    def get_id(self) -> DataSourceId:
        return END_DATA_SOURCE_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log


class GenericDataSource(DataSource):
    def __init__(
            self,
            data_source_id: DataSourceId,
            group_id: str,
            event_provider: EventSelectionProvider,
    ):
        self.sensor_id: DataSourceId = data_source_id
        self.group_id: str = group_id
        self.event_provider = event_provider
        self.event_log: List[AbstractEvent] = []

    def get_id(self) -> DataSourceId:
        return self.sensor_id

    def get_event_provider(self):
        return self.event_provider

    def get_event_data(self):
        return self.event_provider.get_event_data()

    def emit_event(self, case, activity_name, timestamp) -> Event:
        event = Event(
            timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            sensor_value=activity_name,
            case_id=case,
            sensor_name=self.sensor_id.get_name(),
            group_id=self.group_id
        )
        self.event_log.append(event)
        return event

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log
