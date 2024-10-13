from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import ConstantNextSensorProvider


class TransitionParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        if isinstance(config, str):
            return ConstantNextSensorProvider(config)
        return self.dependencies[config["type"]].parse(config)