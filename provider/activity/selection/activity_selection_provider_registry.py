from provider.activity.generation.activity_generation_registry import ActivityGenerationProviderRegistry
from provider.activity.selection.ordered.ordered_selection_provider import OrderedActivitySelectionProviderFactory
from provider.activity.selection.uniform.uniform_selction_provider import UniformActivitySelectionProviderFactory


class ActivitySelectionProviderRegistry:
    def get(self, config) -> UniformActivitySelectionProviderFactory:
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
        return registry[config["selection"]](config)
