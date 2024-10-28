import os

from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.load.load_provider import ConstantLoadProvider


class ConstantLoadParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        if "load" in os.environ:
            load = int(os.environ["LOAD"])
        else:
            load = config["load"]
        return ConstantLoadProvider(load)