from typing import List

from core.object import ObjectData, GenericObjectSource
from provider.object.input.input_provider import InputObjectProvider


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
            for i in range(obj.numberOfObject):
                if not next((item for item in self.objects if item.object_id.id == obj.objectName), None):
                    return False
        return True

    def add_object(self, obj: GenericObjectSource):
        self.objects.append(obj)

    def add_objects(self, objects: List[GenericObjectSource]):
        for obj in objects:
            self.add_object(obj)
