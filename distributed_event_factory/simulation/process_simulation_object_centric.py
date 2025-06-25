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
from simulation.simulator_objects.workstation_service import WorkstationService


class ProcessSimulationObjectCentric:
    def __init__(
            self,
            object_storage: ObjectStorage,
            data_sources: Dict[str, DataSource],
            objects: Dict[str, ObjectData],
            stocks: Dict[str, InputObjectProvider]
    ):
        self.workstation_steps = []
        self.workstation_service = WorkstationService()
        self.current_timestamp = datetime.now()
        self.object_storage = object_storage
        self.objects = objects
        self.data_sources = data_sources
        self.stocks: Dict[str, InputObjectProvider] = stocks

    def simulate(self) -> Event:
        self.configureWorkStationsAndSteps()
        self.add_configured_stocks_in_warehouse()
        available_steps: List[WorkProcessStep] = (
            self.workstation_service.get_activatable_workstations(self.workstation_steps, self.object_storage))
        next_step: WorkProcessStep = self.workstation_service.get_workstation(available_steps)
        event = next_step.produce_event(self.current_timestamp)
        self.object_storage.add_object(event.output)
        return event

    def add_configured_stocks_in_warehouse(self):
        for stock in self.stocks.get("default"):
            self.object_storage.add_objects(ObjectUtility().convert_object_data_to_generic_objects(generic_objects_possible=self.objects, object_data=stock))

    def configureWorkStationsAndSteps(self):
        for data_source in self.data_sources:
            if data_source != "<start>" and data_source != "<end>":
                data_source_id = DataSourceId(data_source)
                events = self._get_sensor_with_id(DataSourceId("Assembly")).get_event_data()
                input_objects = self._get_sensor_with_id(DataSourceId("Assembly")).event_provider.input_objects
                for e in events:
                    self.workstation_steps.append(WorkProcessStep(activity=e.get_activity_provider().get_activity(), node=data_source_id.get_name(),
                                    group_id=self._get_sensor_with_id(data_source_id).group_id,
                                    input_objects=input_objects, output_objects=e.get_activity_provider().get_output(),
                                    duration=e.get_duration()))

    def _get_sensor_with_id(self, data_source_id) -> DataSource:
        for sensor in self.data_sources:
            if self.data_sources[sensor].get_id() == data_source_id:
                return self.data_sources[sensor]
        raise ValueError("Sensor not found")
