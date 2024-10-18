class DataSourceId:
    def __init__(self, data_source_id: str):
        self.id: str = data_source_id

    def __eq__(self, other):
        return hasattr(other, "id") and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_name(self):
        return self.id


START_SENSOR_ID = DataSourceId("<start>")
END_DATA_SOURCE_ID = DataSourceId("<end>")
