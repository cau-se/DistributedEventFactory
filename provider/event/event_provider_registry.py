from provider.activity.selection.activity_selection_provider_registry import ActivitySelectionProviderRegistry
from provider.event.event_provider import EventDataProvider, CustomEventDataProvider
from provider.transition.duration.duration_registry import DurationProviderRegistry
from provider.transition.nextsensor.next_sensor_provider_registry import NextSensorProviderRegistry


class EventProviderRegistry:

    def get(self, config) -> EventDataProvider:
        registry = dict()
        registry["classic"] = lambda config: (
            CustomEventDataProvider(
                duration_provider=DurationProviderRegistry().get(config=config["duration"]),
                transition_provider=NextSensorProviderRegistry().get(config["transition"]),
                activity_provider=ActivitySelectionProviderRegistry()
                .get(config=config["activities"])
                .get_activity_provider(),
            ))

        return registry["classic"](config)
