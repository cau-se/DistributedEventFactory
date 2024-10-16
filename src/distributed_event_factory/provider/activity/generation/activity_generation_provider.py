import abc
from string import ascii_uppercase as alphabet
from typing import List

class ActivityGenerationProvider(abc.ABC):

    @abc.abstractmethod
    def get_activities(self):
        pass


class DistinctActivityGenerationProvider(ActivityGenerationProvider):
    def __init__(self, number_of_activities_provider: CountProvider):
        self.activity_names = self.generate_activity_names()
        self.number_of_activities = number_of_activities_provider.get()

    def generate_activity_names(self):
        potential_sensor_names = []
        for char in alphabet:
            for char2 in alphabet:
                potential_sensor_names.append("Event " + char + char2)
        return iter(potential_sensor_names)

    def get_activities(self):
        activities: List[str] = []
        for i in range(self.number_of_activities):
            activities.append(next(self.activity_names))
        return activities


class ListBasedActivityGenerationProvider(ActivityGenerationProvider):

    def __init__(self, sensor_id_activity_map: List[List[str]]):
        self.sensor_id_activity_map = sensor_id_activity_map
        self.activity_iterator = iter(sensor_id_activity_map)

    def get_activities(self):
        activities = next(self.activity_iterator)
        if not activities:
            return []
        return activities


