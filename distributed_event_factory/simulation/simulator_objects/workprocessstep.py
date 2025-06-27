from datetime import timedelta, datetime

from process_mining_core.datastructure.core.event import Event

from simulation.object_event import ObjectEvent

Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"

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
        self.last_event_end_timestamp = None

    def produce_event(self, current_timestamp, workstation) -> ObjectEvent:
        return ObjectEvent(
            timestamp=self.add_to_last_timestamp(current_timestamp, self.duration).strftime(Y_M_D_H_M_S),
            activity=self.activity,
            node=self.node,
            group_id=workstation,
            input=", ".join(str(obj) for obj in self.input_objects),
            output=", ".join(str(obj) for obj in self.output_objects)
        )

    def add_to_last_timestamp(self, current_timestamp, duration):
        self.last_event_end_timestamp = current_timestamp + timedelta(seconds=duration)
        return self.last_event_end_timestamp
