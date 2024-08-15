from provider.activity.generation.activity_generation_registry import ActivityGenerationProviderRegistry
from provider.activity.selection.activity_selection_provider import ActivitySelectionProviderFactory
from provider.activity.selection.ordered.ordered_selection_provider import OrderedActivitySelectionProviderFactory
from provider.activity.selection.single.single_selection_provider import SingleActivitySelectionProviderFactory
from provider.activity.selection.uniform.uniform_selection_provider import UniformActivitySelectionProviderFactory


class ActivitySelectionProviderRegistry:
    def get(self, config) -> ActivitySelectionProviderFactory:
        registry = dict()
        registry["uniform"] = lambda config: (
            UniformActivitySelectionProviderFactory(
                potential_activities_provider=ActivityGenerationProviderRegistry().get(config["from"])
            )
        )
        registry["ordered"] = lambda config: (
            OrderedActivitySelectionProviderFactory(
                potential_activities_provider=ActivityGenerationProviderRegistry().get(config["from"])
            )
        )
        if "selection" not in config:
            return SingleActivitySelectionProviderFactory(config)

        return registry[config["selection"]](config)
