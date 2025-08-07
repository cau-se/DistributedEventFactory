from core.route import Route
from parser.parser import Parser


class RouteParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        route_list = []
        for route in config["routes"]:
            route_list.append(Route(
                route_for_activity=route["routeForActivity"],
                start=route["start"],
                end=route["end"],
                duration=route["duration"]
            ))
        return route_list