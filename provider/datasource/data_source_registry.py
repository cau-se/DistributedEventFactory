from typing import List

from core.datasource import GenericDataSource
from core.datasource_id import DataSourceId
from provider.activity.eventselection.event_selection_provider_registry import EventSelectionProviderRegistry
from provider.sink.sink_provider_registry import SinkProviderRegistry


class DataSourceRegistry:
    def get(self, data_source_definitions: List[str]):
        data_sources = []
        for definition in data_source_definitions:
            sensor_id = definition["name"]
            data_sources.append(
                GenericDataSource(
                    sensor_id=DataSourceId(sensor_id),
                    event_provider=EventSelectionProviderRegistry().get(config=definition["eventGeneration"]),
                    sender=SinkProviderRegistry().get(config=definition["sink"]).get_sender(sensor_id)
                )
            )
        return data_sources
