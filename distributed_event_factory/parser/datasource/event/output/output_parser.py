from distributed_event_factory.parser.parser import Parser
from provider.object.size_params_provider import SizeParamsProvider
from provider.transition.output.output_provider import OutputObjectProvider


class OutputParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        object_list = []
        for object_element in config:
            size_params = None
            if object_element["size"]:
                size_params = SizeParamsProvider(width=object_element["size"]["width"],
                                                depth=object_element["size"]["depth"],
                                                length=object_element["size"]["length"])
            object_list.append(
                OutputObjectProvider(object_element["object"], object_element["number"], object_element["change"],
                                     size_params))
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