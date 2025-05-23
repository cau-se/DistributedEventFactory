from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider


class ConstantActivityParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return ConstantActivityProvider(config)