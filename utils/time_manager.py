from typing import Dict, Callable
from datetime import datetime, timedelta


class Units:
    @staticmethod
    def millisecond(value: float) -> timedelta:
        return timedelta(milliseconds=value)

    @staticmethod
    def second(value: float) -> timedelta:
        return timedelta(seconds=value)

    @staticmethod
    def minute(value: float) -> timedelta:
        return timedelta(minutes=value)

    @staticmethod
    def hour(value: float) -> timedelta:
        return timedelta(hours=value)

    @staticmethod
    def day(value: float) -> timedelta:
        return timedelta(days=value)

    @staticmethod
    def week(value: float) -> timedelta:
        return timedelta(weeks=value)

    @staticmethod
    def month(value: float) -> timedelta:
        return timedelta(days=value * 30)

    @staticmethod
    def year(value: float) -> timedelta:
        return timedelta(days=value * 365)

    @staticmethod
    def decade(value: float) -> timedelta:
        return timedelta(days=value * 365 * 10)

    @staticmethod
    def century(value: float) -> timedelta:
        return timedelta(days=value * 365 * 100)

    @staticmethod
    def millennium(value: float) -> timedelta:
        return timedelta(days=value * 365 * 1000)

    def __getitem__(self, item: str):
        return getattr(Units, item)


class TimeManager:
    def __init__(self):
        self.time_map = {}

    def add_time(self, id: int, time: datetime):
        self.time_map[str(id)] = time

    def increase_time(self, map_id: int, value, unit: type[Callable[[float], datetime]]):
        if str(map_id) not in self.time_map:
            raise ValueError(f"ID {map_id} not found in the time map.")

        time = self.time_map[str(map_id)]
        new_time = time + unit(value)
        self.time_map[str(map_id)] = new_time


manager = TimeManager()

manager.add_time(1, datetime.now())
manager.increase_time(1, 5, Units.minute)

print(Units["test"])
