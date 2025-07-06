import random
from typing import List
from datetime import timedelta
from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep

class WorkStation:
    def __init__(self, work_station_name:str, work_process_steps: List[WorkProcessStep]):
        self.work_station_name = work_station_name
        self.work_process_steps = work_process_steps
        self.last_event_end_timestamp = None

    def _is_activatable(self, object_storage: ObjectStorage):
        for workstation_step in self.work_process_steps:
            if object_storage.contains_all_object_of_data(workstation_step.input_objects):
                return True

        return False

    def get_activatable_work_steps(self, object_storage: ObjectStorage):
        activatable_workstations = []

        for workstation_step in self.work_process_steps:
            if object_storage.contains_all_object_of_data(workstation_step.input_objects):
                activatable_workstations.append(workstation_step)

        return activatable_workstations

    def get_prefered_activatable_work_steps(self, object_storage: ObjectStorage, prefered_workstation_steps: List[str]):
        activatable_steps = self.get_activatable_work_steps(object_storage)
        work_step_selected = []

        for workstation_step in activatable_steps:
            if workstation_step.node in prefered_workstation_steps:
                work_step_selected.append(workstation_step)

        return work_step_selected[random.randint(0, len(work_step_selected) - 1)]

    def workstation_has_preselected_activatable_steps(self, object_storage: ObjectStorage, prefered_workstation_steps: List[str]) -> bool:
        activatable_steps = self.get_activatable_work_steps(object_storage)

        for workstation_step in activatable_steps:
            if workstation_step.node in prefered_workstation_steps:
                return True

        return False

    def get_random_workstation_step(self, object_storage: ObjectStorage) -> WorkProcessStep:
        work_process_steps_possible = self.get_activatable_work_steps(object_storage)
        return work_process_steps_possible[random.randint(0, len(work_process_steps_possible) - 1)]

    def add_to_last_timestamp(self, current_timestamp, duration):
        self.last_event_end_timestamp = current_timestamp + timedelta(seconds=duration)
        return self.last_event_end_timestamp

    def add_steps_to_workstation(self, steps):
        for step in steps:
            self.work_process_steps.append(step)