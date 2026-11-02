import copy
import random

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class InsertionPostProcessor(PostProcessor):
    """Adds an event with an alternative activity at the same node."""

    def __init__(self, probability: float):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")
        self.probability = probability
        self.transition_activities = {}

    def set_transition_alternatives(self, transition_activities):
        self.transition_activities = {
            node: list(dict.fromkeys(activities))
            for node, activities in transition_activities.items()
        }

    def process(self, event):
        if random.random() >= self.probability:
            return event

        activity_attribute = "activity" if hasattr(event, "activity") else "sensor_value"
        activity = getattr(event, activity_attribute, None)
        alternatives = [
            alternative
            for alternative in self.transition_activities.get(event.node, ())
            if alternative != activity
        ]
        if not alternatives:
            return event

        inserted_event = copy.copy(event)
        setattr(inserted_event, activity_attribute, random.choice(alternatives))
        print(
            "PostProcessor [insertion]: inserted alternative activity "
            f"{getattr(inserted_event, activity_attribute)!r} at node {event.node!r}"
        )
        return [event, inserted_event]
