from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.time_uncertainty_post_processor import TimeUncertaintyPostProcessor


class TimeUncertaintyPostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return TimeUncertaintyPostProcessor(
            probability=config["probability"],
            sigma_seconds=config["sigmaSeconds"],
        )
