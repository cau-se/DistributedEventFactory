from typing import Dict, List

from distributed_event_factory.core.object import GenericObjectSource, ObjectData


class ObjectUtility:

    def convert_object_data_to_generic_objects(self, generic_objects_possible:Dict[str,GenericObjectSource], object_data:ObjectData, timestamp):
        objects:List[GenericObjectSource]=[]
        obj = generic_objects_possible[object_data.objectName].clone()
        for i in range(object_data.numberOfObject):
            obj = obj.clone()
            if object_data.lastState:
                obj.add_change(ObjectData(timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"), object_state=object_data.lastState,
                                              object_id=obj.object_id))
            objects.append(obj)
        return objects

    def convert_object_name_to_generic_object(self, generic_objects_possible: Dict[str,GenericObjectSource],
                                               object_name: str):
        return generic_objects_possible[object_name]
