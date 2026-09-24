from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.payload.fixed_payload_update import FixedPayloadUpdateProvider


class PayloadUpdateParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        if config is None:
            return FixedPayloadUpdateProvider(0)

        return self.dependencies[config["type"]].parse(config)
