import random
from typing import Dict, List

from distributed_event_factory.provider.postprocessor.post_processor import PostProcessor


class TransitionMistakePostProcessor(PostProcessor):
    """Randomly rewrites an event activity to another transition of the same datasource."""

    def __init__(self, probability: float):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be between 0 and 1")
        self.probability = probability
        self.transition_activities: Dict[str, List[str]] = {}

    def set_transition_alternatives(self, transition_activities: Dict[str, List[str]]) -> None:
        self.transition_activities = {
            node: list(dict.fromkeys(activities))
            for node, activities in transition_activities.items()
        }

    def process(self, event: "Event"):
        if random.random() >= self.probability:
            return event

        alternatives = [
            activity
            for activity in self.transition_activities.get(event.node, ())
            if activity != event.activity
        ]
        if alternatives:
            original_activity = event.activity
            event.activity = random.choice(alternatives)
            print(
                "PostProcessor [transitionMistake]: "
                f"changed activity {original_activity!r} -> {event.activity!r} "
                f"for node {event.node!r}"
            )
        return event
