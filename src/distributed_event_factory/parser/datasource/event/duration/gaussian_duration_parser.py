from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.transition.duration.gaussian_duration import GaussianDurationProvider


class GaussianDurationParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return GaussianDurationProvider(config["mu"], config["sigma"])