from typing import List

from core.datasource import GenericDataSource
from core.datasource_id import DataSourceId
from provider.activity.selection.activity_selection_provider_registry import ActivitySelectionProviderRegistry
from provider.sink.sink_provider_registry import SinkProviderRegistry
from provider.transition.duration.duration_registry import DurationProviderRegistry
from provider.transition.next_sensor_provider import NextSensorProvider


class DataSourceRegistry:
    def get(self, data_source_definitions: List[str]):
        data_sources = []
        for definition in data_source_definitions:
            sensor_id = definition["name"]
            data_sources.append(
                GenericDataSource(
                    sensor_id=DataSourceId(sensor_id),
                    duration_provider=DurationProviderRegistry().get(config=definition["duration"]),
                    transition_provider=NextSensorProvider(definition["transition"]),
                    activity_emission_provider=ActivitySelectionProviderRegistry()
                    .get(config=definition["activities"])
                    .get_activity_provider(),
                    sender=SinkProviderRegistry().get(config=definition["sink"]).get_sender(sensor_id)
                )
            )
        return data_sources