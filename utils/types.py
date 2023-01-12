import datetime
from dataclasses import dataclass


@dataclass
class SensorLog:
    """
    A data class representing the type for a sensor log
    """

    timestamp: datetime.datetime
    sensor_value: any
    case_id: str
    sensor_type: str
    status: str