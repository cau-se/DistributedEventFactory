import abc
import datetime


class Event:
    @abc.abstractmethod
    def get_case(self):
        pass


class StartEvent(Event):
    def __init__(self, case_id):
        self.case_id = case_id

    def get_case(self):
        return self.case_id

    def __str__(self):
        return f"<Start of case {self.case_id}>"


class EndEvent(Event):

    def __init__(self, case_id):
        self.case_id = case_id

    def get_case(self):
        return self.case_id

    def __str__(self):
        return f"<End of case {self.case_id}>"

class GenEvent(Event):
    def __init__(self, timestamp, sensor_value, case_id, sensor_name):
        self.timestamp: datetime.datetime = timestamp
        self.sensor_value: any = sensor_value
        self.case_id: str = case_id
        self.sensor_name: str = sensor_name

    def get_case(self):
        return self.get_case()

    def __str__(self):
        return str(self.__dict__)
