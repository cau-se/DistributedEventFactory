from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider
from distributed_event_factory.provider.event.event_data import EventData
from distributed_event_factory.provider.transition.duration.duration_provider import ConstantDurationProvider
from distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import ConstantNextSensorProvider


class EventDataParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return EventData(
            duration_provider=ConstantDurationProvider(config["duration"]),
            activity_provider=ConstantActivityProvider(config["activity"]),
            transition_provider=ConstantNextSensorProvider(config["transition"])
        )