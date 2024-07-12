import abc
from abc import ABC
from typing import List

from core.event import Event, GenEvent, StartEvent, EndEvent
from provider.sender.send_provider import Sender
from provider.transition.duration_provider import DurationProvider
from provider.transition.transition_provider import TransitionProvider
from core.sensor_id import SensorId, START_SENSOR_ID, END_SENSOR_ID


class Sensor(ABC):

    @abc.abstractmethod
    def emit_event(self, case, timestamp) -> None:
        pass

    @abc.abstractmethod
    def get_sensor_transition(self) -> tuple[int, SensorId]:
        pass

    @abc.abstractmethod
    def get_id(self) -> SensorId:
        pass

    @abc.abstractmethod
    def get_event_log(self) -> List[str]:
        pass


class StartSensor(Sensor):

    def __init__(self, transition_provider: TransitionProvider, sender):
        self.event_log = []
        self.transition_provider = transition_provider
        self.sender = sender

    def emit_event(self, case, timestamp):
        event = StartEvent(case)
        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self) -> tuple[int, SensorId]:
        return 0, self.transition_provider.get_next_sensor()

    def get_id(self) -> SensorId:
        return START_SENSOR_ID

    def get_event_log(self) -> List[str]:
        return self.event_log


class EndSensor(Sensor):

    def __init__(self, sender):
        self.event_log = []
        self.sender = sender

    def emit_event(self, case, timestamp):
        event = EndEvent(case)
        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self) -> tuple[int, SensorId]:
        raise ValueError("There is no transition on the end sensor")

    def get_id(self) -> SensorId:
        return END_SENSOR_ID

    def get_event_log(self) -> List[str]:
        return self.event_log


class GenericSensor(Sensor):
    def __init__(
            self,
            sensor_id: SensorId,
            transition_provider: TransitionProvider,
            duration_provider: DurationProvider,
            sender: Sender
    ):
        self.sensor_id: SensorId = sensor_id
        self.transition_provider: TransitionProvider = transition_provider
        self.duration_provider = duration_provider
        self.sender = sender
        self.event_log = []

    def get_id(self) -> SensorId:
        return self.sensor_id

    def emit_event(self, case, timestamp):
        event_name = "Event " + self.sensor_id.id
        event = GenEvent(
            timestamp=timestamp,
            sensor_value=event_name,
            case_id=case,
            sensor_name=self.sensor_id.get_name(),
        )

        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self):
        next_sensor = self.transition_provider.get_next_sensor()
        duration = self.duration_provider.get_duration()
        return duration, next_sensor

    def get_event_log(self):
        return self.event_log
