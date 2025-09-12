import uuid
class ObjectId:
    def __init__(self, data_source_id: str):
        self.id: str = data_source_id
        self.unique_id = str(uuid.uuid4())

    def __eq__(self, other):
        return hasattr(other, "id") and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_name(self):
        return self.id

    def get_unique_id(self):
        return self.unique_id