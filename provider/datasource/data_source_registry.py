from typing import List

from core.datasource import GenericDataSource
from core.datasource_id import DataSourceId
from provider.activity.eventselection.event_selection_provider_registry import EventSelectionProviderRegistry
from provider.sink.sink_provider import SinkProvider
from provider.sink.sink_provider_registry import SinkProviderRegistry


class DataSourceRegistry:

    def get_sink(self, definition, sensor_id, default_sink):
        if "sink" not in definition:
            return default_sink.get_sender(sensor_id)
        return SinkProviderRegistry().get(config=definition["sink"]).get_sender(sensor_id)

    def get(self, data_source_definitions: List[str], default_sink: SinkProvider):
        data_sources = []
        for definition in data_source_definitions:
            sensor_id = definition["name"]
            data_sources.append(
                GenericDataSource(
                    sensor_id=DataSourceId(sensor_id),
                    group_id=definition.get("groupId", "default group"),
                    event_provider=EventSelectionProviderRegistry().get(config=definition["eventGeneration"]),
                    sender=self.get_sink(definition, sensor_id, default_sink)
                )
            )
        return data_sources
