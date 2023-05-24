import copy
import random as rd
from typing import List

from utils.utils_types import SensorLog, fisher_yates_shuffle


def add_noise(lst: List[SensorLog], frequency: float, change_value: float):
    """
    Adds noise to a list of SensorLog.

    :param
        lst (list): A list of SensorLog.
        frequency (float): The percentage of elements to add noise to.
        change_value (float): a possibility that the SensorValue is changed

    Returns:
        list: The modified list with added noise.

    """
    num_noise_elements: int = int(len(lst) * frequency)

    indices: List[int] = rd.sample(range(len(lst)), num_noise_elements)

    # Copy and insert the selected elements after their original position
    for j in sorted(indices, reverse=True):
        lst[j].status = "NOISE"
        if rd.random() >= change_value:
            selected = lst[j].sensor_value
            sensor_value_list = fisher_yates_shuffle(list(selected), int((len(selected) / 2) - 1),
                                                     int(len(selected) - 1))
            new_sensor_value = ''.join(sensor_value_list)
            lst[j].sensor_value = new_sensor_value
            lst[j].status = "NOISE_WITH_VALUE_ERROR"

        lst.insert(j + 1, copy.deepcopy(lst[j]))
    return lst


sl = []
for i in range(10):
    s = SensorLog(case_id="", sensor_name="", sensor_value=f"SensorValue {i}", status="Valid", timestamp="",
                  generated_by="")
    sl.append(s)

for n in add_noise(sl, 0.5, 0.5):
    print(n)
