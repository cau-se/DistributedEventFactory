from typing import List

from distributed_event_factory.core.object import ObjectData
from distributed_event_factory.simulation.simulator_objects.workprocessstep import WorkProcessStep

class ObjectStorageV2:

    def __init__(self):
        self.objects: List[ObjectData] = []

    def add_object(self, object: ObjectData):
        self.objects.append(object)

    def add_objects(self, objects: List[ObjectData]):
        for object in objects:
            self.add_object(object)

    def remove_object(self, input_object: ObjectData):
        for object in self.objects:
            if input_object.objectName == object.object_type:
                self.objects.remove(object)
                return

    def are_all_inputs_available(self, input_objects: List[ObjectData]) -> bool:
        for input_object in input_objects:
            if not self.is_input_available(input_object):
                return False
        return True

    def is_input_available(self, input_object: ObjectData) -> bool:
        for object in self.objects:
            if object.object_type == input_object.objectName:
                return True
        return False

    def filter_executable_events(self, events: List[WorkProcessStep]) -> List[WorkProcessStep]:
        executable_events = []
        for event in events:
            if self.are_all_inputs_available(event.input_objects):
                executable_events.append(event)
        return executable_events

    def process_event(self, event: WorkProcessStep):
        if not self.are_all_inputs_available(event.input_objects):
            print("Warning: InputObject has not been available")
        for input_object in event.input_objects:
            self.remove_object(input_object)
        for output_object in event.output_objects:
            self.add_object(output_object)