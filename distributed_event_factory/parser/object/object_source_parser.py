from distributed_event_factory.core.object import GenericObjectSource
from distributed_event_factory.core.object_id import ObjectId
from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from provider.object.size_params_provider import SizeParamsProvider


class ObjectSourceParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        input_list = []
        size_params = None
        if config["input"]:
            for input in config["input"]:
                size_params = None
                if input["size"]:
                    size_params = SizeParamsProvider(width=input["size"]["width"],
                                                     depth=input["size"]["depth"],
                                                     length=input["size"]["length"])
                input_list.append(InputObjectProvider(
                    objectName=input["object"],
                    numberOfObject=input["number"],
                    lastState=input["lastState"],
                    size=size_params,
                ))
        if config["size"]:
            size_params = SizeParamsProvider(length=config["size"]["length"], depth=config["size"]["depth"],
                                             width=config["size"]["width"])
        return GenericObjectSource(
            object_id_name=ObjectId(config["name"]),
            object_type=config["type"],
            input_objects=input_list,
            size=size_params
        )
