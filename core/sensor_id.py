class SensorId:
    def __init__(self, id: str):
        self.id: str = id

    def get_name(self):
        return self.id

START_SENSOR = SensorId("<start>")
END_SENSOR = SensorId("<end>")