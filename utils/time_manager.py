from typing import Dict
from datetime import datetime, timedelta


class TimeManager:
    def __init__(self):
        self.time_map: Dict[str, datetime] = {}

    def update_time(self, id: str, time: timedelta):
        if id in self.time_map:
            self.time_map[id] += time
        else:
            self.time_map[id] = datetime.now() + time

    def get_time(self, id: str) -> timedelta:
        if id in self.time_map:
            return datetime.now() - self.time_map[id]
        else:
            raise ValueError(f"ID: {id} not in timemap")
