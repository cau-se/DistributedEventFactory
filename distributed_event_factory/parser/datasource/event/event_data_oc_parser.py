from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.event.event_data_oc_provider import EventDataOcProvider


class EventDataOcParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return EventDataOcProvider(
            #TODO hrei Fix here :)
            input_provider=self.dependencies["input"],
            output_provider=self.dependencies["output"].parse(config["output"]),
            activity_provider=self.dependencies["activity"].parse(config["activity"]),
            duration_provider=self.dependencies["duration"].parse(config["duration"]),
            transition_provider=self.dependencies["transition"].parse(config["transition"])
        )