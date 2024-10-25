import random
import string
from datetime import datetime, timedelta
from typing import List, Dict

from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID, DataSourceId
from distributed_event_factory.provider.data.case_provider import CaseIdProvider

class ProcessSimulator:
    def __init__(
            self,
            data_sources: Dict[str, DataSource],
            case_id_provider: CaseIdProvider):

        self.tokens: List[Token] = []
        self.datasources: Dict[str, DataSource] = data_sources
        self.case_id_provider = case_id_provider
        self.last_timestamp = datetime.now()

    def simulate(self) -> Event:
        if not self.tokens:
            token = self.start_new_case()
        else:
            token = self.tokens[int(random.uniform(0, len(self.tokens)))]

        if token.data_source_id == END_DATA_SOURCE_ID:
            self.tokens.remove(token)
            token = self.start_new_case()

        if token.data_source_id == START_SENSOR_ID:
            token.data_source_id = DataSourceId(self._get_sensor_with_id(START_SENSOR_ID).get_event_data().get_transition())

        current_data_source = self._get_sensor_with_id(token.data_source_id)
        event = current_data_source.get_event_data()
        next_datasource = event.get_transition()
        activity = event.get_activity()
        token.add_to_last_timestamp(event.get_duration())
        token.set_data_source_id(self.datasources[next_datasource].get_id())
        self.last_timestamp = token.last_timestamp
        return self._build_event(token.case, activity, self.last_timestamp, current_data_source)

    def start_new_case(self):
        case_id = self.case_id_provider.get()
        token = Token(case_id, START_SENSOR_ID, self.last_timestamp)
        self.tokens.append(token)
        return token

    def _build_event(self, case, activity, timestamp, datasource):
        if hasattr(datasource, "sensor_id"):
            return Event(
                timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                activity=activity,
                case_id=case,
                node=datasource.sensor_id.get_name(),
                group_id=datasource.group_id
            )

    def _get_sensor_with_id(self, data_source_id) -> DataSource:
        for sensor in self.datasources:
            if self.datasources[sensor].get_id() == data_source_id:
                return self.datasources[sensor]
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
