import string
from datetime import datetime, timedelta
from queue import PriorityQueue
from typing import Dict

from distributed_event_factory.provider.data.count_provider import CountProvider
from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID, DataSourceId
from distributed_event_factory.provider.data.case_provider import CaseIdProvider

class ProcessSimulator:
    def __init__(
            self,
            data_sources: Dict[str, DataSource],
            case_id_provider: CaseIdProvider,
            max_concurrent_cases: CountProvider
    ):

        self.max_concurrent_cases = max_concurrent_cases
        self.tokens: PriorityQueue[Token] = PriorityQueue(self.max_concurrent_cases.get())
        self.datasources: Dict[str, DataSource] = data_sources
        self.case_id_provider = case_id_provider
        self.last_timestamp = datetime.now()
        self.object_store: Dict[str, int] = {}

    def simulate(self) -> Event:
        emit_event = None
        while not emit_event:
            if len(self.tokens.queue) < self.max_concurrent_cases.get():
                token = self.start_new_case()
            else:
                token = self.tokens.get()

            emit_event = token.event
            if token.data_source_id == END_DATA_SOURCE_ID:
                token = self.start_new_case()

            if token.data_source_id == START_SENSOR_ID:
                token.data_source_id = DataSourceId(self._get_sensor_with_id(START_SENSOR_ID).get_event_data().get_transition())
                self.object_store["order"] = 1
                self.object_store["bar"] = 100
                self.object_store["screw"] = 100
            current_data_source = self._get_sensor_with_id(token.data_source_id)
            event = current_data_source.get_event_data()
            necessary_input = current_data_source.event_provider.type_parser
            if not self.check_input_in_object_store(necessary_input):
                raise ValueError("Input not found")
            next_datasource = event.get_transition()
            activity = event.get_activity_provider().get_activity()
            output = event.get_activity_provider().get_output()
            if necessary_input is not None:
                for element in necessary_input:
                    self.object_store[element.objectName] = self.object_store.get(element.objectName)-element.numberOfObject
                    if self.object_store.get(element.objectName) == 0:
                        self.object_store.pop(element.objectName)
            if output is not None:
                for element in output :
                    self.object_store[element.objectName] = element.numberOfObject
            token.add_to_last_timestamp(event.get_duration())
            token.set_data_source_id(self.datasources[next_datasource].get_id())
            self.last_timestamp = token.last_timestamp
            token.event = self._build_event(token.case, activity, self.last_timestamp, current_data_source)
            self.tokens.put(token)

        return emit_event

    def start_new_case(self):
        case_id = self.case_id_provider.get()
        token = Token(case_id, START_SENSOR_ID, self.last_timestamp, None)
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
    
    def check_input_in_object_store(self, input_objects):
        for obj in input_objects:
            if not self.object_store.__contains__(obj.objectName) or self.object_store.get(obj.objectName) is not obj.numberOfObject :
                return False
        return True


class Token:
    def __init__(
            self,
            case: string,
            data_source_id: DataSourceId,
            last_timestamp: datetime,
            event: Event
    ):
        self.case = case
        self.data_source_id = data_source_id
        self.last_timestamp = last_timestamp
        self.event = event

    def set_data_source_id(self, data_source_id):
        self.data_source_id = data_source_id

    def add_to_last_timestamp(self, duration):
        self.last_timestamp += timedelta(minutes=duration)

    def __lt__(self, other):
        return self.last_timestamp < other.last_timestamp