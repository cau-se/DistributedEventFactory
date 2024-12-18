from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.data.constant_count_provider import ConstantCountProvider


class ConstantCountParser(Parser):

    def parse(self, config):
        return ConstantCountProvider(config)

    def add_dependency(self, key: str, dependency):
        pass