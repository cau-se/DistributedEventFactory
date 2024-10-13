from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.load.load_provider import GradualIncreasingLoadProvider


class GradualLoadParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return GradualIncreasingLoadProvider(config["tickCount"], config["minimalLoad"], config["load"])