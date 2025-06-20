from datetime import timedelta

from process_mining_core.datastructure.core.event import Event

from simulation.object_event import ObjectEvent


class WorkProcessStep:

    def __init__(
            self,
            activity,
            input_objects,
            output_objects,
            duration,
            node,
            group_id
    ):
        self.input_objects = input_objects
        self.output_objects = output_objects
        self.duration = duration
        self.activity = activity
        self.node = node
        self.group_id = group_id

    def produce_event(self, current_timestamp) -> ObjectEvent:
        return ObjectEvent(
            timestamp=self.add_to_last_timestamp(current_timestamp, self.duration),
            activity=self.activity,
            node=self.node,
            group_id=self.group_id,
            input=self.input_objects,
            output=self.output_objects
        )

    def add_to_last_timestamp(self, current_timestamp, duration):
        return current_timestamp + timedelta(seconds=duration)
