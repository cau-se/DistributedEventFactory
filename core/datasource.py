from abc import abstractmethod, ABC
from typing import List

from core.event import Event, StartEvent, EndEvent, AbstractEvent
from provider.activity.activity_emission_provider import ActivityEmissionProvider
from provider.sender.send_provider import Sender
from provider.transition.duration_provider import DurationProvider
from provider.transition.transition_provider import TransitionProvider
from core.datasource_id import DataSourceId, START_SENSOR_ID, END_SENSOR_ID


class DataSource(ABC):

    @abstractmethod
    def emit_event(self, case, timestamp) -> None:
        pass

    @abstractmethod
    def get_sensor_transition(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def get_id(self) -> DataSourceId:
        pass

    @abstractmethod
    def get_event_log(self) -> List[AbstractEvent]:
        pass


class StartDataSource(DataSource):

    def __init__(self, transition_provider: TransitionProvider, sender):
        self.event_log = []
        self.transition_provider = transition_provider
        self.sender = sender

    def emit_event(self, case, timestamp) -> None:
        event = StartEvent(case)
        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self) -> tuple[int, int]:
        return 0, self.transition_provider.get_next_sensor()

    def get_id(self) -> DataSourceId:
        return START_SENSOR_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log


class EndDataSource(DataSource):

    def __init__(self, sender):
        self.event_log = []
        self.sender = sender

    def emit_event(self, case, timestamp) -> None:
        event = EndEvent(case)
        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self) -> tuple[int, int]:
        raise ValueError("There is no transition on the end datasource")

    def get_id(self) -> DataSourceId:
        return END_SENSOR_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log


class GenericDataSource(DataSource):
    def __init__(
            self,
            sensor_id: DataSourceId,
            transition_provider: TransitionProvider,
            duration_provider: DurationProvider,
            sender: Sender,
            activity_emission_provider: ActivityEmissionProvider
    ):
        self.sensor_id: DataSourceId = sensor_id
        self.transition_provider: TransitionProvider = transition_provider
        self.duration_provider = duration_provider
        self.sender = sender
        self.event_log: List[AbstractEvent] = []
        self.event_emission_provider = activity_emission_provider

    def get_id(self) -> DataSourceId:
        return self.sensor_id

    def emit_event(self, case, timestamp) -> None:
        activity_name = self.event_emission_provider.emit_activity(payload=0)

        event = Event(
            timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            sensor_value=activity_name,
            case_id=case,
            sensor_name=self.sensor_id.get_name(),
        )

        self.event_log.append(event)
        self.sender.send(event)

    def get_sensor_transition(self) -> tuple[int, int]:
        next_sensor = self.transition_provider.get_next_sensor()
        duration = self.duration_provider.get_duration()
        return duration, next_sensor

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log