from datetime import timedelta, datetime

from distributed_event_factory.simulation.object_event import ObjectEvent
from process_mining_core.datastructure.core.event import Event


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

    def produce_event(self, current_timestamp, workstation) -> ObjectEvent:
        return ObjectEvent(
            timestamp=current_timestamp.strftime(Y_M_D_H_M_S),
            activity=self.activity,
            node=self.node,
            group_id=workstation,
            input=", ".join(str(obj) for obj in self.input_objects),
            output=", ".join(str(obj) for obj in self.output_objects)
        )
