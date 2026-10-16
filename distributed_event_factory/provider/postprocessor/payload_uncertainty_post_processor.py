import random

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class PayloadUncertaintyPostProcessor(PostProcessor):
    def __init__(self, probability: float, sigma: float):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")
        if sigma < 0:
            raise ValueError("sigma must not be negative")
        self.probability = probability
        self.sigma = sigma

    def process(self, event):
        payload = getattr(event, "payload", None)
        if payload is not None and random.random() < self.probability:
            noisy_payload = min(100.0, max(0.0, payload + random.gauss(0, self.sigma)))
            if noisy_payload != payload:
                event.payload = noisy_payload
                print(f"PostProcessor [payloadUncertainty]: changed payload {payload!r} -> {noisy_payload!r}")
        return event
