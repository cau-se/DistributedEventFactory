from typing import List

from src.distributed_event_factory.provider.event.event_provider import EventDataProvider
from src.distributed_event_factory.provider.event.event_provider_registry import EventProviderRegistry
from src.distributed_event_factory.provider.eventselection.event_selection_provider import EventSelectionProvider
from src.distributed_event_factory.provider.eventselection.generic_probability_event_selection_provider import \
    GenericProbabilityEventSelectionProvider
from src.distributed_event_factory.provider.eventselection.ordered_selection_provider import \
    OrderedEventSelectionProvider
from src.distributed_event_factory.provider.eventselection.uniform_selction_provider import \
    UniformEventSelectionProvider


class EventSelectionProviderRegistry:

    def _transform_list(self, config):
        event_providers: List[EventDataProvider] = []
        events = config["events"]
        for event in events:
            event_providers.append(EventProviderRegistry().get(event))
        return event_providers

    def get(self, config) -> EventSelectionProvider:
        registry = dict()
        registry["uniform"] = lambda config: (
                UniformEventSelectionProvider(
                    potential_events=self._transform_list(config["from"])
                )
            )
        registry["ordered"] = lambda config: (
            OrderedEventSelectionProvider(
                potential_events=self._transform_list(config["from"])
            )
        )
        registry["genericProbability"] = lambda config: (
            GenericProbabilityEventSelectionProvider(
                probability_distribution=config["distribution"],
                potential_events=self._transform_list(config["from"])
            )
        )
        return registry[config["selection"]](config)
