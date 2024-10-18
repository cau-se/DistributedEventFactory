import random
import string
from datetime import datetime, timedelta
from typing import List

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID, DataSourceId
from distributed_event_factory.core.event import Event
from distributed_event_factory.provider.data.case_provider import CaseIdProvider

class ProcessSimulator:
    def __init__(
            self,
            data_sources: List[DataSource],
            case_id_provider: CaseIdProvider):
        self.tokens: List[Token] = []
        self.sensors: List[DataSource] = data_sources
        self.case_id_provider = case_id_provider
        self.last_time = datetime.now()
        self.i = 0

    def simulate(self) -> Event:
        if not self.tokens:
            case_id = self.case_id_provider.get()
            self.tokens.append(Token(case_id, START_SENSOR_ID, self.last_time))

        token = self.tokens[int(random.uniform(0, len(self.tokens)))]
        current_data_source = self._get_sensor_with_id(token.data_source_id)
        event = current_data_source.get_event_provider().get_event_data()
        next_datasource = event.get_transition()

        if token.data_source_id == END_DATA_SOURCE_ID:
            event=current_data_source.emit_event(token.case, event.get_activity(), token.last_timestamp)
            self.tokens.remove(token)
            return event
        else:
            activity = event.get_activity()
            token.add_to_last_timestamp(duration=event.get_duration())
            last_timestamp = token.last_timestamp
            event = current_data_source.emit_event(token.case, activity, last_timestamp)
            self.last_time = last_timestamp
            token.set_data_source_id(self.sensors[next_datasource + 1].get_id())
            return event

    def _get_sensor_with_id(self, sensor_id) -> DataSource:
        for sensor in self.sensors:
            if sensor.get_id() == sensor_id:
                return sensor
        raise ValueError("Sensor not found")


class Token:
    def __init__(
            self,
            case: string,
            data_source_id: DataSourceId,
            last_timestamp: datetime
    ):
        self.case = case
        self.data_source_id = data_source_id
        self.last_timestamp = last_timestamp

    def set_data_source_id(self, data_source_id):
        self.data_source_id = data_source_id

    def add_to_last_timestamp(self, duration):
        self.last_timestamp += timedelta(minutes=duration)
