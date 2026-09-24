from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.payload.fixed_payload_update import FixedPayloadUpdateProvider


class FixedPayloadUpdateParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return FixedPayloadUpdateProvider(config["value"])
