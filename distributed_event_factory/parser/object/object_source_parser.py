from distributed_event_factory.core.object import GenericObjectSource
from distributed_event_factory.core.object_id import ObjectId
from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.provider.object.size_params_provider import SizeParamsProvider


class ObjectSourceParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        size_params = None
        if "size" in config and config["size"]:
            size_params = SizeParamsProvider(length=config["size"]["length"], depth=config["size"]["depth"],
                                             width=config["size"]["width"])
        return GenericObjectSource(
            object_id_name=ObjectId(config["name"]),
            object_type=config["type"],
            size=size_params
        )
