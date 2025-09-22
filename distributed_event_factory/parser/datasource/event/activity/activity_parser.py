from distributed_event_factory.parser.parser import Parser

class ActivityParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        if isinstance(config, str):
            return self.dependencies["constant"].parse(config)
        return self.dependencies[config["type"]].parse(config)