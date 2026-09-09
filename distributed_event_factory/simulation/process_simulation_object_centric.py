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
        self.available_datasource_ids: List[DataSourceId] = []
        self.parallel_work_steps_with_start: List[tuple[WorkProcessStep, datetime]] = []
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
        if self.parallel_work_steps_with_start:
            parallel_step, parallel_start_time = self.parallel_work_steps_with_start[0]
            self.parallel_work_steps_with_start = self.parallel_work_steps_with_start[1:]
            self.last_timestamp = parallel_start_time
            return self._execute_step(parallel_step)

        executable_datasources_with_steps = self.get_executable_datasources_with_steps()
        if not executable_datasources_with_steps:
            raise ValueError("No executable object-centric step available")

        if self.next_step_id:
            preferred = [
                datasource_with_steps
                for datasource_with_steps in executable_datasources_with_steps
                if datasource_with_steps[0].get_name() == self.next_step_id
            ]
            if preferred:
                executable_datasources_with_steps = preferred

        executable_datasources_with_steps.sort(key=lambda datasource_with_steps: datasource_with_steps[1][0].duration)
        _, steps = executable_datasources_with_steps[0]

        if len(steps) > 1:
            parallel_start_time = self.last_timestamp
            self.parallel_work_steps_with_start.extend(
                [(step, parallel_start_time) for step in steps[1:]]
            )

        return self._execute_step(steps[0])

    def _execute_step(self, step: WorkProcessStep):
        self.last_timestamp = self.last_timestamp + timedelta(seconds=step.duration)
        self.next_step_id = step.transition
        self.object_storage.process_event(step)
        return step.produce_event(
            self.last_timestamp,
            step.group_id,
            step.input_objects,
            step.output_objects
        )

    def get_executable_datasources_with_steps(self):
        executable_datasources_with_steps = []

        for data_source_id in self.available_datasource_ids:
            datasource = self._get_sensor_with_id(data_source_id)
            input_objects = datasource.event_provider.input_objects
            if not self.object_storage.are_all_inputs_available(input_objects):
                continue

            steps = self.get_steps_for_datasource(datasource, data_source_id, input_objects)
            if steps:
                steps.sort(key=lambda step: step.duration)
                executable_datasources_with_steps.append((data_source_id, steps))

        return executable_datasources_with_steps

    def get_steps_for_datasource(self, datasource: DataSource, data_source_id: DataSourceId, input_objects):
        events = datasource.get_event_data()
        if isinstance(events, list):
            return [
                self.build_work_step(data_source_id, datasource, input_objects, event)
                for event in events
            ]
        return [self.build_work_step(data_source_id, datasource, input_objects, events)]

    def build_work_step(self, data_source_id: DataSourceId, datasource: DataSource, input_objects, event):
        return WorkProcessStep(
            activity=event.activity_provider.get_activity(),
            node=data_source_id.get_name(),
            group_id=datasource.group_id,
            input_objects=input_objects,
            output_objects=event.output_provider,
            duration=event.duration_provider.get_duration(),
            workforces_needed=[],
            transition=event.transition_provider.get_transition()
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
        self.available_datasource_ids = []
        for data_source in self.datasources:
            if data_source == "<end>":
                continue
            self.available_datasource_ids.append(DataSourceId(data_source))
