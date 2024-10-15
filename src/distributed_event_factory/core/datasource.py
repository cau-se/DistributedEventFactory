from abc import abstractmethod, ABC
from typing import List

from distributed_event_factory.core.abstract_datasource import DataSource
from distributed_event_factory.core.datasource_id import DataSourceId, START_SENSOR_ID, END_DATA_SOURCE_ID
from distributed_event_factory.core.event import StartEvent, EndEvent, Event
from distributed_event_factory.provider.event.event_data import EventData
from distributed_event_factory.provider.event.event_provider import EventDataProvider, EndEventProvider, \
    StartEventProvider
from distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider
from distributed_event_factory.provider.transition.transition.transition_provider import ChoiceTransitionProvider, \
    TransitionProvider


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
        self.event_log: List[Event] = []

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

    def get_event_log(self) -> List[Event]:
        return self.event_log
