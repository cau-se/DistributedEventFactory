import random
from datetime import datetime, timedelta
from typing import List
from dataclasses import dataclass

from utils.utils_types import SensorLog, OutlierCategory


def integrate_outliers(sensor_logs: List[SensorLog], outlier_type: str, percentage: float) -> List[SensorLog]:
    """
    Integrate outliers into the SensorLog list based on the given outlier type and percentage.
    """
    outlier_logs = []
    case_ids: set[str] = set(log.case_id for log in sensor_logs)

    for case_id in case_ids:
        case_logs: list[SensorLog] = list(filter(lambda l: l.case_id == case_id, sensor_logs))
        num_outliers: int = int(len(case_logs) * percentage)

        if outlier_type == OutlierCategory.POINT_OUTLIER:
            outlier_logs.extend(generate_point_outliers(case_logs, num_outliers))
        elif outlier_type == OutlierCategory.CONTEXTUAL_OUTLIERS:
            outlier_logs.extend(generate_contextual_outliers(case_logs, num_outliers))
        elif outlier_type == OutlierCategory.SUBSEQUENCE_OUTLIERS:
            outlier_logs.extend(generate_subsequence_outliers(case_logs, num_outliers))

    integrated_logs = sensor_logs + outlier_logs
    return integrated_logs


def generate_point_outliers(case_logs: List[SensorLog], num_outliers: int) -> List[SensorLog]:
    """
    Generate Point Outliers by randomly selecting data points and modifying their values.
    """
    outlier_logs = []

    for _ in range(num_outliers):
        log = random.choice(case_logs)
        outlier_log = SensorLog(
            timestamp=log.timestamp,
            sensor_value=generate_outlier_value(log.sensor_value),
            case_id=log.case_id,
            sensor_name=log.sensor_name,
            status=log.status,
            generated_by=log.generated_by
        )
        outlier_logs.append(outlier_log)

    return outlier_logs


def generate_contextual_outliers(case_logs: List[SensorLog], num_outliers: int) -> List[SensorLog]:
    """
    Generate Contextual Outliers by modifying the values based on the surrounding data points.
    """
    outlier_logs = []

    for _ in range(num_outliers):
        log = random.choice(case_logs)
        previous_log = case_logs[case_logs.index(log) - 1]
        next_log = case_logs[case_logs.index(log) + 1]

        outlier_log = SensorLog(
            timestamp=log.timestamp,
            sensor_value=(previous_log.sensor_value + next_log.sensor_value) / 2,
            case_id=log.case_id,
            sensor_name=log.sensor_name,
            status=log.status,
            generated_by=log.generated_by
        )
        outlier_logs.append(outlier_log)

    return outlier_logs


def generate_subsequence_outliers(case_logs: List[SensorLog], num_outliers: int) -> List[SensorLog]:
    """
    Generate Subsequence as an Outlier by randomly selecting subsequences and modifying their values.
    """
    outlier_logs = []

    for _ in range(num_outliers):
        subsequence_length = random.randint(2, len(case_logs))
        start_index = random.randint(0, len(case_logs) - subsequence_length)
        subsequence = case_logs[start_index : start_index + subsequence_length]

        outlier_subsequence = []
        for log in subsequence:
            outlier_log = SensorLog(
                timestamp=log.timestamp,
                sensor_value=generate_outlier_value(log.sensor_value),
                case_id=log.case_id,
                sensor_name=log.sensor_name,
                status=log.status,
                generated_by=log.generated_by,
            )
            outlier_subsequence.append(outlier_log)

        outlier_logs.extend(outlier_subsequence)

    return outlier_logs


def generate_outlier_value(original_value: str) -> any:
    """
    Generate an outlier value by randomly modifying the original value.
    """
    deviation = random.uniform(0.1, 0.5)  # Adjust the range based on the desired deviation
    is_additive = random.choice([True, False])  # Randomly decide whether to add or subtract

    if is_additive:
        outlier_value = original_value + (original_value * deviation)
    else:
        outlier_value = original_value - (original_value * deviation)

    return outlier_value