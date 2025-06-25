from typing import List, Dict

from core.object import ObjectData, GenericObjectSource
from provider.object.input.input_provider import InputObjectProvider
from provider.transition.output.output_provider import OutputObjectProvider
from simulation.simulator_objects.object_utility import ObjectUtility


class ObjectStorage:

    def __init__(self):
        self.objects: List[GenericObjectSource] = []

    def contains_all_objects(self, objects: List[GenericObjectSource]):
        for obj in objects:
            if not obj in self.objects:
                return False
        return True

    def contains_all_object_of_data(self, objects: List[InputObjectProvider]):
        for obj in objects:
            if not obj.lastState:
                if sum(1 for item in self.objects if
                       item.object_id.id == obj.objectName and not item.values_changed) < obj.numberOfObject:
                    return False
            else:
                if (sum(1 for item in self.objects if
                        item.object_id.id == obj.objectName and item.get_last_changed_value() == obj.lastState)
                        < obj.numberOfObject):
                    return False
        return True

    def add_object(self, obj: GenericObjectSource):
        self.objects.append(obj)

    def add_objects(self, objects: List[GenericObjectSource]):
        for obj in objects:
            self.add_object(obj)

    def find_object_of_data_in_storage(self, obj):
        if obj.lastState:
            return next((item for item in self.objects if
                         item.object_id.id == obj.objectName and item.get_last_changed_value() == obj.lastState), None)
        else:
            return next((item for item in self.objects if
                         item.object_id.id == obj.objectName and not item.values_changed), None)

    def find_object_in_input_objects(self, obj, objects):
        return next((item for item in objects if
                     item.objectName == obj.objectName), None)

    def manage_input_and_output_of_steps(self, input_objects: List[InputObjectProvider],
                                         output_objects: List[OutputObjectProvider],
                                         object_templates: Dict[str, ObjectData], timestamp):
        objects = []
        for input_object in input_objects:
            for i in range(input_object.numberOfObject):
                obj = self.find_object_of_data_in_storage(input_object)
                objects.append(obj)
                self.objects.remove(obj)
        self.add_output_changed_objects_to_store(input_objects, object_templates, output_objects, timestamp)

    def add_output_changed_objects_to_store(self, input_objects, object_templates, output_objects, timestamp):
        for output_object in output_objects:
            for i in range(output_object.numberOfObject):
                obj = self.find_object_in_input_objects(output_object, input_objects)
                if obj:
                    if output_object.change:
                        obj.add_change(ObjectData(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                  object_state=output_object.change,
                                                  object_id=obj.object_id))
                    self.add_object(obj)
                else:
                    obj = ObjectUtility().convert_object_name_to_generic_object(object_templates,
                                                                                output_object.objectName).clone()
                    if output_object.change:
                        obj.add_change(ObjectData(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                  object_state=output_object.change,
                                                  object_id=obj.object_id))
                    self.add_object(obj)
