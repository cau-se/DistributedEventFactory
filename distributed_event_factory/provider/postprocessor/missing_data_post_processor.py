import random

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class MissingDataPostProcessor(PostProcessor):
    def __init__(self, payload_probability: float, timestamp_probability: float, activity_probability: float):
        probabilities = (payload_probability, timestamp_probability, activity_probability)
        if any(not 0.0 <= probability <= 1.0 for probability in probabilities):
            raise ValueError("missing-data probabilities must be between 0 and 1")
        self.payload_probability = payload_probability
        self.timestamp_probability = timestamp_probability
        self.activity_probability = activity_probability

    def process(self, event):
        missing_fields = []
        if random.random() < self.payload_probability:
            event.payload = None
            missing_fields.append("payload")
        if random.random() < self.timestamp_probability:
            event.timestamp = None
            missing_fields.append("timestamp")
        if random.random() < self.activity_probability:
            if hasattr(event, "activity"):
                event.activity = None
                missing_fields.append("activity")
            elif hasattr(event, "sensor_value"):
                event.sensor_value = None
                missing_fields.append("activity")
        if missing_fields:
            print(f"PostProcessor [missingData]: removed {', '.join(missing_fields)}")
        return event
