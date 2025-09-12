from datetime import datetime
from typing import List, Dict

from distributed_event_factory.core.abstract_datasource import DataSource
from distributed_event_factory.core.datasource_id import DataSourceId
from distributed_event_factory.core.object import ObjectData
from distributed_event_factory.core.route import Route
from distributed_event_factory.core.workforce import Workforce
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.provider.workforce.InputWorkforceProvider import WorkforceStartPositionProvider
from distributed_event_factory.simulation.simulator_objects.object_storage import ObjectStorage
from distributed_event_factory.simulation.simulator_objects.object_utility import ObjectUtility
from distributed_event_factory.simulation.simulator_objects.route_management import RouteManagement
from distributed_event_factory.simulation.simulator_objects.workforce_storage import WorkforceStorage
from distributed_event_factory.simulation.simulator_objects.workprocessstep import WorkProcessStep
from distributed_event_factory.simulation.simulator_objects.workstation import WorkStation
from distributed_event_factory.simulation.simulator_objects.workstation_service import WorkstationService
from process_mining_core.datastructure.core.event import Event


class ProcessSimulationObjectCentric:
    def __init__(
            self,
            object_storage: ObjectStorage,
    ):
        self.workstations = []
        self.workstation_service = WorkstationService()
        self.workforce_storage = None
        self.last_timestamp = datetime.now()
        self.object_storage = object_storage
        self.prior_step: str = ""
        self.parallel_workstation_step_start_time = []

    def complete_init(self):
        self.routeManagement = RouteManagement(self.routes.get("default"))
        self.configureWorkStationsAndSteps()
        self.add_configured_stocks_in_warehouse()
        self.configureWorkforceStartPositions(self.workforce_start_positions)

    def set_objects(
            self,
            object_dict: Dict[str, ObjectData]
    ):
        self.objects = object_dict

    def set_datasources(
            self,
            datasource_dict: Dict[str, DataSource]
    ):
        self.datasources = datasource_dict

    def set_routes(
            self,
            routes_dict: Dict[str, Route]
    ):
        self.routes = routes_dict

    def set_stocks(
            self,
            stock_dict: Dict[str, InputObjectProvider]
    ):
        self.stocks = stock_dict

    def set_workforce_start_positions(
            self,
            workforce_start_positions_dict: Dict[str, WorkforceStartPositionProvider]
    ):
        self.workforce_start_positions = workforce_start_positions_dict

    def simulate(self) -> Event:
        if self.parallel_workstation_step_start_time:
            next_workstation, next_step, self.last_timestamp = self.parallel_workstation_step_start_time[0]
            self.parallel_workstation_step_start_time = self.parallel_workstation_step_start_time[1:]
        else:
            available_workstations: List[WorkStation] = (
                self.workstation_service.get_activatable_workstations(self.workstations, self.object_storage,
                                                                      self.workforce_storage))
            next_step, next_workstation = self.get_next_workstation_and_step(available_workstations)
        self.prior_step = next_step.node
        self.last_timestamp = next_workstation.add_to_last_timestamp(self.last_timestamp, next_step.duration)
        ingoing_objects, outgoing_objects = self.object_storage.manage_input_and_output_of_steps(
            next_step.input_objects, next_step.output_objects,
            self.objects, self.last_timestamp)
        if self.workforce_storage:
            self.workforce_storage.manage_workforce_changes(next_step, self.routeManagement)
        event = next_step.produce_event(self.last_timestamp,
                                        next_workstation.work_station_name, ingoing_objects, outgoing_objects)
        return event

    def _get_next_step_by_event_provider(self, data_source) -> List[str]:
        events = self._get_sensor_with_id(DataSourceId(data_source)).get_event_data()
        if len(events) == 1:
            return [events[0].transition_provider.next_sensor_index]
        elif len(events) > 1:
            next_sensors = []
            for e in events:
                next_sensors.append(e.transition_provider.next_sensor_index)
            return next_sensors
        return None

    def get_next_workstation_and_step(self, available_workstations):
        workstation_step_pairs_ascending = self.workstation_service.get_next_workstations_and_step_sorted_duration_ascending(
            object_storage=self.object_storage, workstations=available_workstations,
            workforce_storage=self.workforce_storage)

        if self.prior_step:
            next_available_steps = self._get_next_step_by_event_provider(self.prior_step)
            if next_available_steps[0]:
                next_workstation_step_pairs = self.workstation_service.get_next_workstation_step_pair_parallel(
                    next_available_steps, workstation_step_pairs_ascending, self.object_storage, self.workforce_storage,
                    self.routeManagement)

                if not next_workstation_step_pairs:
                    return ValueError("No available workstations")
                elif len(next_workstation_step_pairs) == 1:
                    next_workstation, next_step = next_workstation_step_pairs[0]
                    return next_step, next_workstation
                elif len(next_workstation_step_pairs) > 1:
                    next_workstation, next_step = next_workstation_step_pairs[0]
                    next_workstation_step_pairs.remove((next_workstation, next_step))
                    for workstation, step in next_workstation_step_pairs:
                        self.parallel_workstation_step_start_time.append((workstation, step, self.last_timestamp))
                    return next_step, next_workstation

        next_step, next_workstation = self.get_random_workstation_step_or_parallel_start(
            workstation_step_pairs_ascending)
        return next_step, next_workstation

    def get_random_workstation_step_or_parallel_start(self, workstation_steps_ascending):
        if len(workstation_steps_ascending) > 1:
            parallel_workstation_step_time = []

            possible_step = self.object_storage.contains_all_object_of_data_for_steps(workstation_steps_ascending)
            if self.workforce_storage:
                possible_step = self.workforce_storage.contains_all_workforces_for_steps(
                    steps=workstation_steps_ascending, routeManagement=self.routeManagement)
            if possible_step:
                for workstation, step in possible_step:
                    parallel_workstation_step_time.append(
                        (workstation, step, self.last_timestamp))
            self.parallel_workstation_step_start_time.extend(parallel_workstation_step_time[1:])
            next_workstation, next_step, _ = parallel_workstation_step_time[0]
        else:
            next_workstation, next_step = workstation_steps_ascending[0]
        return next_step, next_workstation

    def _get_sensor_with_id(self, data_source_id) -> DataSource:
        for sensor in self.datasources:
            if self.datasources[sensor].get_id() == data_source_id:
                return self.datasources[sensor]
        raise ValueError("Sensor not found")

    ### preparing methods ###
    def add_configured_stocks_in_warehouse(self):
        for stock in self.stocks.get("default"):
            self.object_storage.add_objects(
                ObjectUtility().convert_object_data_to_generic_objects(generic_objects_possible=self.objects,
                                                                       object_data=stock,
                                                                       timestamp=self.last_timestamp))

    def configureWorkStationsAndSteps(self):
        for data_source in self.datasources:
            if data_source != "<start>" and data_source != "<end>":
                data_source_id = DataSourceId(data_source)
                events = self._get_sensor_with_id(DataSourceId(data_source)).get_event_data()
                event_provider = self._get_sensor_with_id(DataSourceId(data_source)).event_provider
                input_objects = event_provider.input_objects
                workstation = event_provider.workstation
                workforce = event_provider.workforce
                start_location = event_provider.start
                end_location = event_provider.end
                workstation_steps = []
                for e in events:
                    workstation_steps.append(WorkProcessStep(activity=e.get_activity_provider().get_activity(),
                                                             node=data_source_id.get_name(),
                                                             group_id=self._get_sensor_with_id(
                                                                 data_source_id).group_id,
                                                             input_objects=input_objects,
                                                             output_objects=e.get_activity_provider().get_output(),
                                                             duration=e.get_duration(),
                                                             workforces_needed=workforce,
                                                             start_location=start_location,
                                                             end_location=end_location))
                matching_workstation = self.workstation_service.get_workstation_by_name(workstation, self.workstations)
                if matching_workstation:
                    matching_workstation.add_steps_to_workstation(workstation_steps)
                else:
                    self.workstations.append(
                        WorkStation(work_station_name=workstation, work_process_steps=workstation_steps))

    def configureWorkforceStartPositions(self, workforce_start_positions):
        if not workforce_start_positions:
            return
        self.workforce_storage = WorkforceStorage()
        for workforce_start_position in workforce_start_positions.get("default"):
            for i in range(workforce_start_position.numberOfWorkforce):
                self.workforce_storage.add_workforce(
                    Workforce(name=workforce_start_position.name, location=workforce_start_position.location))
