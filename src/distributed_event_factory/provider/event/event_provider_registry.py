from distributed_event_factory.provider.activity.selection.activity_selection_provider_registry import \
    ActivitySelectionProviderRegistry
from distributed_event_factory.provider.event.event_provider import EventDataProvider, CustomEventDataProvider
from distributed_event_factory.provider.transition.duration.duration_registry import DurationProviderRegistry
from distributed_event_factory.provider.transition.transition.next_sensor_provider_registry import \
    NextSensorProviderRegistry


class EventProviderRegistry:

    def get(self, config) -> EventDataProvider:
        registry = dict()
        registry["classic"] = lambda config: (
            CustomEventDataProvider(
                duration_provider=DurationProviderRegistry().get(config=config["duration"]),
                transition_provider=NextSensorProviderRegistry().get(config["transition"]),
                activity_provider=ActivitySelectionProviderRegistry()
                .get(config=config["activity"])
                .get_activity_provider(),
            ))

        return registry["classic"](config)
