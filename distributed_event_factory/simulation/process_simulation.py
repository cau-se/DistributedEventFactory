import string
from datetime import datetime, timedelta
from queue import PriorityQueue
from typing import Dict, List

from core.datasource_id import ROUTING_ID
from core.object import Object
from core.route import Route
from distributed_event_factory.provider.data.count_provider import CountProvider
from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID, DataSourceId
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from simulation.object_event import ObjectEvent


class ProcessSimulator:
    def __init__(
            self,
            data_sources: Dict[str, DataSource],
            case_id_provider: CaseIdProvider,
            max_concurrent_cases: CountProvider,
            objects: Dict[str, Object],
            routes: Dict[str, Route]
    ):

        self.max_concurrent_cases = max_concurrent_cases
        self.tokens: PriorityQueue[Token] = PriorityQueue(self.max_concurrent_cases.get())
        self.datasources: Dict[str, DataSource] = data_sources
        self.case_id_provider = case_id_provider
        self.last_timestamp = datetime.now()
        self.object_store: Dict[str, int] = {}
        self.object_store_objects: List[Object] = []
        self.objects = objects
        self.routes = routes
        self.add_start_supplies_in_warehouse(self.last_timestamp)

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
                token.data_source_id = DataSourceId(
                    self._get_sensor_with_id(START_SENSOR_ID).get_event_data().get_transition())
            current_data_source = self._get_sensor_with_id(token.data_source_id)
            event = current_data_source.get_event_data()
            necessary_input = current_data_source.event_provider.type_parser
            if not self.check_input_in_object_store(necessary_input):
                next_datasource = token.event.node
                activity = token.event.activity
                output = eval(token.event.output)
                if str(output).count("objectName") ==1:
                    output = [output]
                necessary_input = eval(token.event.input)
                if str(necessary_input).count("objectName") == 1:
                    necessary_input = [necessary_input]
                current_data_source = self.datasources.get(token.event.node)
                if not self.check_input_in_object_store(necessary_input):
                    raise ValueError("Input not found")
            else:
                next_datasource = event.get_transition()
                activity = event.get_activity_provider().get_activity()
                output = event.get_activity_provider().get_output()
            input_objects = self.remove_used_input(necessary_input)
            self.set_next_datasource_token(activity, current_data_source, next_datasource, token)
            token.add_to_last_timestamp(event.get_duration())
            self.last_timestamp = token.last_timestamp
            self.add_produced_output(output, necessary_input, input_objects, self.last_timestamp)
            if (necessary_input is not None and necessary_input) or output is not None:
                token.event = self._build_event(token.case, activity, self.last_timestamp, current_data_source,
                                                necessary_input, output)

            else:
                token.event = self._build_event(token.case, activity, self.last_timestamp, current_data_source)
            self.tokens.put(token)

        return emit_event

    def set_next_datasource_token(self, activity, current_data_source, next_datasource, token):
        if next_datasource == ROUTING_ID.get_name():
            start_point = current_data_source.sensor_id.id
            for route in self.routes.get("default"):
                if route.get_route_for_activity() == activity and route.get_start() == start_point:
                    token.add_to_last_timestamp(route.get_duration())
                    next_datasource = route.get_end()
                    token.set_data_source_id(self.datasources[next_datasource].get_id())
                    return
        else:
            token.set_data_source_id(self.datasources[next_datasource].get_id())

    def add_start_supplies_in_warehouse(self, timestamp):
        self.object_store["order"] = 100
        self.object_store["barResource"] = 100
        self.object_store["screw"] = 500
        self.object_store["bar"] = 150
        for i in range(100):
            self.object_store_objects.append(self.objects.get("order").clone())
            self.object_store_objects.append(self.objects.get("barResource").clone())

        for i in range(150):
            obj = self.objects.get("bar").clone()
            obj.add_change(Object(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"), object_state="sanded",
                                  object_id=obj.object_id))
            self.object_store_objects.append(obj)

        for i in range(500):
            self.object_store_objects.append(self.objects.get("screw").clone())

    def add_produced_output(self, output, necessary_input, input_objects, timestamp):
        if output is not None:
            for element in output:
                if type(element) is not Dict:
                    element = eval(str(element))
                if self.object_store.get(element.get("objectName")) is None:
                    self.object_store[element.get("objectName")] = element.get("numberOfObject")
                else:
                    self.object_store[element.get("objectName")] = self.object_store.get(
                        element.get("objectName")) + element.get("numberOfObject")
                for i in range(0, element.get("numberOfObject")):
                    input_for_element = self.find_in_list_input_list(input_objects, element.get("objectName"))
                    if input_for_element:
                        if (element.get("change")):
                            input_info = self.find_in_necessary_input(necessary_input, element.get("objectName"))
                            output_object = self.find_in_list_input_list_with_state(input_objects, element.get("objectName"),
                                                                         input_info.lastState)
                            output_object.add_change(
                                Object(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"), object_state=element.get("change"),
                                       object_id=output_object.object_id))
                            self.object_store_objects.append(
                                output_object)
                        else:
                            self.object_store_objects.append(input_objects.get(input_objects.index(element.get("objectName"))))
                    else:
                        if (element.get("change")):
                            output_object = self.objects.get(element.get("objectName")).clone()
                            output_object.add_change(
                                Object(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"), object_state=element.get("change"),
                                       object_id=output_object.object_id))
                            self.object_store_objects.append(output_object)
                        else:
                            self.object_store_objects.append(self.objects.get(element.get("objectName")))

    def find_in_list_input_list_with_state(self, data, key, change_value):
        return next((item for item in data if item.object_id.id == key and item.get_last_changed_value() == change_value), None)

    def find_in_necessary_input(self, necessary_input, key):
        return next((item for item in necessary_input if item.objectName == key), None)

    def find_in_list_input_list(self, data, key):
        return next((item for item in data if item.object_id.id == key), None)

    def find_in_list_without_changed_value(self, data, key):
        return next((item for item in data if item.object_id.id == key and not item.values_changed), None)

    def find_in_list(self, data, key, change_value):
        return next(
            (item for item in data if item.object_id.id == key and item.get_last_changed_value() == change_value), None)

    def remove_used_input(self, necessary_input):
        if necessary_input is not None:
            input_objects = []
            for element in necessary_input:
                if type(element) is not Dict:
                    element = eval(str(element))
                self.object_store[element.get("objectName")] = self.object_store.get(
                    element.get("objectName")) - element.get("numberOfObject")
                if self.object_store.get(element.get("objectName")) == 0:
                    self.object_store.pop(element.get("objectName"))

                for i in range(0, element.get("numberOfObject")):
                    if (element.get("lastState")):
                        object_from_store_index = self.object_store_objects.index(
                            self.find_in_list(self.object_store_objects, element.get("objectName"), element.get("lastState")))
                        input_obj =self.object_store_objects.pop(object_from_store_index)
                        input_objects.append(input_obj)
                    else:
                        object_from_store_index = self.object_store_objects.index(self.find_in_list_without_changed_value(self.object_store_objects, element.get("objectName")))
                        input_obj = self.object_store_objects.pop(object_from_store_index)
                        input_objects.append(input_obj)
            return input_objects
        return None

    def start_new_case(self):
        case_id = self.case_id_provider.get()
        token = Token(case_id, START_SENSOR_ID, self.last_timestamp, None)
        return token

    def _build_event(self, case, activity, timestamp, datasource, input=None, output=None):
        if hasattr(datasource, "sensor_id"):
            if input and output:
                return ObjectEvent(
                    timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    activity=activity,
                    case_id=case,
                    node=datasource.sensor_id.get_name(),
                    group_id=datasource.group_id,
                    input=", ".join(str(obj) for obj in input),
                    output=", ".join(str(obj) for obj in output)
                )
            else:
                return Event(
                    timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    activity=activity,
                    case_id=case,
                    node=datasource.sensor_id.get_name(),
                    group_id=datasource.group_id
                )
        return None

    def _get_sensor_with_id(self, data_source_id) -> DataSource:
        for sensor in self.datasources:
            if self.datasources[sensor].get_id() == data_source_id:
                return self.datasources[sensor]
        raise ValueError("Sensor not found")

    def check_input_in_object_store(self, necessary_inputs):
        for obj in necessary_inputs:
            if type(obj) is not Dict:
                obj = eval(str(obj))
            if obj.get("lastState"):
                if not self.object_store.__contains__(obj.get("objectName")) or self.object_store.get(
                        obj.get("objectName")) < obj.get("numberOfObject") or sum(1 for stored_obj in self.object_store_objects if
                                                                    stored_obj.object_id.id == obj.get("objectName") and stored_obj.get_last_changed_value() == obj.get("lastState")) < obj.get("numberOfObject"):
                    return False
            elif not self.object_store.__contains__(obj.get("objectName")) or self.object_store.get(
                    obj.get("objectName")) < obj.get("numberOfObject") or sum(1 for stored_obj in self.object_store_objects if
                                                                stored_obj.object_id.id == obj.get("objectName") and not stored_obj.values_changed) < obj.get("numberOfObject"):
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
