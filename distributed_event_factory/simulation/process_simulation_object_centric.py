from datetime import datetime
from typing import List

from process_mining_core.datastructure.core.event import Event
from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep
from simulation.simulator_objects.workstation_service import WorkstationService


class ProcessSimulationObjectCentric:
    def __init__(
        self,
        workstation_steps: List[WorkProcessStep],
        object_storage: ObjectStorage
    ):
        self.workstation_steps = workstation_steps
        self.workstation_service = WorkstationService()
        self.current_timestamp = datetime.now()
        self.object_storage = object_storage

    def simulate(self) -> Event:
        available_steps: List[WorkProcessStep] = (
            self.workstation_service.get_activatable_workstations(self.workstation_steps, self.object_storage))
        next_step: WorkProcessStep = self.workstation_service.get_workstation(available_steps)
        event = next_step.produce_event(self.current_timestamp)
        self.object_storage.add_object(event.output)
        return event


