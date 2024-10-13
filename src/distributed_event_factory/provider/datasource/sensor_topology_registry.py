from src.distributed_event_factory.provider.datasource.data_source_registry import DataSourceRegistry
from src.distributed_event_factory.provider.datasource.sensor_topology import DataSourceTopologyProvider, \
    ConcreteDataSourceTopologyProvider
from src.distributed_event_factory.provider.sink.sink_provider_registry import SinkProviderRegistry

class DataSourceProviderRegistry:

    def get(self, config) -> DataSourceTopologyProvider:
        registry = dict()

        registry["concrete"] = lambda config: ConcreteDataSourceTopologyProvider(
            data_source_list=DataSourceRegistry().get(
                data_source_definitions=config["dataSources"],
                default_sink=SinkProviderRegistry().get(config=config["defaultSink"])
            )
        )
        return registry["concrete"](config)
