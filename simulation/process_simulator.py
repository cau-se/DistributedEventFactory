import random
from datetime import datetime, timedelta
from typing import List

from core.sensor import Sensor
from core.sensor_id import END_SENSOR_ID, START_SENSOR_ID
from provider.data.case_provider import CaseIdProvider


class ProcessSimulator:
    def __init__(self, sensors, case_id_provider: CaseIdProvider):
        self.tokens: List[Token] = []
        self.sensors: List[Sensor] = sensors
        self.case_id_provider = case_id_provider
        self.last_time = datetime.now()

    def simulate(self):
        if not self.tokens:
            case_id = self.case_id_provider.get()
            self.tokens.append(Token(case_id, START_SENSOR_ID, self.last_time))

        token = self.tokens[int(random.uniform(0, len(self.tokens)))]
        current_sensor = self._get_sensor_with_id(token.sensor_id)

        if token.sensor_id == END_SENSOR_ID:
            current_sensor.emit_event(token.case, token.last_timestamp)
            self.tokens.remove(token)
        else:
            duration, next_sensor_index = current_sensor.get_sensor_transition()
            token.add_to_last_timestamp(duration=duration)
            last_timestamp = token.last_timestamp
            current_sensor.emit_event(token.case, last_timestamp)
            self.last_time = last_timestamp
            # exclusion of start sensor
            token.set_sensor(self.sensors[next_sensor_index + 1].get_id())

    def _get_sensor_with_id(self, sensor_id) -> Sensor:
        for sensor in self.sensors:
            if sensor.get_id() == sensor_id:
                return sensor
        raise ValueError("Sensor not found")


class Token:
    def __init__(self, case, sensor, last_timestamp):
        self.case = case
        self.sensor_id = sensor
        self.last_timestamp = last_timestamp

    def set_sensor(self, sensor_id):
        self.sensor_id = sensor_id

    def add_to_last_timestamp(self, duration):
        self.last_timestamp += timedelta(minutes=duration)
