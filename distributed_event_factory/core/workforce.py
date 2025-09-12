from core.object_id import ObjectId
from core.route import Route
from simulation.simulator_objects.route_management import RouteManagement


class Workforce:
    def __init__(self, name:str, location:str):
        self.name = name
        self.location = location
        self.available = True
        self.object_id = ObjectId(name)

    def get_duration_to_get_to_location(self, location:str, routeManagement:RouteManagement):
        route: Route =  routeManagement.get_route_for_start_end(self.location, location)
        return route.duration

    def get_location(self):
        return self.location

    def is_transfer_to_location_possible(self, location:str, routeManagement:RouteManagement):
        if self.available:
            return routeManagement.route_for_start_end_exists(self.location, location)
        return False

    def set_available(self, available:bool):
        self.available = available

    def is_available(self):
        return self.available
