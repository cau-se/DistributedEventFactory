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
    sensor_name: str
    status: str
    debug: str


class OutlierCategory:
    GLOBAL_OUTLIERS = "GLOBAL_OUTLIERS"
    CONTEXTUAL_OUTLIERS = "CONTEXTUAL_OUTLIERS"
    COLLECTIVE_OUTLIERS = "COLLECTIVE_OUTLIERS"
