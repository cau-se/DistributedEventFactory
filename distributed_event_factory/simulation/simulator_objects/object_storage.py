from typing import List

from core.object import Object


class ObjectStorage:

    def __init__(self):
        self.objects: List[str] = []

    def contains_all_objects(self, objects: List[Object]):
        for obj in objects:
            if not obj in self.objects:
                return False
        return True

    def add_object(self, obj: str):
        self.objects.extend(obj)
