import random
from datetime import datetime, timedelta

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class TimeUncertaintyPostProcessor(PostProcessor):
    def __init__(self, probability: float, sigma_seconds: float):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")
        if sigma_seconds < 0:
            raise ValueError("sigmaSeconds must not be negative")
        self.probability = probability
        self.sigma_seconds = sigma_seconds

    def process(self, event):
        if event.timestamp is None or random.random() >= self.probability:
            return event

        timestamp = event.timestamp
        original_timestamp = timestamp
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        timestamp += timedelta(seconds=random.gauss(0, self.sigma_seconds))
        event.timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        if event.timestamp != original_timestamp:
            print(
                "PostProcessor [timeUncertainty]: "
                f"changed timestamp {original_timestamp!r} -> {event.timestamp!r}"
            )
        return event
