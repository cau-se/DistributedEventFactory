from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.payload.uniform_payload_update import UniformPayloadUpdateProvider


class UniformPayloadUpdateParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return UniformPayloadUpdateProvider(config["lowerBound"], config["upperBound"])
