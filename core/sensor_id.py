class SensorId:
    def __init__(self, id: str):
        self.id: str = id

    def __eq__(self, other):
        return hasattr(other, "id") and self.id == other.id

    def get_name(self):
        return self.id


START_SENSOR_ID = SensorId("<start>")
END_SENSOR_ID = SensorId("<end>")
