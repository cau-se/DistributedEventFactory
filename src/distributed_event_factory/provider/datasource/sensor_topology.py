from abc import abstractmethod
from typing import List

from distributed_event_factory.core.datasource import DataSource, StartDataSource, EndDataSource
from distributed_event_factory.core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID
from distributed_event_factory.provider.sink.console.console_sink import PrintConsoleSinkProvider
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
        data_sources.append(
            StartDataSource(
                transition_provider=ChoiceTransitionProvider(transitions),
                sender=PrintConsoleSinkProvider().get_sender(START_SENSOR_ID.get_name())))
        for data_source in self.data_source_list:
            data_sources.append(data_source)

        data_sources.append(EndDataSource(sender=PrintConsoleSinkProvider().get_sender(END_DATA_SOURCE_ID.get_name())))
        return data_sources
