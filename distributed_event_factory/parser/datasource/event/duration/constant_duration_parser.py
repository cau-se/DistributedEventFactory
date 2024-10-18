from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.transition.duration.constant_duration import ConstantDurationProvider


class ConstantDurationParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return ConstantDurationProvider(config["duration"])