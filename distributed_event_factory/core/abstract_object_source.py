from abc import ABC, abstractmethod
from distributed_event_factory.core.object_id import ObjectId


class ObjectSource(ABC):

    @abstractmethod
    def emit_object(self, id, object_name, timestamp) -> None:
        pass

    @abstractmethod
    def get_id(self) -> ObjectId:
        pass

    @abstractmethod
    def get_object_type(self) -> str:
        pass

    #@abstractmethod
    #def get_input_objects(self) -> []:
    #    pass
