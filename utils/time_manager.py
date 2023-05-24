from typing import Dict, Callable
from datetime import datetime, timedelta


class Units:
    @staticmethod
    def millisecond(value: float):
        return timedelta(milliseconds=value)

    @staticmethod
    def second(value: float):
        return timedelta(seconds=value)

    @staticmethod
    def minute(value: float):
        return timedelta(minutes=value)

    @staticmethod
    def hour(value: float):
        return timedelta(hours=value)

    @staticmethod
    def day(value: float):
        return timedelta(days=value)

    @staticmethod
    def week(value: float):
        return timedelta(weeks=value)

    @staticmethod
    def month(value: float):
        return timedelta(days=value * 30)

    @staticmethod
    def year(value: float):
        return timedelta(days=value * 365)

    @staticmethod
    def decade(value: float):
        return timedelta(days=value * 365 * 10)

    @staticmethod
    def century(value: float):
        return timedelta(days=value * 365 * 100)

    @staticmethod
    def millennium(value: float):
        return timedelta(days=value * 365 * 1000)


class TimeManager:
    def __init__(self):
        self.time_map = {}

    def add_time(self, id: int, time: datetime):
        self.time_map[str(id)] = time

    def increase_time(self, id: int, value, unit: type[Callable[[float], datetime]]):
        if str(id) not in self.time_map:
            raise ValueError("ID not found in the time map.")

        time = self.time_map[str(id)]
        new_time = time + unit(value)
        self.time_map[str(id)] = new_time


manager = TimeManager()

manager.add_time(1, datetime.now())
manager.increase_time(2, 5, Units.minute)
print(manager.time_map['id1'])
