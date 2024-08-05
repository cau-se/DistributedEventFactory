from typing import List

from core.datasource import DataSource, GenericDataSource
from provider.activity.selection.activity_selection_provider_registry import ActivitySelectionProviderRegistry
from provider.datasource.data_source_registry import DataSourceRegistry
from provider.datasource.sensor_topology import DataSourceTopologyProvider, ConcreteDataSourceTopologyProvider
from provider.sink.sink_provider_registry import SinkProviderRegistry
from provider.transition.duration.duration_registry import DurationProviderRegistry
from provider.transition.nextsensor.next_sensor_provider import NextSensorProvider


class DataSourceProviderRegistry:

    def get(self, config) -> DataSourceTopologyProvider:
        registry = dict()

        registry["concrete"] = lambda config: ConcreteDataSourceTopologyProvider(
            data_source_list=DataSourceRegistry().get(data_source_definitions=config["dataSources"])
        )
        return registry["concrete"](config)

