from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.transition.output.output_provider import OutputObjectProvider


class OutputParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        object_list = []
        for object_element in config:
            object_list.append(OutputObjectProvider(object_element["object"], object_element["number"], object_element["change"]))
        return object_list

class DummyObjectParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        object_list = []
        return object_list