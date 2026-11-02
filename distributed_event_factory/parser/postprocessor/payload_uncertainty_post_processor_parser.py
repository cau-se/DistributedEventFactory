from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.payload_uncertainty_post_processor import PayloadUncertaintyPostProcessor


class PayloadUncertaintyPostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return PayloadUncertaintyPostProcessor(
            probability=config["probability"],
            sigma=config["sigma"],
        )
