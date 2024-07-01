import random
import time
from datetime import datetime, timedelta
from typing import List

from scheduled_futures import ScheduledThreadPoolExecutor

from core.sensor import Sensor, GenericSensor
from core.sensor_id import SensorId, END_SENSOR, START_SENSOR

from provider.data.case_provider import CaseIdProvider, IncreasingCaseIdProvider
from provider.generic.count_provider import StaticCountProvider, CountProvider
from provider.load.load_provider import LoadProvider, GradualIncreasingLoadProvider
from provider.sensor.sensor_topology import SensorTopologyProvider, GenericSensorTopologyProvider
from provider.transition.duration_provider import DurationProvider, GaussianDurationProvider
from provider.transition.next_state_provider import NextStateProvider, DistinctNextStateProvider
from provider.transition.transition_probability_provider import TransitionProbabilityProvider, \
    DrawWithoutReplacementTransitionProvider
from provider.transition.transition_provider import GenericTransitionProvider
from utils.utils_types import GeneratedEvent


class ProcessSimulator:
    def __init__(self, sensors, case_id_provider: CaseIdProvider):
        self.tokens: List[Token] = []
        self.sensors: List[Sensor] = sensors
        self.case_id_provider = case_id_provider
        self.last_time = datetime.now()
        self.tick = 0

    def simulate(self) -> GeneratedEvent:
        if not self.tokens:
            case_id = self.case_id_provider.get()
            self.tokens.append(Token(case_id, START_SENSOR, self.last_time))

        token = self.tokens[int(random.uniform(0, len(self.tokens)))]

        current_sensor = self._get_sensor_with_id(token.sensor_id)

        duration, next_sensor = current_sensor.get_sensor_transition()
        token.add_to_last_timestamp(duration=duration)
        last_timestamp = token.last_timestamp
        gen_event = current_sensor.emit_event(token.case, last_timestamp)
        self.last_time = last_timestamp

        if next_sensor.get_name() == END_SENSOR.get_name():
            self.tokens.remove(token)
            print("----------END----------------")
        else:
            token.set_sensor(next_sensor)

        return gen_event

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