from datetime import datetime, timedelta
from typing import Dict, List

from distributed_event_factory.core.abstract_datasource import DataSource
from distributed_event_factory.core.datasource_id import DataSourceId
from distributed_event_factory.core.object import ObjectData
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.simulation.abstract_process_simulator import ProcessSimulator
from distributed_event_factory.simulation.abstract_process_simulator_config import ProcessSimulatorConfig
from distributed_event_factory.simulation.simulator_objects.object_storage_v2 import ObjectStorageV2
from distributed_event_factory.simulation.simulator_objects.object_utility import ObjectUtility
from distributed_event_factory.simulation.simulator_objects.workprocessstep import WorkProcessStep


class ProcessSimulationObjectCentric(ProcessSimulator):
    def __init__(
            self,
            object_storage,
    ):
        self.last_timestamp = datetime.now()
        self.object_storage: ObjectStorageV2 = ObjectStorageV2()
        self.work_steps: List[WorkProcessStep] = []
        self.next_step_id = None

    def configure(self, config: ProcessSimulatorConfig):
        self.objects = config.get_configs_of_type("object")
        self.datasources = config.get_configs_of_type("datasource")
        self.stocks = config.get_configs_of_type("stock")
        self.complete_init()

    def complete_init(self):
        self.configure_work_steps()
        self.add_configured_stocks_in_warehouse()

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

    def set_stocks(
            self,
            stock_dict: Dict[str, InputObjectProvider]
    ):
        self.stocks = stock_dict

    def simulate(self):
        executable_steps = self.object_storage.filter_executable_events(self.work_steps)
        if not executable_steps:
            raise ValueError("No executable object-centric step available")

        if self.next_step_id:
            preferred = [step for step in executable_steps if step.node == self.next_step_id]
            if preferred:
                executable_steps = preferred

        executable_steps.sort(key=lambda step: step.duration)
        next_step = executable_steps[0]
        self.last_timestamp = self.last_timestamp + timedelta(seconds=next_step.duration)
        self.next_step_id = next_step.transition

        self.object_storage.process_event(next_step)

        return next_step.produce_event(
            self.last_timestamp,
            next_step.group_id,
            next_step.input_objects,
            next_step.output_objects
        )

    def _get_sensor_with_id(self, data_source_id: DataSourceId) -> DataSource:
        for sensor in self.datasources:
            if self.datasources[sensor].get_id() == data_source_id:
                return self.datasources[sensor]
        raise ValueError("Sensor not found")

    def add_configured_stocks_in_warehouse(self):
        for stock in self.stocks.get("default"):
            self.object_storage.add_objects(
                ObjectUtility().convert_object_data_to_generic_objects(
                    generic_objects_possible=self.objects,
                    object_data=stock,
                    timestamp=self.last_timestamp
                )
            )

    def configure_work_steps(self):
        for data_source in self.datasources:
            if data_source == "<end>":
                continue

            data_source_id = DataSourceId(data_source)
            datasource = self._get_sensor_with_id(data_source_id)
            event_provider = datasource.event_provider
            events = datasource.get_event_data()

            self.work_steps.append(
                WorkProcessStep(
                    activity=events.activity_provider.get_activity(),
                    node=data_source_id.get_name(),
                    group_id=datasource.group_id,
                    input_objects=event_provider.input_objects,
                    output_objects=events.output_provider,
                    duration=events.duration_provider.get_duration(),
                    workforces_needed=[],
                    transition=events.transition_provider.get_transition()
                )
            )
