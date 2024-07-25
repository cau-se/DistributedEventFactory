from provider.activity.generation.activity_generation_provider import ActivityGenerationProvider, \
    DistinctActivityGenerationProvider, ListBasedActivityGenerationProvider
from provider.generic.count_provider_registry import CountProviderRegistry

class ActivityGenerationProviderRegistry:
    def __init__(self):
        self.count_provider_registry = CountProviderRegistry()

    def get(self, config) -> ActivityGenerationProvider:
        registry = dict()
        registry["distinct"] = lambda config: DistinctActivityGenerationProvider(
            number_of_activities_provider=self.count_provider_registry.get(config["count"]))
        registry["list"] = lambda config: ListBasedActivityGenerationProvider(sensor_id_activity_map=config["values"])
        return registry[config["type"]](config)