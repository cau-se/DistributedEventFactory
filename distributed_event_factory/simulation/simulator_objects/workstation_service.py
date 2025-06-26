import random
from typing import List

from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep


class WorkstationService:

    def get_activatable_workstations(self, workstations: List[WorkProcessStep], object_storage: ObjectStorage):
        activatable_workstations = []

        for workstation in workstations:
            if object_storage.contains_all_object_of_data(workstation.input_objects):
                activatable_workstations.append(workstation)

        return activatable_workstations

    def get_random_workstation(self, workstations: List[WorkProcessStep]) -> WorkProcessStep:
        return workstations[random.randint(0, len(workstations) - 1)]

    def get_workstation_preselected(self, workstations: List[WorkProcessStep], prefered_workstations: List[str]):
        workstations_selected = []
        for workstation in workstations:
            if workstation.node in prefered_workstations:
                workstations_selected.append(workstation)
        if len(workstations_selected) ==1:
            return workstations_selected[0]
        elif len(workstations_selected) > 1:
            return random.choice(workstations_selected)
        return workstations[random.randint(0, len(workstations) - 1)]