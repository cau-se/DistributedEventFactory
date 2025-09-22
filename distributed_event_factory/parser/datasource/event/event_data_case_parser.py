from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.event.event_data_case_provider import CustomEventDataProvider

class EventDataCaseParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return CustomEventDataProvider(
            activity_provider=self.dependencies["activity"].parse(config["activity"]),
            duration_provider=self.dependencies["duration"].parse(config["duration"]),
            transition_provider=self.dependencies["transition"].parse(config["transition"])
        )