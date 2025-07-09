from typing import List

from core.workforce import Workforce
from simulation.simulator_objects.route_management import RouteManagement


class WorkforceStorage:
    def __init__(self):
        self.workforces: List[Workforce] = []

    def get_available_workforce_at_location(self, location:str):
        for workforce in self.workforces:
            if workforce.location == location:
                return workforce
        return None

    def get_available_workforce_closest_to_location(self, location:str, routeManagement:RouteManagement):
        locations = routeManagement.closest_to_location_order(location)
        for location in locations:
            for workforce in self.workforces:
                if workforce.location == location:
                    return workforce
        return None