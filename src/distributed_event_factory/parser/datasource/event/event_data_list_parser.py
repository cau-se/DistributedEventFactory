from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider
from distributed_event_factory.provider.event.event_provider import CustomEventDataProvider
from distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import ConstantNextSensorProvider

class EventDataListParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        event_list = []
        for event in config:
            event_list.append(CustomEventDataProvider(
                duration_provider=self.dependencies["duration"].parse(event["duration"]),
                activity_provider=self.dependencies["activity"].parse(event["activity"]),
                transition_provider=self.dependencies["transition"].parse(event["transition"])))
        return event_list
