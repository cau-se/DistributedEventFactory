from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.transition.duration.uniform_duration import UniformDurationProvider


class UniformDurationParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return UniformDurationProvider(config["lowerBound"], config["upperBound"])