from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.insertion_post_processor import InsertionPostProcessor


class InsertionPostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return InsertionPostProcessor(probability=config["probability"])
