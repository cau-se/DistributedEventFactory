import abc
from string import ascii_uppercase as alphabet
from typing import List

from provider.generic.count_provider import CountProvider, CountProviderRegistry


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


class ActivityGenerationProviderRegistry:
    def __init__(self):
        self.count_provider_registry = CountProviderRegistry()

    def get(self, type: str, args) -> ActivityGenerationProvider:
        registry = dict()
        registry["distinct"] = lambda config: DistinctActivityGenerationProvider(
            number_of_activities_provider=self.count_provider_registry.get(config["count"]["type"], config["count"]["args"]))
        registry["list"] = lambda config: ListBasedActivityGenerationProvider(sensor_id_activity_map=config["values"])
        return registry[type](args)
