import random
from typing import List

from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workstation import WorkStation


class WorkstationService:

    def get_activatable_workstations(self, workstations: List[WorkStation], object_storage: ObjectStorage):
        activatable_workstations = []

        for workstation in workstations:
            if workstation._is_activatable(object_storage):
                activatable_workstations.append(workstation)

        return activatable_workstations

    def get_workstation_by_name(self, workstation_name, workstations: List[WorkStation]):
        for workstation in workstations:
            if workstation.work_station_name == workstation_name:
                return workstation
        return None

    def get_next_workstation_step_pair_parallel(self, next_available_steps, workstation_steps_ascending,
                                                object_storage: ObjectStorage):
        steps_in_priority = []
        workstations_preselected = self.get_workstations_preselected([item[0] for item in workstation_steps_ascending],
                                                                     next_available_steps, object_storage)
        if workstations_preselected:
            if type(workstations_preselected) is WorkStation:
                steps_in_priority.append((workstations_preselected,
                                          workstations_preselected.get_prefered_activatable_work_steps(object_storage,
                                                                                                       next_available_steps)))
            else:
                for workstation in workstations_preselected:
                    steps_in_priority.append((workstation,
                                              workstation.get_prefered_activatable_work_steps(object_storage,
                                                                                              next_available_steps)))
        for workstation, step in workstation_steps_ascending:
            if ((type(workstations_preselected) is WorkStation and workstation != workstations_preselected) or
                    (type(
                        workstations_preselected) is list and workstation not in workstations_preselected) or not workstations_preselected):
                steps_in_priority.append((workstation, step))
        possible_steps = object_storage.contains_all_object_of_data_for_steps(steps_in_priority)
        possible_steps.sort(key=lambda x: x[1].duration)
        return possible_steps

    def get_next_workstations_and_step_sorted_duration_ascending(self, object_storage: ObjectStorage,
                                                                 workstations: List[WorkStation]):
        workstations_step_pair = []
        for workstation in workstations:
            step = workstation.get_random_workstation_step(object_storage=object_storage)
            workstations_step_pair.append((workstation, step))
        workstations_step_pair.sort(key=lambda x: x[1].duration)
        return workstations_step_pair

    def get_workstations_preselected(self, workstations: List[WorkStation], prefered_workstation_steps: List[str],
                                     object_storage: ObjectStorage):
        workstation_selected = []
        for workstation in workstations:
            if workstation.workstation_has_preselected_activatable_steps(object_storage=object_storage,
                                                                         prefered_workstation_steps=prefered_workstation_steps):
                workstation_selected.append(workstation)
        if len(workstation_selected) == 1:
            return workstation_selected[0]
        elif len(workstation_selected) > 1:
            return workstation_selected
        return None
