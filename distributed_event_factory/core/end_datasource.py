from typing import List

from distributed_event_factory.provider.event.event_data_case_provider import EventDataProvider, EndEventProvider
from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.core.abstract_datasource import DataSource
from distributed_event_factory.core.datasource_id import END_DATA_SOURCE_ID, DataSourceId
from distributed_event_factory.core.event import EndEvent


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

    def get_event_log(self) -> List[Event]:
        return self.event_log

    #def get_input_objects(self):
    #    return InputObjectProvider().get_input_objects()