from typing import List

from provider.transition.transition_provider_new import TransitionProviderNew
from core.util import SensorId
from utils.utils_types import GeneratedEvent


class Sensor:

    def emit_event(self, case, timestamp) -> str:
        pass

    def get_sensor_transition(self) -> tuple[int, SensorId]:
        pass

    def get_id(self) -> SensorId:
        pass

    def get_event_log(self) -> List[str]:
        pass


class GenericSensor(Sensor):
    def __init__(
            self,
            sensor_id: SensorId,
            transition_provider_new,
            duration_provider
    ):
        self.sensor_id: SensorId = sensor_id
        self.transition_provider_new: TransitionProviderNew = transition_provider_new
        self.duration_provider = duration_provider
        self.event_log = []

    def get_id(self) -> SensorId:
        return self.sensor_id

    def emit_event(self, case, timestamp):
        event_name = "Event " + self.sensor_id.id
        event = GeneratedEvent(
            timestamp=timestamp,
            sensor_value=event_name,
            case_id=case,
            sensor_name=self.sensor_id.get_id(),
            status="Status",
            generated_by="GenBy"
        )

        self.event_log.append(event)
        return event

    def get_sensor_transition(self):
        next_sensor = self.transition_provider_new.get_next_sensor()
        duration = self.duration_provider.get_duration()
        return duration, next_sensor

    def get_event_log(self):
        return self.event_log


