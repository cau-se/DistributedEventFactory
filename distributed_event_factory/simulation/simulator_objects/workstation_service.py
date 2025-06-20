import random
from typing import List

from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep


class WorkstationService:

    def get_activatable_workstations(self, workstations: List[WorkProcessStep], object_storage: ObjectStorage):
        activatable_workstations = []

        for workstation in workstations:
            if object_storage.contains_all_objects(workstation.input_objects):
                activatable_workstations.append(workstation)

        return activatable_workstations

    def get_workstation(self, workstations: List[WorkProcessStep]) -> WorkProcessStep:
        return workstations[random.randint(0, len(workstations) - 1)]