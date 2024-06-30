import random
import time
from datetime import datetime, timedelta
from typing import List
from core.sensor import Sensor, GenericSensor
from core.util import SensorId, END_SENSOR, START_SENSOR

from provider.data.case_provider import CaseIdProvider, IncreasingCaseIdProvider
from provider.generic.count_provider import StaticCountProvider
from provider.transition.duration_provider import DurationProvider, GaussianDurationProvider
from provider.transition.next_state_provider import NextStateProvider, DistinctNextStateProvider
from provider.transition.transition_probability_provider import TransitionProbabilityProvider, \
    DrawWithoutReplacementTransitionProvider
from provider.transition.transition_provider_new import GenericTransitionProvider
from utils.utils_types import GeneratedEvent


class SensorTopologyBuilder:

    def __init__(self, next_state_provider, transition_probability_provider, transition_count_provider, duration_provider):
        self.next_state_provider: NextStateProvider = next_state_provider
        self.transition_probability_provider: TransitionProbabilityProvider = transition_probability_provider
        self.transition_count_provider = transition_count_provider
        self.duration_provider: DurationProvider = duration_provider


    def get_sensors(self, number_of_sensors):
        sensor_ids: List[SensorId] = []
        for i in range(number_of_sensors):
            sensor_ids.append(SensorId(str(i)))
        sensor_ids.append(START_SENSOR)
        sensor_ids.append(END_SENSOR)

        sensors: List[Sensor] = []
        for sensor_id in sensor_ids:
            number_of_next_states = self.transition_count_provider.get()
            sensor_ids_for_transition = self._get_sensor_ids_without_start(sensor_ids)
            new_sensor = GenericSensor(
                sensor_id=sensor_id,
                transition_provider_new=GenericTransitionProvider(
                    next_sensors=self.next_state_provider.get_next_states(sensor_ids_for_transition, number_of_next_states=number_of_next_states),
                    next_sensor_probabilities=self.transition_probability_provider.get_transition_probabilities(number_of_next_states)
                ),
                duration_provider=self.duration_provider
            )
            sensors.append(new_sensor)
        return sensors

    def _get_sensor_ids_without_start(self, sensor_ids):
        # TODO here: Mit richtiger equals methode lösen
        valid_sensor_ids = []
        for sensor_id in sensor_ids:
            if sensor_id.get_id() != START_SENSOR.get_id():
                valid_sensor_ids.append(sensor_id)
        return valid_sensor_ids


class ProcessSimulator:
    def __init__(self, sensors, case_id_provider: CaseIdProvider):
        self.tokens: List[Token] = []
        self.sensors: List[Sensor] = sensors
        self.case_id_provider = case_id_provider
        self.tick = 0

    def simulate(self) -> GeneratedEvent:
        if not self.tokens:
            case_id = self.case_id_provider.get()
            # TODO here the datetime will be a problem.
            # We must track the whole last event to have a progressing time scope
            self.tokens.append(Token(case_id, START_SENSOR, datetime.now()))

        token = self.tokens[int(random.uniform(0, len(self.tokens)))]

        current_sensor = self._get_sensor_with_id(token.sensor_id)

        duration, next_sensor = current_sensor.get_sensor_transition()
        token.add_to_last_timestamp(duration=duration)
        gen_event = current_sensor.emit_event(token.case, token.last_timestamp)

        if next_sensor.get_id() == END_SENSOR.get_id():
            self.tokens.remove(token)
            return None
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


if __name__ == '__main__':
    sensors: List[Sensor] = SensorTopologyBuilder(
        next_state_provider=DistinctNextStateProvider(),
        transition_probability_provider=DrawWithoutReplacementTransitionProvider(),
        transition_count_provider=StaticCountProvider(count=3),
        duration_provider=GaussianDurationProvider(mu=10, sigma=1)
    ).get_sensors(20)

    process_simulator = ProcessSimulator(
        sensors=sensors,
        case_id_provider=IncreasingCaseIdProvider()
    )
    for i in range(1000):
        print(process_simulator.simulate())

    for sensor in sensors:
        print(sensor.get_id().get_id())
        for event in sensor.get_event_log():
            print(event)
