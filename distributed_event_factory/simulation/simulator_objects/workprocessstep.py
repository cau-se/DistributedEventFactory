from distributed_event_factory.simulation.object_event import ObjectEvent
from collections import defaultdict

Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"

class WorkProcessStep:

    def __init__(
            self,
            activity,
            input_objects,
            output_objects,
            duration,
            node,
            group_id,
            workforces_needed,
            start_location,
            end_location
    ):
        self.input_objects = input_objects
        self.workforces_needed = workforces_needed
        self.output_objects = output_objects
        self.duration = duration
        self.activity = activity
        self.node = node
        self.group_id = group_id
        self.start_location = start_location
        self.end_location = end_location

    def clone(self):
        return WorkProcessStep(
            self.activity,
            self.input_objects,
            self.output_objects,
            self.duration,
            self.node,
            self.group_id,
            self.workforces_needed,
            self.start_location,
            self.end_location
        )

    def produce_event(
            self,
            current_timestamp,
            workstation,
            ingoing_objects,
            outgoing_objects
    ) -> ObjectEvent:
        return ObjectEvent(
            timestamp=current_timestamp.strftime(Y_M_D_H_M_S),
            activity=self.activity,
            node=self.node,
            group_id=workstation,
            input=ingoing_objects,
            output=outgoing_objects
        )



class ObjectCounter:
    def __init__(self, objects):
        self.objects = objects
        self.memory = {}

    def count_and_memorize(self):
        groups = defaultdict(list)

        for obj in self.objects:
            key = str(ObjectIdenticalParameters(obj))
            if not groups.get(key):
                groups[key] = [obj.get_id().get_unique_id()]
            else:
                unique_ids = groups.pop(key)
                unique_ids.append(obj.get_id().get_unique_id())
                groups[key] = unique_ids

        for key, unique_ids in groups.items():
            self.memory[key] = {'count': len(unique_ids), 'uniqueIds': unique_ids}

        return self.memory


class ObjectIdenticalParameters:
    def __init__(self, object):
        self.name = object.object_id_name.id
        self.object_type = object.object_type
        self.size = object.size

    def __str__(self):
        return str({
            key: (str(value) if key == "size" or "objects" else value)
            for key, value in self.__dict__.items()
            if value
        })
