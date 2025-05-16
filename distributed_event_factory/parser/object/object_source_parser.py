from distributed_event_factory.core.object import GenericObjectSource
from distributed_event_factory.core.object_id import ObjectId
from distributed_event_factory.parser.parser import Parser

class ObjectSourceParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return GenericObjectSource(
            object_id=ObjectId(config["name"]),
            object_type=config["type"],
            input_objects=config["input"].split(","),
            length=config["length"],
            width=config["width"]
        )
