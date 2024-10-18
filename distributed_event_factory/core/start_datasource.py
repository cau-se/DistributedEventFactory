from typing import List

from distributed_event_factory.core.abstract_datasource import DataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, DataSourceId
from distributed_event_factory.core.event import StartEvent, AbstractEvent
from distributed_event_factory.provider.event.event_provider import EventDataProvider, StartEventProvider
from distributed_event_factory.provider.transition.transition.transition_provider import TransitionProvider


class StartDataSource(DataSource):

    def __init__(self, transition_provider: TransitionProvider):
        self.event_log = []
        self.transition_provider = transition_provider

    def get_event_data(self) -> EventDataProvider:
        return StartEventProvider(self.transition_provider).get_event_data()

    def emit_event(self, case, activity, timestamp) -> AbstractEvent:
        return StartEvent(case, self.transition_provider)

    def get_sensor_transition(self) -> tuple[int, int]:
        return 0, self.transition_provider.get_transition()

    def get_id(self) -> DataSourceId:
        return START_SENSOR_ID

    def get_event_log(self) -> List[AbstractEvent]:
        return self.event_log