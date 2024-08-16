from abc import abstractmethod, ABC
from typing import List

from core.event import Event, StartEvent, EndEvent, AbstractEvent
from provider.activity.eventselection.event_selection_provider import EventSelectionProvider
from provider.event.event_provider import EventDataProvider, StartEventProvider, EndEventProvider
from provider.sink.sink_provider import Sink
from core.datasource_id import DataSourceId, START_SENSOR_ID, END_DATA_SOURCE_ID
from provider.transition.transition_provider_factory import NextSensorProvider


class DataSource(ABC):

    @abstractmethod
    def emit_event(self, case, activity_name, timestamp) -> None:
        pass

    @abstractmethod
    def get_event_provider(self) -> EventDataProvider:
        pass

    @abstractmethod
    def get_id(self) -> DataSourceId:
        pass

    @abstractmethod
    def get_event_log(self) -> List[AbstractEvent]:
        pass


class StartDataSource(DataSource):

    def __init__(self, transition_provider: NextSensorProvider, sender):
        self.event_log = []
        self.transition_provider = transition_provider
        self.sender = sender

    def get_event_provider(self) -> EventDataProvider:
        return StartEventProvider()

    def emit_event(self, case, activity, timestamp) -> None:
        event = StartEvent(case)
        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self) -> tuple[int, int]:
        return 0, self.transition_provider.get_next_sensor()

    def get_id(self) -> DataSourceId:
        return START_SENSOR_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log


class EndDataSource(DataSource):

    def __init__(self, sender):
        self.event_log = []
        self.sender = sender

    def emit_event(self, case, activity, timestamp) -> None:
        event = EndEvent(case)
        self.event_log.append(event)
        self.sender.send(event)

    def get_event_provider(self) -> EventDataProvider:
        return EndEventProvider()

    def get_sensor_transition(self) -> tuple[int, int]:
        raise ValueError("There is no transition on the end datasource")

    def get_id(self) -> DataSourceId:
        return END_DATA_SOURCE_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log


class GenericDataSource(DataSource):
    def __init__(
            self,
            sensor_id: DataSourceId,
            group_id: str,
            event_provider: EventSelectionProvider,
            sender: Sink,
    ):
        self.sensor_id: DataSourceId = sensor_id
        self.group_id: str = group_id
        self.sender = sender
        self.event_provider = event_provider
        self.event_log: List[AbstractEvent] = []

    def get_id(self) -> DataSourceId:
        return self.sensor_id

    def get_event_provider(self):
        return self.event_provider

    def emit_event(self, case, activity_name, timestamp) -> None:
        event = Event(
            timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            sensor_value=activity_name,
            case_id=case,
            sensor_name=self.sensor_id.get_name(),
            group_id=self.group_id
        )
        self.event_log.append(event)
        self.sender.send(event)

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log
