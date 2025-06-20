import string
from datetime import datetime, timedelta
from queue import PriorityQueue
from typing import Dict, List
import math

from core.datasource_id import ROUTING_ID
from core.object import Object
from core.route import Route
from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.provider.data.count_provider import CountProvider
from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID, DataSourceId
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from provider.event.event_provider import EventDataProvider
from provider.object.input.input_provider import InputObjectProvider
from simulation.object_event import ObjectEvent

CHANGE = "change"
LAST_STATE = "lastState"
NUMBER_OF_OBJECT = "numberOfObject"
OBJECT_NAME = "objectName"
Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"


class ProcessSimulator:
    def __init__(
            self,
            data_sources: Dict[str, DataSource],
            case_id_provider: CaseIdProvider,
            max_concurrent_cases: CountProvider,
            objects: Dict[str, Object],
            routes: Dict[str, Route],
            stocks: Dict[str, InputObjectProvider]
    ):

        self.max_concurrent_cases = max_concurrent_cases
        # Add all interactions with token to the token class
        self.tokens: PriorityQueue[Token] = PriorityQueue()
        self.datasources: Dict[str, DataSource] = data_sources
        self.case_id_provider: CaseIdProvider = case_id_provider
        self.last_timestamp = datetime.now()

        # Refactor to one own class, two methods get_objects, get_object_count
        self.object_store: Dict[str, int] = {}
        self.object_store_objects: List[Object] = []

        self.objects: Dict[str, Object] = objects
        self.routes: Dict[str, Route] = routes
        self.stocks: Dict[str, InputObjectProvider] = stocks

        # Are that also objects?
        self.orders: List[str] = []
        self.add_configured_stocks_in_warehouse(self.last_timestamp)
        self.buffered_events = []

    def simulate(self) -> Event:
        if not self.buffered_events:
            new_events = self.simulate_next_steps()
            self.buffered_events = new_events
        return self.buffered_events.pop()

    def simulate_next_steps(self) -> List[Event]:
        emit_event = []

        # Potentially get stuck if no emit_event found
        while not emit_event:
            if len(self.tokens.queue) < self.max_concurrent_cases.get():
                token = self.start_new_case()
            else:
                token = self.tokens.get()

            if token.event:
                emit_event.append(token.event)

            if token.data_source_id == END_DATA_SOURCE_ID:
                token = self.start_new_case()

            if token.data_source_id == START_SENSOR_ID:
                # Only one start allowed
                token.data_source_id = DataSourceId(
                    self._get_sensor_with_id(START_SENSOR_ID).get_event_data()[0].get_transition())
                # TODO create different product orders (at the moment not used)
                orderObject = self.objects.get("woodShelf")
                self.orders.append(orderObject)
                self.append_order(orderObject)
            current_data_source = self._get_sensor_with_id(token.data_source_id)
            event = current_data_source.get_event_data()
            if type(event) is list:
                for e in event:
                    self.inner_simulation_per_event(current_data_source, e, token)
            else:
                self.inner_simulation_per_event(current_data_source, event, token)

        return emit_event

    #
    def inner_simulation_per_event(self, current_data_source, event, token):
        required_input_objects = current_data_source.event_provider.input_objects # type parser is a weird word

        # This line can be nicer after the refactoring to an object class
        if not self.check_input_in_object_store(required_input_objects):
            activity, current_data_source, required_input_objects, next_datasource, output = self.set_parameters_for_previous_event(
                current_data_source, required_input_objects, token)
        else:
            next_datasource = event.get_transition()
            activity = event.get_activity_provider().get_activity()
            output = event.get_activity_provider().get_output()

        # to object store class
        input_objects = self.remove_used_input(required_input_objects)
        token.add_to_last_timestamp(event.get_duration())
        self.last_timestamp = token.last_timestamp
        self.add_produced_output(output, required_input_objects, input_objects, self.last_timestamp)
        if (required_input_objects is not None and required_input_objects) or output is not None:
            token.event = self._build_event(token.case, activity, self.last_timestamp, current_data_source,
                                            required_input_objects, output)
        else:
            token.event = self._build_event(token.case, activity, self.last_timestamp, current_data_source)
        self.set_next_datasource_token(activity, current_data_source, next_datasource, token)
        self.add_tokens(activity, current_data_source, next_datasource, output, token)

    def start_new_case(self):
        case_id = self.case_id_provider.get()
        token = Token(case_id, START_SENSOR_ID, self.last_timestamp, None)
        return token

    def _build_event(self, case, activity, timestamp, datasource, input=None, output=None):
        if hasattr(datasource, "sensor_id"):
            if input and output:
                return ObjectEvent(
                    timestamp=timestamp.strftime(Y_M_D_H_M_S),
                    activity=activity,
                    case_id=case,
                    node=datasource.sensor_id.get_name(),
                    group_id=datasource.group_id,
                    input=", ".join(str(obj) for obj in input),
                    output=", ".join(str(obj) for obj in output)
                )
            else:
                return Event(
                    timestamp=timestamp.strftime(Y_M_D_H_M_S),
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

    def append_order(self, orderObject):
        if orderObject.input_objects:
            for input in orderObject.input_objects:
                for i in range(0, input.numberOfObject):
                    self.orders.append(self.objects.get(input.objectName))
                self.append_order(self.objects.get(input.objectName))

    def check_input_in_object_store(self, necessary_inputs):
        for obj in necessary_inputs:
            if type(obj) is not Dict:
                obj = eval(str(obj))
            if obj.get(LAST_STATE):
                if not self.object_store.__contains__(obj.get(OBJECT_NAME)) or self.object_store.get(
                        obj.get(OBJECT_NAME)) < obj.get(NUMBER_OF_OBJECT) or sum(
                    1 for stored_obj in self.object_store_objects if
                    stored_obj.object_id.id == obj.get(OBJECT_NAME) and stored_obj.get_last_changed_value() == obj.get(
                        LAST_STATE)) < obj.get(NUMBER_OF_OBJECT):
                    return False
            elif not self.object_store.__contains__(obj.get(OBJECT_NAME)) or self.object_store.get(
                    obj.get(OBJECT_NAME)) < obj.get(NUMBER_OF_OBJECT) or sum(
                1 for stored_obj in self.object_store_objects if
                stored_obj.object_id.id == obj.get(OBJECT_NAME) and not stored_obj.values_changed) < obj.get(
                NUMBER_OF_OBJECT):
                return False
        return True

    def add_configured_stocks_in_warehouse(self, timestamp):
        if not self.stocks:
            return
        for stock in self.stocks.get("default"):
            for i in range(stock.numberOfObject):
                if stock.lastState:
                    obj = self.objects.get(stock.objectName).clone()
                    obj.add_change(Object(timestamp=timestamp.strftime(Y_M_D_H_M_S), object_state=stock.lastState,
                                          object_id=obj.object_id))
                    self.object_store_objects.append(obj)
                else:
                    self.object_store_objects.append(self.objects.get(stock.objectName).clone())
            self.object_store[stock.objectName] = stock.numberOfObject

    def set_parameters_for_previous_event(self, current_data_source, necessary_input, token):
        next_datasource = token.event.node
        activity = token.event.activity
        output = eval(token.event.output)
        if str(output).count(OBJECT_NAME) == 1:
            output = [output]
        necessary_input = eval(token.event.input)
        if str(necessary_input).count(OBJECT_NAME) == 1:
            necessary_input = [necessary_input]
        current_data_source = self.datasources.get(token.event.node)
        if not self.check_input_in_object_store(necessary_input):
            raise ValueError("Input not found", necessary_input)
        return activity, current_data_source, necessary_input, next_datasource, output

    def set_next_datasource_token(self, activity, current_data_source, next_datasource, token):
        if next_datasource == ROUTING_ID.get_name():
            start_point = current_data_source.sensor_id.id

            # This is for many route files, currently only one route is configured
            for route in self.routes.get("default"):
                # Consider using a dictionary where activity
                if route.get_route_for_activity() == activity and route.get_start() == start_point:
                    token.add_to_last_timestamp(route.get_duration())
                    next_datasource = route.get_end()
                    token.set_data_source_id(self.datasources[next_datasource].get_id())
                    return
        else:
            token.set_data_source_id(self.datasources[next_datasource].get_id())

    def add_produced_output(self, output, necessary_input, input_objects, timestamp):
        if output is not None:
            for element in output:
                if type(element) is not Dict:
                    element = eval(str(element))
                if self.object_store.get(element.get(OBJECT_NAME)) is None:
                    self.object_store[element.get(OBJECT_NAME)] = element.get(NUMBER_OF_OBJECT)
                else:
                    self.object_store[element.get(OBJECT_NAME)] = self.object_store.get(
                        element.get(OBJECT_NAME)) + element.get(NUMBER_OF_OBJECT)
                self.add_output_to_object_store_objects(element, input_objects, necessary_input, timestamp)

    def add_output_to_object_store_objects(self, element, input_objects, necessary_input, timestamp):
        for i in range(0, element.get(NUMBER_OF_OBJECT)):
            input_for_element = self.find_in_list_input_list(input_objects, element.get(OBJECT_NAME))
            if input_for_element:
                if (element.get(CHANGE)):
                    input_info = self.find_in_necessary_input(necessary_input, element.get(OBJECT_NAME))
                    output_object = self.find_in_list_with_change_state(input_objects, element.get(OBJECT_NAME),
                                                                        input_info.lastState)
                    self.add_object_to_object_store_objects_with_change(element, output_object, timestamp)
                else:
                    self.object_store_objects.append(input_objects.get(input_objects.index(element.get(OBJECT_NAME))))
            else:
                if (element.get(CHANGE)):
                    output_object = self.objects.get(element.get(OBJECT_NAME)).clone()
                    self.add_object_to_object_store_objects_with_change(element, output_object, timestamp)
                else:
                    self.object_store_objects.append(self.objects.get(element.get(OBJECT_NAME)))

    def add_object_to_object_store_objects_with_change(self, element, output_object, timestamp):
        output_object.add_change(
            Object(
                timestamp=timestamp.strftime(Y_M_D_H_M_S),
                object_state=element.get(CHANGE),
                object_id=output_object.object_id)
        )
        self.object_store_objects.append(
            output_object)

    def remove_used_input(self, necessary_input):
        if necessary_input is not None:
            input_objects = []
            for element in necessary_input:
                if type(element) is not Dict:
                    element = eval(str(element))
                self.object_store[element.get(OBJECT_NAME)] = self.object_store.get(
                    element.get(OBJECT_NAME)) - element.get(NUMBER_OF_OBJECT)
                if self.object_store.get(element.get(OBJECT_NAME)) == 0:
                    self.object_store.pop(element.get(OBJECT_NAME))

                self.remove_input_from_object_store_objects(element, input_objects)
            return input_objects
        return None

    def remove_input_from_object_store_objects(self, element, input_objects):
        for i in range(0, element.get(NUMBER_OF_OBJECT)):
            if (element.get(LAST_STATE)):
                object_from_store_index = self.object_store_objects.index(
                    self.find_in_list_with_change_state(self.object_store_objects, element.get(OBJECT_NAME),
                                                        element.get(LAST_STATE)))
            else:
                object_from_store_index = self.object_store_objects.index(
                    self.find_in_list_without_changed_value(self.object_store_objects, element.get(OBJECT_NAME)))
            input_obj = self.object_store_objects.pop(object_from_store_index)
            input_objects.append(input_obj)

    def add_tokens(self, activity, current_data_source, next_datasource, output, token):
        if self.objects:
            number_of_tokens = self.tokens.qsize()
            input_of_following_event = self._get_sensor_with_id(token.data_source_id)
            first_output = output[0]
            if type(first_output) is not Dict:
                first_output = eval(str(first_output))

            if not isinstance(input_of_following_event, EndDataSource) and str(
                    first_output.get(OBJECT_NAME)) != "order":
                input_of_following_event = input_of_following_event.event_provider.input_objects
                for output_elem in output:
                    if type(output_elem) is not Dict:
                        output_elem = eval(str(output_elem))
                    if self.find_in_necessary_input(input_of_following_event, output_elem.get(OBJECT_NAME)):
                        num_of_input_following_event = self.find_in_necessary_input(input_of_following_event,
                                                                                    output_elem.get(
                                                                                        OBJECT_NAME)).numberOfObject

                        if output_elem.get(NUMBER_OF_OBJECT) > num_of_input_following_event:
                            self.set_next_datasource_token(activity, current_data_source, next_datasource, token)
                            output_input_factor = math.ceil(
                                output_elem.get(NUMBER_OF_OBJECT) / num_of_input_following_event)
                            event_data = self.datasources[next_datasource].get_event_data()
                            if type(event_data) is list and len(event_data) == 1:
                                duration_following_activity = event_data[0].get_duration()
                            elif type(event_data) is EventDataProvider:
                                duration_following_activity = event_data.get_duration()
                            else:
                                raise ValueError("Duration not known, multiple events after loop of events")
                            for x in range(output_input_factor):
                                if x != 0:
                                    token.event = None
                                token.add_to_last_timestamp(x * duration_following_activity)
                                self.tokens.put(token.clone())
            if number_of_tokens == self.tokens.qsize():
                self.tokens.put(token)
        else:
            self.tokens.put(token)

    def find_in_necessary_input(self, necessary_input, key):
        return next((item for item in necessary_input if item.objectName == key), None)

    def find_in_list_input_list(self, data, key):
        return next((item for item in data if item.object_id.id == key), None)

    def find_in_list_without_changed_value(self, data, key):
        return next((item for item in data if item.object_id.id == key and not item.values_changed), None)

    def find_in_list_with_change_state(self, data, key, change_value):
        return next(
            (item for item in data if item.object_id.id == key and item.get_last_changed_value() == change_value), None)


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

    def clone(self):
        return Token(self.case,
                     self.data_source_id,
                     self.last_timestamp,
                     self.event)
