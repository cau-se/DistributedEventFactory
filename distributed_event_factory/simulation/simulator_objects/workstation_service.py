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

    def get_next_workstations_sorted_duration_ascending(self, object_storage: ObjectStorage, workstations: List[WorkStation]):
        workstations_with_step_sorted_duration_ascending = []
        workstations_to_search_in = workstations.copy()
        while len(workstations_with_step_sorted_duration_ascending) != len(workstations):
            shortest_workstation = self.get_workstation_with_shortest_next_step(object_storage, workstations_to_search_in)
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
