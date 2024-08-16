from abc import abstractmethod, ABC


class CaseId:
    def __init__(self, case_id: str):
        self.case_id = case_id


class Activity:
    def __init__(self, activity: str):
        self.activity = activity


class AbstractEvent(ABC):
    @abstractmethod
    def get_case(self) -> CaseId:
        pass


class StartEvent(AbstractEvent):
    def __init__(self, case_id: CaseId):
        self.case_id = case_id

    def get_case(self):
        return self.case_id

    def __str__(self):
        return f"<Start of case {self.case_id}>"


class EndEvent(AbstractEvent):

    def __init__(self, case_id: CaseId):
        self.case_id = case_id

    def get_case(self):
        return self.case_id

    def __str__(self):
        return f"<End of case {self.case_id}>"


class Event(AbstractEvent):
    def __init__(self, timestamp, sensor_value, case_id: CaseId, sensor_name, group_id):
        self.timestamp = timestamp
        self.sensor_value: any = sensor_value
        self.case_id: CaseId = case_id
        self.sensor_name: str = sensor_name
        self.group_id: str = group_id

    def get_case(self):
        return self.case_id

    def __str__(self):
        return str(self.__dict__)
