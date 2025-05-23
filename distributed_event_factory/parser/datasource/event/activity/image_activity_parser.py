from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.activity.image_activity_provider import ImageActivityProvider


class ImageActivityParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return ImageActivityProvider(activity=config["activity"])