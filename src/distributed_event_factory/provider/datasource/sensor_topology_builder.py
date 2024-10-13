from typing import List

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.provider.datasource.sensor_topology import ConcreteDataSourceTopologyProvider

class SensorTopologyBuilder:

    def __init__(self):
        self.datasources: List[DataSource] = []

    def add_datasource(self, datasource: DataSource):
        self.datasources.append(datasource)

    def build(self):
        return ConcreteDataSourceTopologyProvider(data_source_list=self.datasources)