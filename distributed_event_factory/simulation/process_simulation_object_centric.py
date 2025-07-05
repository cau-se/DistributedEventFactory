from datetime import datetime
from typing import List, Dict

from process_mining_core.datastructure.core.event import Event

from core.abstract_datasource import DataSource
from core.datasource_id import DataSourceId
from core.object import ObjectData
from provider.object.input.input_provider import InputObjectProvider
from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.object_utility import ObjectUtility
from simulation.simulator_objects.workprocessstep import WorkProcessStep
from simulation.simulator_objects.workstation import WorkStation
from simulation.simulator_objects.workstation_service import WorkstationService


class ProcessSimulationObjectCentric:
    def __init__(
            self,
            object_storage: ObjectStorage,
            data_sources: Dict[str, DataSource],
            objects: Dict[str, ObjectData],
            stocks: Dict[str, InputObjectProvider]
    ):
        self.workstations = []
        self.workstation_service = WorkstationService()
        self.last_timestamp = datetime.now()
        self.object_storage = object_storage
        self.objects = objects
        self.data_sources = data_sources
        self.stocks: Dict[str, InputObjectProvider] = stocks
        self.configureWorkStationsAndSteps()
        self.add_configured_stocks_in_warehouse()
        self.prior_step: str = ""
        self.parallel_workstation_step_start_time = []

    def simulate(self) -> Event:
        if self.parallel_workstation_step_start_time:
            next_workstation, next_step, self.last_timestamp = self.parallel_workstation_step_start_time[0]
            self.parallel_workstation_step_start_time = self.parallel_workstation_step_start_time[1:]
        else:
            available_workstations: List[WorkStation] = (
                self.workstation_service.get_activatable_workstations(self.workstations, self.object_storage))
            next_step, next_workstation = self.get_next_workstation_and_step(available_workstations)
        self.prior_step = next_step.node
        self.last_timestamp = next_workstation.add_to_last_timestamp(self.last_timestamp, next_step.duration)
        ingoing_objects, outgoing_objects = self.object_storage.manage_input_and_output_of_steps(
            next_step.input_objects, next_step.output_objects,
            self.objects, self.last_timestamp)
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
        workstations_ascending = self.workstation_service.get_next_workstations_sorted_duration_ascending(
            object_storage=self.object_storage, workstations=available_workstations)

        if self.prior_step:
            next_available_steps = self._get_next_step_by_event_provider(self.prior_step)
            if next_available_steps[0]:
                next_workstation_and_step = self.workstation_service.get_next_workstation_step_pair_parallel(
                    next_available_steps, workstations_ascending, self.object_storage)

                if not next_workstation_and_step:
                    return ValueError("No available workstations")
                elif len(next_workstation_and_step) == 1:
                    next_workstation, next_step = next_workstation_and_step[0]
                    return next_step, next_workstation
                elif len(next_workstation_and_step) > 1:
                    next_workstation, next_step = next_workstation_and_step[0]
                    next_workstation_and_step.remove((next_workstation, next_step))
                    for workstation, step in next_workstation_and_step:
                        self.parallel_workstation_step_start_time.append((workstation, step, self.last_timestamp))
                    return next_step, next_workstation

        next_step, next_workstation = self.get_random_workstation_step_or_parallel_start(workstations_ascending)
        return next_step, next_workstation

    def get_random_workstation_step_or_parallel_start(self, parallel_workstations):
        if len(parallel_workstations) > 1:
            multiple_workstations = []
            forecast_workstations_steps = []
            for workstation in parallel_workstations:
                step = workstation.get_fastest_available_step(object_storage=self.object_storage)
                forecast_workstations_steps.append((workstation, step))

            possible_step = self.object_storage.contains_all_object_of_data_for_steps([(workstation, step)])
            if possible_step:
                for workstation, step in possible_step:
                    multiple_workstations.append(
                        (workstation, step, self.last_timestamp))
            self.parallel_workstation_step_start_time.extend(multiple_workstations[1:])
            next_workstation, next_step ,_ = multiple_workstations[0]
        else:
            next_workstation: WorkStation = parallel_workstations[0]
            next_step = next_workstation.get_random_workstation_step(object_storage=self.object_storage)
        return next_step, next_workstation

    def _get_sensor_with_id(self, data_source_id) -> DataSource:
        for sensor in self.data_sources:
            if self.data_sources[sensor].get_id() == data_source_id:
                return self.data_sources[sensor]
        raise ValueError("Sensor not found")

    ### preparing methods ###
    def add_configured_stocks_in_warehouse(self):
        for stock in self.stocks.get("default"):
            self.object_storage.add_objects(
                ObjectUtility().convert_object_data_to_generic_objects(generic_objects_possible=self.objects,
                                                                       object_data=stock,
                                                                       timestamp=self.last_timestamp))

    def configureWorkStationsAndSteps(self):
        for data_source in self.data_sources:
            if data_source != "<start>" and data_source != "<end>":
                data_source_id = DataSourceId(data_source)
                events = self._get_sensor_with_id(DataSourceId(data_source)).get_event_data()
                input_objects = self._get_sensor_with_id(DataSourceId(data_source)).event_provider.input_objects
                workstation = self._get_sensor_with_id(DataSourceId(data_source)).event_provider.workstation
                workstation_steps = []
                for e in events:
                    workstation_steps.append(WorkProcessStep(activity=e.get_activity_provider().get_activity(),
                                                             node=data_source_id.get_name(),
                                                             group_id=self._get_sensor_with_id(
                                                                 data_source_id).group_id,
                                                             input_objects=input_objects,
                                                             output_objects=e.get_activity_provider().get_output(),
                                                             duration=e.get_duration()))

                self.workstations.append(
                    WorkStation(work_station_name=workstation, work_process_steps=workstation_steps))
