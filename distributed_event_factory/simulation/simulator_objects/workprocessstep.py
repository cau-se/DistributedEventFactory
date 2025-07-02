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

    def produce_event(self, current_timestamp, workstation, ingoing_objects, outgoing_objects) -> ObjectEvent:
        return ObjectEvent(
            timestamp=current_timestamp.strftime(Y_M_D_H_M_S),
            activity=self.activity,
            node=self.node,
            group_id=workstation,
            input=", ".join([str(obj) for obj in self.input_objects] +["objectIds: " + ", ".join(obj.object_id.unique_id for obj in ingoing_objects)]),
            output=", ".join([str(obj) for obj in self.output_objects] +["objectIds: " + ", ".join(obj.object_id.unique_id for obj in outgoing_objects)])
        )
