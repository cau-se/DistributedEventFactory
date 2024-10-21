from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.load.sinus_load_provider import SinusLoadProvider


class SinusLoadParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return SinusLoadProvider(config["mean"], config["amplitude"], config["phase"])