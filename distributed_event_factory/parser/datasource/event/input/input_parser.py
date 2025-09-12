from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.provider.object.size_params_provider import SizeParamsProvider

class InputParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        object_list = []
        for object_element in config["input"]:
            size_params = None
            if "size" in object_element and object_element["size"]:
                size_params = SizeParamsProvider(width=object_element["size"]["width"],
                                                 depth=object_element["size"]["depth"],
                                                 length=object_element["size"]["length"])
            object_list.append(
                InputObjectProvider(object_element["object"], object_element["number"], object_element["lastState"],
                                    size_params))
        return object_list