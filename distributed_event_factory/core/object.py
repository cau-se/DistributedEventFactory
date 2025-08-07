from typing import List

from distributed_event_factory.core.abstract_object_source import ObjectSource
from distributed_event_factory.core.object_id import ObjectId


class ObjectData:
    def __init__(
            self,
            timestamp,
            object_state: str,
            object_id: ObjectId
    ):
        self.timestamp = timestamp
        self.object_state = object_state
        # Maybe call that object type
        self.object_id = object_id


class GenericObjectSource(ObjectSource):

    def __init__(
            self,
            object_id_name: str,
            object_type: str,
            size
    ):
        self.values_changed: List[ObjectData] = []
        self.object_id_name = object_id_name
        self.object_id = ObjectId(object_id_name)
        self.object_type = object_type
        self.size = size

    def emit_object(self, id, object_name, timestamp) -> ObjectData:
        object = ObjectData(
            timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            object_type=self.object_type,
            object_id=self.object_id
        )
        self.values_changed.append(object)
        return object

    def get_id(self) -> ObjectId:
        return self.object_id

    def get_object_type(self) -> str:
        return self.object_type

    def get_size(self):
        return self.size

    def get_last_changed_value(self):
        if self.values_changed:
            return self.values_changed[-1].object_state
        return None

    def add_change(self, change):
        self.values_changed.append(change)

    def clone(self):
        return GenericObjectSource(self.object_id_name,
                                   self.object_type,
                                   self.size)
