from src.distributed_event_factory.parser.parser import Parser
from src.distributed_event_factory.provider.transition.duration.duration_provider import ConstantDurationProvider


class ConstantDurationParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return ConstantDurationProvider(config["duration"])