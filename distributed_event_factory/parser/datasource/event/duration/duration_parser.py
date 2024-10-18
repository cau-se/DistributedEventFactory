from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.transition.duration.constant_duration import ConstantDurationProvider


class DurationParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        if isinstance(config, int):
            return ConstantDurationProvider(config)
        return self.dependencies[config["type"]].parse(config)