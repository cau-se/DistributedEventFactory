from distributed_event_factory.parser.parser import Parser
from provider.object.input.input_provider import InputObjectProvider


class InputParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        object_list = []
        for object_element in config["input"]:
            object_list.append(InputObjectProvider(object_element["object"], object_element["number"]))
        return object_list