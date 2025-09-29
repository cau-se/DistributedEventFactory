import random
from typing import List

from distributed_event_factory.simulation.simulator_objects.object_storage import ObjectStorage
from distributed_event_factory.simulation.simulator_objects.object_storage_v2 import ObjectStorageV2
from distributed_event_factory.simulation.simulator_objects.route_management import RouteManagement
from distributed_event_factory.simulation.simulator_objects.workforce_storage import WorkforceStorage
from distributed_event_factory.simulation.simulator_objects.workstation import WorkStation


class WorkstationService:

    def get_activatable_workstations(
            self,
            workstations: List[WorkStation],
            object_storage: ObjectStorage,
            workforce_storage: WorkforceStorage = None) -> List[WorkStation]:
        activatable_workstations = []

        for workstation in workstations:
            if workforce_storage:
                if workstation._is_activatable_including_workforce(object_storage, workforce_storage):
                    activatable_workstations.append(workstation)
            else:
                if workstation._is_activatable(object_storage):
                    activatable_workstations.append(workstation)

        return activatable_workstations

    def get_next_workstation_step_pair_parallel(
            self,
            workstations,
            next_available_steps,
            object_storage: ObjectStorageV2,
            workforce_storage: WorkforceStorage = None,
            route_management: RouteManagement = None
    ):
        steps_in_priority = []
        workstations_preselected = self.get_workstations_preselected(
            workstations,
            next_available_steps,
            object_storage,
            workforce_storage
        )
        self.append_possible_preselected_workstation_step_pairs(
            next_available_steps,
            object_storage,
            steps_in_priority,
            workstations_preselected,
            workforce_storage
        )

        possible_steps = object_storage.filter_executable_events(next_available_steps)

        if workforce_storage:
            possible_steps = workforce_storage.contains_all_workforces_for_steps(
                possible_steps,
                route_management,
                next_available_steps
            )
        possible_steps.sort(key=lambda x: x.duration)
        return possible_steps

    def append_possible_preselected_workstation_step_pairs(
            self,
            next_available_steps,
            object_storage,
            steps_in_priority,
            workstations_preselected,
            workforce_storage: WorkforceStorage = None):
        if workstations_preselected:
            if type(workstations_preselected) is WorkStation:
                steps_in_priority.append(
                    (workstations_preselected,
                     workstations_preselected.get_prefered_activatable_work_steps(
                         object_storage,
                         next_available_steps,
                         workforce_storage)
                     )
                )
            else:
                for workstation in workstations_preselected:
                    steps_in_priority.append(
                        (workstation,
                         workstation.get_prefered_activatable_work_steps(
                             object_storage,
                             next_available_steps,
                             workforce_storage)
                         )
                    )

    def get_next_workstations_and_step_sorted_duration_ascending(
            self,
            object_storage: ObjectStorage,
            workstations: List[WorkStation],
            workforce_storage: WorkforceStorage = None):
        workstations_step_pair = []
        for workstation in workstations:
            step = workstation.get_random_activatable_workstation_step(
                object_storage=object_storage,
                workforce_storage=workforce_storage
            )
            workstations_step_pair.append(step)
        workstations_step_pair.sort(key=lambda x: x.duration)
        return workstations_step_pair

    def get_workstations_preselected(
            self,
            workstations: List[WorkStation],
            prefered_workstation_steps: List[str],
            object_storage: ObjectStorage,
            workforce_storage: WorkforceStorage = None
    ):
        workstation_selected = []
        for workstation in workstations:
            if workstation.workstation_has_preselected_activatable_steps(
                object_storage=object_storage,
                prefered_workstation_steps=prefered_workstation_steps,
                workforce_storage=workforce_storage
            ):
                workstation_selected.append(workstation)
        if len(workstation_selected) == 1:
            return workstation_selected[0]
        elif len(workstation_selected) > 1:
            return workstation_selected
        return None

    def get_workstation_by_name(self, possible_workstations: List[WorkStation], workstation_name: str):
        workstations = [workstation for workstation in possible_workstations if
                        workstation.work_station_name == workstation_name]
        if workstations:
            return workstations[0]
        else:
            return None
