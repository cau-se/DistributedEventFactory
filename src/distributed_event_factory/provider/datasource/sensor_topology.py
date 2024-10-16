from abc import abstractmethod
from typing import List

from distributed_event_factory.core.datasource import DataSource
from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.core.start_datasource import StartDataSource
from distributed_event_factory.provider.transition.transition.transition_provider import ChoiceTransitionProvider


class DataSourceTopologyProvider:
    @abstractmethod
    def get_sensor_topology(self, number_of_sensors) -> List[DataSource]:
        pass


class ConcreteDataSourceTopologyProvider(DataSourceTopologyProvider):
    def __init__(self, data_source_list: List[DataSource]):
        self.data_source_list = data_source_list

    def get_sensor_topology(self, number_of_sensors):
        data_sources = []
        transitions = [0.0] * number_of_sensors
        transitions[0] = 1.0
        data_sources.append(StartDataSource(transition_provider=ChoiceTransitionProvider(transitions)))
        for data_source in self.data_source_list:
            data_sources.append(data_source)

        data_sources.append(EndDataSource())
        return data_sources
