from typing import List

from core.route import Route


class RouteManagement:
    def __init__(self, routes: List[Route]):
        self.routes = routes

    def get_route_for_start_end(self, start, end):
        for route in self.routes:
            if route.start == start and route.end == end:
                return route
        return None

    def get_route_for_start(self, start):
        for route in self.routes:
            if route.start == start:
                return route
        return None

    def route_for_start_end_exists(self, start, end):
        for route in self.routes:
            if route.start == start and route.end == end:
                return True
        return False

    def closest_to_location(self, location:str):
        min_route = self.get_route_for_start(location)
        min_duration = min_route.duration

        for route in self.routes:
            if route.start == location:
                if min_duration > route.duration:
                    min_duration = route.duration
                    min_route = route
        return min_route


    def closest_to_location_order(self, location:str):
        possible_routes = []
        for route in self.routes:
            if route.start == location:
                possible_routes.append(route)
        possible_routes.sort(key=lambda route: route.duration)
        return possible_routes