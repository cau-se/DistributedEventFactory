from typing import List, Dict

from distributed_event_factory.core.object import ObjectData, GenericObjectSource
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.provider.object.size_params_provider import SizeParamsProvider
from distributed_event_factory.provider.transition.output.output_provider import OutputObjectProvider
from distributed_event_factory.simulation.simulator_objects.object_utility import ObjectUtility
from distributed_event_factory.simulation.simulator_objects.workprocessstep import WorkProcessStep


class ObjectStorage:

    def __init__(self):
        self.objects: List[GenericObjectSource] = []

    def contains_all_object_of_data(self, objects: List[InputObjectProvider]):
        for obj in objects:
            if not obj.lastState:
                if not obj.size:
                    if sum(1 for item in self.objects if
                           item.object_id.id.id == obj.objectName and not item.values_changed and not item.size) < obj.numberOfObject:
                        return False
                else:
                    if sum(1 for item in self.objects if
                           item.object_id.id.id == obj.objectName and not item.values_changed and self.object_size_smaller_or_equal(
                               item.size, obj.size)) < obj.numberOfObject:
                        return False
            else:
                if not obj.size:
                    if (sum(1 for item in self.objects if
                            item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState and not item.size)
                            < obj.numberOfObject):
                        return False
                else:
                    if (sum(1 for item in self.objects if
                            item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState and self.object_size_smaller_or_equal(
                                item.size, obj.size))
                            < obj.numberOfObject):
                        return False
        return True

    def contains_all_object_of_data_for_steps(self, steps: List[WorkProcessStep]):
        object_forecast = self.objects.copy()
        possible_workstation_step_pairs = []
        for workstation, step in steps:
            all_objects_possible = True
            for obj in step.input_objects:
                if not obj.lastState:
                    if not obj.size:
                        all_objects_possible = self.contains_objects_without_last_state_without_size_for_steps(
                            all_objects_possible, obj,
                            object_forecast)
                    else:
                        all_objects_possible = self.contains_objects_without_last_state_with_size_for_steps(
                            all_objects_possible, obj,
                            object_forecast)
                else:
                    if not obj.size:
                        all_objects_possible = self.contains_objects_with_last_state_without_size_for_steps(
                            all_objects_possible,
                            obj,
                            object_forecast)
                    else:
                        all_objects_possible = self.contains_objects_with_last_state_with_size_for_steps(
                            all_objects_possible,
                            obj,
                            object_forecast)
            if all_objects_possible:
                possible_workstation_step_pairs.append((workstation, step))
        return possible_workstation_step_pairs

    def contains_objects_with_last_state_without_size_for_steps(self, all_objects_possible, obj, object_forecast):
        if not (sum(1 for item in object_forecast if
                    item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState and not item.size)
                < obj.numberOfObject):
            for i in range(obj.numberOfObject):
                obj_to_remove = self.find_object_of_data_in_storage(obj, object_forecast)
                object_forecast.remove(obj_to_remove)
        else:
            all_objects_possible = False
        return all_objects_possible

    def contains_objects_without_last_state_without_size_for_steps(self, all_objects_possible, obj, object_forecast):
        if not sum(1 for item in object_forecast if
                   item.object_id.id.id == obj.objectName and not item.values_changed and not item.size) < obj.numberOfObject:
            for i in range(obj.numberOfObject):
                obj_to_remove = self.find_object_of_data_in_storage(obj, object_forecast)
                object_forecast.remove(obj_to_remove)
        else:
            all_objects_possible = False
        return all_objects_possible

    def contains_objects_without_last_state_with_size_for_steps(self, all_objects_possible, obj, object_forecast):
        if not sum(1 for item in object_forecast if
                   item.object_id.id.id == obj.objectName and not item.values_changed and self.object_size_smaller_or_equal(
                       item.size, obj.size)) < obj.numberOfObject:
            for i in range(obj.numberOfObject):
                obj_to_remove = self.find_object_of_data_in_storage(obj, object_forecast)
                object_forecast.remove(obj_to_remove)
        else:
            all_objects_possible = False
        return all_objects_possible

    def contains_objects_with_last_state_with_size_for_steps(self, all_objects_possible, obj, object_forecast):
        if not (sum(1 for item in object_forecast if
                    item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState and self.object_size_smaller_or_equal(
                        item.size, obj.size))
                < obj.numberOfObject):
            for i in range(obj.numberOfObject):
                obj_to_remove = self.find_object_of_data_in_storage(obj, object_forecast)
                object_forecast.remove(obj_to_remove)
        else:
            all_objects_possible = False
        return all_objects_possible

    def object_size_smaller_or_equal(self, given_size, wanted_size):
        if (not wanted_size.length and given_size.length) or (
                wanted_size.length and not given_size.length) or (
                given_size.length and wanted_size.length and given_size.length < wanted_size.length):
            return False
        if (not wanted_size.width and given_size.width) or (
                wanted_size.width and not given_size.width) or (
                given_size.width and wanted_size.width and given_size.width < wanted_size.width):
            return False
        if (not wanted_size.depth and given_size.depth) or (
                wanted_size.depth and not given_size.depth) or (
                given_size.depth and wanted_size.depth and given_size.depth < wanted_size.depth):
            return False
        return True

    def get_times_given_object_generates_wanted_object(self, given_size, wanted_size):
        if self.object_size_smaller_or_equal(given_size, wanted_size):
            depth_times = None
            width_times = None
            length_times = None
            if given_size.depth and wanted_size.depth:
                depth_times = round(given_size.depth / wanted_size.depth)
            if given_size.width and wanted_size.width:
                width_times = round(given_size.width / wanted_size.width)
            if given_size.length and wanted_size.length:
                length_times = round(given_size.length / wanted_size.length)
            filtered_numbers = [n for n in [depth_times, width_times, length_times] if n is not None]
            return min(filtered_numbers)
        return 0

    def get_leftover_size_of_given_object(self, given_size, wanted_size):
        factor = self.get_times_given_object_generates_wanted_object(given_size, wanted_size)
        if factor > 0:
            depth = given_size.depth
            width = given_size.width
            length = given_size.length
            if given_size.depth and wanted_size.depth:
                depth = given_size.depth - (wanted_size.depth * factor)
            if given_size.width and wanted_size.width:
                width = given_size.width - (wanted_size.width * factor)
            if given_size.length and wanted_size.length:
                length = given_size.length - (wanted_size.length * factor)
            return SizeParamsProvider(depth=depth, width=width, length=length)
        return given_size

    def are_size_params_empty(self, size_params):
        if not size_params or (not size_params.depth and not size_params.width and not size_params.length):
            return True
        return False

    def add_object(self, obj: GenericObjectSource):
        self.objects.append(obj)

    def add_objects(self, objects: List[GenericObjectSource]):
        for obj in objects:
            self.add_object(obj)

    def find_object_of_data_in_local_storage(self, obj):
        return self.find_object_of_data_in_storage(obj, self.objects)

    def find_object_of_data_in_storage(self, obj, objects):
        if obj.lastState:
            if obj.size:
                return next((item for item in objects if
                             item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState and self.object_size_smaller_or_equal(
                                 item.size, obj.size)),
                            None)
            else:
                return next((item for item in objects if
                             item.object_id.id.id == obj.objectName and item.get_last_changed_value() == obj.lastState and not item.size),
                            None)
        else:
            if obj.size:
                return next((item for item in objects if
                             item.object_id.id.id == obj.objectName and not item.values_changed and self.object_size_smaller_or_equal(
                                 item.size, obj.size)),
                            None)
            else:
                return next((item for item in objects if
                             item.object_id.id.id == obj.objectName and not item.values_changed and not item.size),
                            None)

    def find_object_in_input_objects(self, obj, objects):
        return next((item for item in objects if
                     item.object_id.id.id == obj.objectName), None)

    def find_object_by_id(self, uid):
        return next((item for item in self.objects if
                     item.object_id.unique_id == uid), None)

    def manage_input_and_output_of_steps(self, input_objects: List[InputObjectProvider],
                                         output_objects: List[OutputObjectProvider],
                                         object_templates: Dict[str, ObjectData], timestamp):
        ingoing_objects = []
        outgoing_objects = []
        for input_object in input_objects:
            for i in range(input_object.numberOfObject):
                obj = self.find_object_of_data_in_local_storage(input_object)
                if obj:
                    ingoing_objects.append(obj)
                    self.objects.remove(obj)
                    if obj.size and input_object.size:
                        leftover_size = self.get_leftover_size_of_given_object(obj.size, input_object.size)
                        if not self.are_size_params_empty(leftover_size):
                            obj = obj.clone()
                            obj.add_change(ObjectData(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                      object_state="size: "+str(leftover_size),
                                                      object_id=obj.object_id))
                            obj.size = leftover_size
                            self.add_object(obj)
                            outgoing_objects.append(obj)
                else:
                    return ValueError("Object not found")
        ingoing_objects_copy = ingoing_objects[:]
        outgoing_objects.extend(self.add_output_changed_objects_to_store(ingoing_objects_copy, object_templates, output_objects,
                                                                    timestamp))
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
                    if output_object.size:
                        obj.size.length = output_object.size.length
                        obj.size.width = output_object.size.width
                        obj.size.depth = output_object.size.depth
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

                    if output_object.size:
                        obj.size.length = output_object.size.length
                        obj.size.width = output_object.size.width
                        obj.size.depth = output_object.size.depth
                    self.add_object(obj)
                    outgoing_objects.append(obj)
        return outgoing_objects
