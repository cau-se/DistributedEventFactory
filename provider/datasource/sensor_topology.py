import abc
from typing import List

from core.datasource import DataSource, GenericDataSource, StartDataSource, EndDataSource
from core.datasource_id import DataSourceId, START_SENSOR_ID, END_SENSOR_ID
from provider.activity.activity_emission_provider import ActivityEmissionProviderFactory
from provider.datasource.datasource_id_provider import DataSourceIdProvider
from provider.sender.send_provider import SendProvider
from provider.transition.duration_provider import DurationProvider
from provider.transition.transition_provider_factory import MatrixBasedTransitionProvider


class SensorTopologyProvider:
    @abc.abstractmethod
    def get_sensors(self, number_of_sensors) -> List[DataSource]:
        pass


class GenericSensorTopologyProvider(SensorTopologyProvider):

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
        self.send_provider: SendProvider = send_provider
        self.activity_emission_provider: ActivityEmissionProviderFactory = activity_emission_provider

    def get_sensors(self, number_of_sensors):
        sensors: List[DataSource] = []
        sensors.append(StartDataSource(transition_provider=self.transition_provider.get(number_of_sensors + 1), sender=self.send_provider.get_sender(START_SENSOR_ID.get_name())))
        for i in range(number_of_sensors):
            sensor_id = self.data_source_id_provider.get_id()
            sensors.append(
                GenericDataSource(
                    sensor_id=sensor_id,
                    transition_provider=self.transition_provider.get(number_of_sensors + 1),
                    duration_provider=self.duration_provider,
                    sender=self.send_provider.get_sender(sensor_id.get_name()),
                    activity_emission_provider=self.activity_emission_provider.get_activity_provider()
                )
            )
        sensors.append(EndDataSource(sender=self.send_provider.get_sender(END_SENSOR_ID.get_name())))
        return sensors
