from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.drop_rate_post_processor import DropRatePostProcessor


class DropRatePostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return DropRatePostProcessor(drop_rate=config["dropRate"])
