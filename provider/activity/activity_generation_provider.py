import abc
from string import ascii_uppercase as alphabet
from typing import List


class ActivityGenerationProvider(abc.ABC):

    @abc.abstractmethod
    def get_activities(self, number_of_activities):
        pass


class DistinctActivityGenerationProvider(ActivityGenerationProvider):
    def __init__(self):
        self.activity_names = self.generate_activity_names()

    def generate_activity_names(self):
        potential_sensor_names = []
        for char in alphabet:
            for char2 in alphabet:
                potential_sensor_names.append("Event " + char + char2)
        return iter(potential_sensor_names)

    def get_activities(self, number_of_activities):
        activities: List[str] = []
        for i in range(number_of_activities):
            activities.append(next(self.activity_names))
        return activities
