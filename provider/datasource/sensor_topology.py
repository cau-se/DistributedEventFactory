from abc import ABC, abstractmethod
from typing import List

from core.datasource import DataSource, GenericDataSource, StartDataSource, EndDataSource
from core.datasource_id import START_SENSOR_ID, END_DATA_SOURCE_ID
from provider.activity.selection.activity_selection_provider import ActivitySelectionProviderFactory
from provider.datasource.datasource_id_provider import DataSourceIdProvider
from provider.sink.console.console_sink import PrintConsoleSinkProvider
from provider.sink.sink_provider import SinkProvider
from provider.transition.duration.duration_provider import DurationProvider
from provider.transition.next_sensor_provider import NextSensorProvider
from provider.transition.transition_provider_factory import MatrixBasedTransitionProvider


class DataSourceTopologyProvider:
    @abstractmethod
    def get_sensor_topology(self, number_of_sensors) -> List[DataSource]:
        pass


class GenericDataSourceTopologyProvider(DataSourceTopologyProvider):
    def __init__(
            self,
            data_source_provider,
            transition_provider_factory,
            send_provider,
    ):
        self.transition_provider: MatrixBasedTransitionProvider = transition_provider_factory
        self.send_provider: SinkProvider = send_provider
        self.data_source_provider: DataSourceProvider = data_source_provider

    def get_sensor_topology(self, number_of_sensors):
        sensors: List[DataSource] = []
        sensors.append(StartDataSource(transition_provider=self.transition_provider.get(number_of_sensors + 1),
                                       sender=self.send_provider.get_sender(START_SENSOR_ID.get_name())))
        for i in range(number_of_sensors):
            sensors.append(self.data_source_provider.get_data_source(number_of_sensors))
        sensors.append(EndDataSource(sender=self.send_provider.get_sender(END_DATA_SOURCE_ID.get_name())))
        return sensors


class ConcreteDataSourceTopologyProvider(DataSourceTopologyProvider):
    def __init__(self, data_source_list: List[DataSource]):
        self.data_source_list = data_source_list

    def get_sensor_topology(self, number_of_sensors):
        data_sources = []
        transitions = [0.0] * number_of_sensors
        transitions[0] = 1.0
        data_sources.append(
            StartDataSource(
                transition_provider=NextSensorProvider(transitions),
                sender=PrintConsoleSinkProvider().get_sender(START_SENSOR_ID.get_name())))
        for data_source in self.data_source_list:
            data_sources.append(data_source)

        data_sources.append(EndDataSource(sender=PrintConsoleSinkProvider().get_sender(END_DATA_SOURCE_ID.get_name())))
        return data_sources


class DataSourceProvider(ABC):
    @abstractmethod
    def get_data_source(self, number_of_sensors):
        pass


class GenericDataSourceProvider(DataSourceProvider):

    def __init__(
            self,
            data_source_id_provider,
            transition_provider_factory,
            duration_provider,
            send_provider,
            activity_emission_provider
    ):
        self.data_source_id_provider: DataSourceIdProvider = data_source_id_provider
        self.transition_provider: MatrixBasedTransitionProvider = transition_provider_factory
        self.duration_provider: DurationProvider = duration_provider
        self.send_provider: SinkProvider = send_provider
        self.activity_emission_provider: ActivitySelectionProviderFactory = activity_emission_provider

    def get_data_source(self, number_of_sensors):
        sensor_id = self.data_source_id_provider.get_id()
        return GenericDataSource(
            sender=self.send_provider.get_sender(sensor_id.get_name()),
            sensor_id=sensor_id,
            transition_provider=self.transition_provider.get(number_of_sensors + 1),
            duration_provider=self.duration_provider,
            activity_emission_provider=self.activity_emission_provider.get_activity_provider()
        )

