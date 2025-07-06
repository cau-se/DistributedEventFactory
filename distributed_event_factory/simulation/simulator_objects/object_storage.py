from typing import List, Dict

from core.object import ObjectData, GenericObjectSource
from provider.object.input.input_provider import InputObjectProvider
from provider.transition.output.output_provider import OutputObjectProvider
from simulation.simulator_objects.object_utility import ObjectUtility
from simulation.simulator_objects.workprocessstep import WorkProcessStep


class ObjectStorage:

    def __init__(self):
        self.objects: List[GenericObjectSource] = []

    def contains_all_object_of_data(self, objects: List[InputObjectProvider]):
        for obj in objects:
            if not obj.lastState:
                if sum(1 for item in self.objects if
                       item.object_id.id.id == obj.objectName and not item.values_changed) < obj.numberOfObject:
                    return False
            else:
                if (sum(1 for item in self.objects if
                        item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState)
                        < obj.numberOfObject):
                    return False
        return True

    def contains_all_object_of_data_for_steps(self, steps: List[WorkProcessStep]):
        object_forecast = self.objects.copy()
        possible_steps = []
        for workstation, step in steps:
            all_objects_possible = True
            for obj in step.input_objects:
                if not obj.lastState:
                    if not sum(1 for item in object_forecast if
                               item.object_id.id.id == obj.objectName and not item.values_changed) < obj.numberOfObject:
                        for i in range(obj.numberOfObject):
                            obj_to_remove = self.find_object_of_data_in_storage(obj, object_forecast)
                            object_forecast.remove(obj_to_remove)
                    else:
                        all_objects_possible = False
                else:
                    if not (sum(1 for item in object_forecast if
                                item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState)
                            < obj.numberOfObject):
                        for i in range(obj.numberOfObject):
                            obj_to_remove = self.find_object_of_data_in_storage(obj, object_forecast)
                            object_forecast.remove(obj_to_remove)
                    else:
                        all_objects_possible = False
            if all_objects_possible:
                possible_steps.append((workstation, step))
        return possible_steps

    def add_object(self, obj: GenericObjectSource):
        self.objects.append(obj)

    def add_objects(self, objects: List[GenericObjectSource]):
        for obj in objects:
            self.add_object(obj)

    def find_object_of_data_in_local_storage(self, obj):
        return self.find_object_of_data_in_storage(obj, self.objects)

    def find_object_of_data_in_storage(self, obj, objects):
        if obj.lastState:
            return next((item for item in objects if
                         item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState),
                        None)
        else:
            return next((item for item in objects if
                         item.object_id.id.id == obj.objectName and not item.values_changed), None)

    def find_object_in_input_objects(self, obj, objects):
        return next((item for item in objects if
                     item.object_id.id.id == obj.objectName), None)

    def manage_input_and_output_of_steps(self, input_objects: List[InputObjectProvider],
                                         output_objects: List[OutputObjectProvider],
                                         object_templates: Dict[str, ObjectData], timestamp):
        ingoing_objects = []
        for input_object in input_objects:
            for i in range(input_object.numberOfObject):
                obj = self.find_object_of_data_in_local_storage(input_object)
                if obj:
                    ingoing_objects.append(obj)
                    self.objects.remove(obj)
                else:
                    return ValueError("Object not found")
        outgoing_objects = self.add_output_changed_objects_to_store(ingoing_objects, object_templates, output_objects,
                                                                    timestamp)
        return ingoing_objects, outgoing_objects

    def add_output_changed_objects_to_store(self, objects, object_templates, output_objects, timestamp):
        outgoing_objects = []
        for output_object in output_objects:
            for i in range(output_object.numberOfObject):
                obj = self.find_object_in_input_objects(output_object, objects)
                if obj:
                    if output_object.change:
                        obj.add_change(ObjectData(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                  object_state=output_object.change,
                                                  object_id=obj.object_id))
                    self.add_object(obj)
                    outgoing_objects.append(obj)
                    objects.remove(obj)
                else:
                    obj = ObjectUtility().convert_object_name_to_generic_object(object_templates,
                                                                                output_object.objectName).clone()
                    if output_object.change:
                        obj.add_change(ObjectData(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                  object_state=output_object.change,
                                                  object_id=obj.object_id))
                    self.add_object(obj)
                    outgoing_objects.append(obj)
        return outgoing_objects
