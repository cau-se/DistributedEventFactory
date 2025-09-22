from typing import List

from distributed_event_factory.core.workforce import Workforce
from distributed_event_factory.provider.workforce.InputWorkforceProvider import InputWorkforceProvider
from distributed_event_factory.simulation.simulator_objects.route_management import RouteManagement


class WorkforceStorage:
    def __init__(self):
        self.workforces: List[Workforce] = []

    def get_workforce_at_location_available(self, workforce_input: InputWorkforceProvider, location: str,
                                            workforce_storage):
        number_of_matching_workforces = 0
        workforce_set = []
        for workforce in workforce_storage:
            if workforce.location == location and workforce.name == workforce_input.name:
                number_of_matching_workforces += 1
                workforce_set.append(workforce)
            if number_of_matching_workforces == workforce_input.numberOfWorkforce:
                return workforce_set
        return workforce_set

    def get_all_workforces_at_location_available(
            self,
            workforces_input: List[InputWorkforceProvider],
            location: str,
            workforce_storage
    ):
        workforce_set = []
        is_complete = True
        for workforce in workforces_input:
            preserved_workforces = self.get_workforce_at_location_available(workforce, location, workforce_storage)
            if not preserved_workforces or len(preserved_workforces) != workforce.numberOfWorkforce:
                is_complete = False
            for preserved_workforce in preserved_workforces:
                workforce_set.append(preserved_workforce)
        return workforce_set, is_complete

    def is_workforce_type_available(self, workforce_input: InputWorkforceProvider):
        number_of_matching_workforces = 0
        for workforce in self.workforces:
            if workforce.name == workforce_input.name:
                number_of_matching_workforces += 1
        return number_of_matching_workforces >= workforce_input.numberOfWorkforce

    def are_all_workforces_types_available(self, workforces_input: List[InputWorkforceProvider]):
        for workforce in workforces_input:
            if not self.is_workforce_type_available(workforce):
                return False
        return True

    def get_available_workforce_closest_to_location(self, location: str, type: str, workforce_storage,
                                                    routeManagement: RouteManagement):
        locations = routeManagement.closest_to_location_order(location)
        for closest_location in locations:
            for workforce in workforce_storage:
                if workforce.name == type and workforce.location == closest_location.start:
                    route = routeManagement.get_route_for_start_end(closest_location.start, location)
                    return workforce, route
        return None, None

    def contains_all_workforces_for_steps(self, steps, routeManagement: RouteManagement, preselected=None):
        workforce_forecast = self.workforces.copy()
        possible_workstation_step_pairs = []
        currently_not_at_location = []
        for workstation, step in steps:
            if step.workforces_needed:
                reserved_workforces, is_complete = self.get_all_workforces_at_location_available(step.workforces_needed,
                                                                                                 step.start_location,
                                                                                                 workforce_forecast)
                if reserved_workforces and is_complete:
                    for reserved_workforce in reserved_workforces:
                        workforce_forecast.remove(reserved_workforce)
                    possible_workstation_step_pairs.append((workstation, step))
                elif not is_complete and reserved_workforces:
                    return ValueError(len(reserved_workforces), step)
                else:
                    if preselected and step.node in preselected:
                        prefered_currently_not_at_location = [(workstation, step)]
                        possible_workstation_step_pairs = self.contains_workforces_near_by(
                            prefered_currently_not_at_location, possible_workstation_step_pairs, routeManagement,
                            workforce_forecast)
                    else:
                        currently_not_at_location.append((workstation, step))
            else:
                possible_workstation_step_pairs.append((workstation, step))

        return self.contains_workforces_near_by(currently_not_at_location, possible_workstation_step_pairs,
                                                routeManagement, workforce_forecast)

    def contains_workforces_near_by(
            self,
            currently_not_at_location,
            possible_workstation_step_pairs,
            routeManagement,
            workforce_forecast
    ):
        for workstation, step in currently_not_at_location:
            all_workforces_at_location = True
            steps_with_duration = []
            for workforce in step.workforces_needed:
                workforce, route = self.get_available_workforce_closest_to_location(
                    step.start_location,
                    workforce.name,
                    workforce_forecast,
                    routeManagement
                )
                if workforce:
                    step = step.clone()
                    step.duration = step.duration + route.duration
                    self.workforces.remove(workforce)
                    workforce.location = step.start_location
                    self.workforces.append(workforce)
                else:
                    all_workforces_at_location = False
            if all_workforces_at_location and steps_with_duration:
                possible_workstation_step_pairs.append((workstation, step))
        return possible_workstation_step_pairs

    def manage_workforce_changes(self, step, routeManagement: RouteManagement):
        if step.start_location != step.end_location and step.workforces_needed:
            workforces, is_complete = self.get_all_workforces_at_location_available(
                step.workforces_needed,
                step.start_location,
                self.workforces)
            if workforces:
                for workforce in workforces:
                    self.workforces.remove(workforce)
                    workforce.location = step.end_location
                    self.workforces.append(workforce)
            else:
                for workforce in step.workforces_needed:
                    workforce, _ = self.get_available_workforce_closest_to_location(
                        step.start_location,
                        workforce.name,
                        self.workforces,
                        routeManagement
                    )
                    self.workforces.remove(workforce)
                    workforce.location = step.end_location
                    self.workforces.append(workforce)

    def add_workforce(self, workforce: Workforce):
        self.workforces.append(workforce)
