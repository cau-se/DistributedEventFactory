from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.postprocessor.missing_data_post_processor import MissingDataPostProcessor


class MissingDataPostProcessorParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return MissingDataPostProcessor(
            payload_probability=config.get("payloadProbability", 0.0),
            timestamp_probability=config.get("timestampProbability", 0.0),
            activity_probability=config.get("activityProbability", 0.0),
        )
