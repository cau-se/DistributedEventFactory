from core.object import GenericObjectSource, ObjectData
from typing import Dict, List


class ObjectUtility:

    def convert_object_data_to_generic_objects(self, generic_objects_possible:Dict[str,GenericObjectSource], object_data:ObjectData):
        objects:List[GenericObjectSource]=[]
        obj = generic_objects_possible[object_data.objectName]
        for i in range(object_data.numberOfObject):
            objects.append(obj.clone())
        return objects

    def convert_object_name_to_generic_object(self, generic_objects_possible: Dict[str,GenericObjectSource],
                                               object_name: str):
        return generic_objects_possible[object_name]
