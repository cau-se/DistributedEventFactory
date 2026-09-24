from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.payload.gaussian_payload_update import GaussianPayloadUpdateProvider


class GaussianPayloadUpdateParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return GaussianPayloadUpdateProvider(config["mu"], config["sigma"])
