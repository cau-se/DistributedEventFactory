from typing import List, Tuple


class Route:

    def __init__(
            self,
            route_name: str,
            start: str,
            end: str,
            transfer_objects: List[Tuple[str, int]],
            duration: int

    ):
        self.route_name : route_name
        self.start = start
        self.end = end
        self.transfer_objects = transfer_objects
        self.duration = duration
