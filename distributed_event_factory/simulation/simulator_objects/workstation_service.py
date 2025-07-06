import random
from typing import List

from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep
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

    def get_next_workstation_step_pair_parallel(self, next_available_steps, workstations: List[WorkStation],
                                                object_storage: ObjectStorage):
        steps_in_priority = []
        workstations_preselected = self.get_workstations_preselected(workstations, next_available_steps, object_storage)
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
        for workstation in workstations:
            if ((type(workstations_preselected) is WorkStation and workstation != workstations_preselected) or
                    (type(
                        workstations_preselected) is list and workstation not in workstations_preselected) or not workstations_preselected):
                steps_in_priority.append((workstation, workstation.get_fastest_available_step(object_storage)))
        possible_steps = object_storage.contains_all_object_of_data_for_steps(steps_in_priority)
        possible_steps.sort(key=lambda x: x[1].duration)
        return possible_steps

    def get_next_workstations_sorted_duration_ascending(self, object_storage: ObjectStorage,
                                                        workstations: List[WorkStation]):
        workstations_with_step_sorted_duration_ascending = []
        workstations_to_search_in = workstations.copy()
        while len(workstations_with_step_sorted_duration_ascending) != len(workstations):
            shortest_workstation = self.get_workstation_with_shortest_next_step(object_storage,
                                                                                workstations_to_search_in)
            workstations_to_search_in.remove(shortest_workstation)
            workstations_with_step_sorted_duration_ascending.append(shortest_workstation)
        return workstations_with_step_sorted_duration_ascending

    def get_workstation_with_shortest_next_step(self, object_storage: ObjectStorage, workstations: List[WorkStation]):
        minimal_duration = workstations[0].get_duration_of_shortest_available_step(object_storage=object_storage)
        workstation_with_shortest_next_step = workstations[0]

        for workstation in workstations:
            workstation_shortest_duration = workstation.get_duration_of_shortest_available_step(
                object_storage=object_storage)
            if workstation_shortest_duration < minimal_duration:
                minimal_duration = workstation_shortest_duration
                workstation_with_shortest_next_step = workstation

        return workstation_with_shortest_next_step

    def get_random_workstation(self, workstations: List[WorkStation]) -> WorkStation:
        return workstations[random.randint(0, len(workstations) - 1)]

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
