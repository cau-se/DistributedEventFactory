from src.distributed_event_factory.parser.parser import Parser
from src.distributed_event_factory.provider.load.load_provider import ConstantLoadProvider


class ConstantLoadParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return ConstantLoadProvider(config["load"])