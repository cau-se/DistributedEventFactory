from abc import abstractmethod, ABC

from src.distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, \
    AbstractNextSensorProvider


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
    def __init__(self, case_id: CaseId, transition_provider: AbstractNextSensorProvider):
        self.case_id = case_id
        self.transition_provider = transition_provider
        self.node = "start"

    def get_case(self):
        return self.case_id

    def get_next_sensor(self):
        return self.transition_provider.get_next_sensor()

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
        self.activity: any = sensor_value
        self.caseId: CaseId = case_id
        self.node: str = sensor_name
        self.group: str = group_id

    def get_case(self):
        return self.caseId

    def __str__(self):
        return str(self.__dict__)
