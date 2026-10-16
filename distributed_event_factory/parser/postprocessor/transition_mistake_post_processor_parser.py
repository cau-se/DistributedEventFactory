from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.transition_mistake_post_processor import (
    TransitionMistakePostProcessor,
)


class TransitionMistakePostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return TransitionMistakePostProcessor(probability=config["probability"])
