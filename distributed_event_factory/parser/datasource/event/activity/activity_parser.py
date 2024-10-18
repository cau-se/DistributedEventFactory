from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider


class ActivityParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        if isinstance(config, str):
            return ConstantActivityProvider(config)
        return self.dependencies[config["type"]].parse(config)