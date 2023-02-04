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
    generated_by: str


class OutlierCategory:
    GLOBAL_OUTLIERS = "GLOBAL_OUTLIERS"
    CONTEXTUAL_OUTLIERS = "CONTEXTUAL_OUTLIERS"
    COLLECTIVE_OUTLIERS = "COLLECTIVE_OUTLIERS"


class BgColors:
    HEADER: str = '\033[95m'
    OKBLUE: str = '\033[94m'
    OKCYAN: str = '\033[96m'
    OKGREEN: str = '\033[92m'
    WARNING: str = '\033[93m'
    FAIL: str = '\033[91m'
    ENDC: str = '\033[0m'
    BOLD: str = '\033[1m'
    UNDERLINE: str = '\033[4m'


def print_color(message: str, color: str, end=None) -> None:
    if end is not None:
        print(f"{color}{message}{BgColors.ENDC}", end=end)
    else:
        print(f"{color}{message}{BgColors.ENDC}")
