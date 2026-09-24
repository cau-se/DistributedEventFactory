import random

from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class DropRatePostProcessor(PostProcessor):
    def __init__(self, drop_rate: float):
        if drop_rate < 0 or drop_rate > 1:
            raise ValueError("dropRate must be between 0 and 1")
        self.drop_rate = drop_rate

    def process(self, event: Event):
        if random.random() < self.drop_rate:
            print("dropped")
            return None
        return event
