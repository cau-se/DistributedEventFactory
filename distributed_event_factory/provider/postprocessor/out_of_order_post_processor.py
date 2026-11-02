import random

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class OutOfOrderPostProcessor(PostProcessor):
    def __init__(self, probability: float, window_size: int):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")
        if window_size < 2:
            raise ValueError("windowSize must be at least 2")
        self.probability = probability
        self.window_size = window_size
        self.event_window = []

    def process(self, event):
        self.event_window.append(event)
        if len(self.event_window) < self.window_size:
            return None

        events = self.event_window
        self.event_window = []
        if random.random() < self.probability:
            if self._reorder(events):
                self._print_reordering(events)
        return events

    def flush(self):
        events = self.event_window
        self.event_window = []
        if events and random.random() < self.probability:
            if self._reorder(events):
                self._print_reordering(events)
        return events

    @staticmethod
    def _reorder(events):
        original_order = [id(event) for event in events]
        random.shuffle(events)
        if [id(event) for event in events] == original_order:
            events.append(events.pop(0))
        return [id(event) for event in events] != original_order

    @staticmethod
    def _print_reordering(events):
        activities = [getattr(event, "activity", getattr(event, "sensor_value", None)) for event in events]
        print(f"PostProcessor [outOfOrder]: reordered stream window: {activities!r}")
