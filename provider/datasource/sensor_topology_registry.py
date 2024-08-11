from provider.datasource.data_source_registry import DataSourceRegistry
from provider.datasource.sensor_topology import DataSourceTopologyProvider, ConcreteDataSourceTopologyProvider


class DataSourceProviderRegistry:

    def get(self, config) -> DataSourceTopologyProvider:
        registry = dict()

        registry["concrete"] = lambda config: ConcreteDataSourceTopologyProvider(
            data_source_list=DataSourceRegistry().get(data_source_definitions=config["dataSources"])
        )
        return registry["concrete"](config)

