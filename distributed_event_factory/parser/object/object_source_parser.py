from distributed_event_factory.core.object import GenericObjectSource
from distributed_event_factory.core.object_id import ObjectId
from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider

class ObjectSourceParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        input_list = []
        if config["input"]:
            for input in config["input"]:
                input_list.append(InputObjectProvider(
                    objectName=input["object"],
                    numberOfObject=input["number"],
                    lastState=input["lastState"]
                ))
        return GenericObjectSource(
            object_id=ObjectId(config["name"]),
            object_type=config["type"],
            input_objects=input_list,
            length=config["length"],
            width=config["width"]
        )
