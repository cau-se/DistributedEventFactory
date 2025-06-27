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

    def get_random_workstation(self, workstations: List[WorkStation]) -> WorkStation:
        return workstations[random.randint(0, len(workstations) - 1)]

    def get_workstation_preselected(self, workstations: List[WorkStation], prefered_workstation_steps: List[str], object_storage: ObjectStorage) -> WorkStation:
        workstation_selected = []
        for workstation in workstations:
            if workstation.workstation_has_preselected_activatable_steps(object_storage=object_storage, prefered_workstation_steps=prefered_workstation_steps):
                workstation_selected.append(workstation)
        if len(workstation_selected) == 1:
            return workstation_selected[0]
        elif len(workstation_selected) > 1:
            return random.choice(workstation_selected)

        return workstations[random.randint(0, len(workstations) - 1)]