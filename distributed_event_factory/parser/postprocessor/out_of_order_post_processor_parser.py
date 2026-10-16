from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.out_of_order_post_processor import OutOfOrderPostProcessor


class OutOfOrderPostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return OutOfOrderPostProcessor(
            probability=config["probability"],
            window_size=config["windowSize"],
        )
