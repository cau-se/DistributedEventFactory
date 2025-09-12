class Route:

    def __init__(
            self,
            route_for_activity: str,
            start: str,
            end: str,
            duration: int

    ):
        self.route_for_activity = route_for_activity
        self.start = start
        self.end = end
        self.duration = duration

    def get_route_for_activity(self):
        return self.route_for_activity

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_duration(self):
        return self.duration