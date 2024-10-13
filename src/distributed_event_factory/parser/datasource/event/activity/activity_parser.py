from src.distributed_event_factory.parser.parser import Parser
from src.distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider
from src.distributed_event_factory.provider.transition.duration.duration_provider import ConstantDurationProvider


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