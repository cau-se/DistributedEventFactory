from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.activity_provider import ConstantActivityProvider
from provider.activity.activity_provider import ObjectConstantActivityProvider


class ActivityParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        # TODO hrei: Check how to get rid of instance of
        if isinstance(config, str):
            return ConstantActivityProvider(config)
        elif isinstance(config, dict):
            return ObjectConstantActivityProvider(config["name"], self.dependencies["output"].parse(config["output"]))
        return self.dependencies[config["type"]].parse(config)