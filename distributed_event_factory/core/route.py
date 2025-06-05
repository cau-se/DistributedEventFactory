from typing import List, Tuple


class Route:

    def __init__(
            self,
            route_for_activity: str,
            start: str,
            end: str,
            transfer_objects: List[Tuple[str, int]],
            duration: int

    ):
        self.route_for_activity = route_for_activity
        self.start = start
        self.end = end
        self.transfer_objects = transfer_objects
        self.duration = duration

    def get_route_for_activity(self):
        return self.route_for_activity

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_transfer_objects(self):
        return self.transfer_objects

    def get_duration(self):
        return self.duration