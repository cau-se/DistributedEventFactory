from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.activity_provider import ObjectConstantActivityProvider


class ObjectConstantActivityParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    # TODO hrei: Check whether that can be put to the base class
    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return ObjectConstantActivityProvider(config["name"], self.dependencies["output"].parse(config["output"]))