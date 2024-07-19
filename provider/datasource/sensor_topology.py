import abc
from typing import List

from core.datasource import DataSource, GenericDataSource, StartDataSource, EndDataSource
from core.datasource_id import START_SENSOR_ID, END_SENSOR_ID
from provider.activity.activity_emission_provider import ActivityEmissionProviderFactory, \
    UniformActivityEmissionProviderFactory

from provider.activity.activity_generation_provider import DistinctActivityGenerationProvider
from provider.datasource.datasource_id_provider import DataSourceIdProvider, DataSourceIdProviderRegistry
from provider.generic.count_provider import StaticCountProvider
from provider.sender.send_provider import SendProvider, SinkProviderRegistry
from provider.transition.duration_provider import DurationProvider, DurationProviderRegistry
from provider.transition.transition_provider_factory import MatrixBasedTransitionProvider, TransitionProviderRegistry


class SensorTopologyProvider:
    @abc.abstractmethod
    def get_sensors(self, number_of_sensors) -> List[DataSource]:
        pass


class SensorTopologyProviderRegistry:

    def __init__(self):
        self.dataSourceIdProviderRegistry = DataSourceIdProviderRegistry()
        self.sinkProviderRegistry = SinkProviderRegistry()
        self.transitionProviderRegistry = TransitionProviderRegistry()
        self.durationProviderRegistry = DurationProviderRegistry()

    def get(self, type: str, args) -> SensorTopologyProvider:
        registry = dict()
        registry["classic"] = lambda config: GenericSensorTopologyProvider(
            data_source_id_provider=self.dataSourceIdProviderRegistry.get(config["dataSources"]["type"],
                                                                          config["dataSources"]["args"]),
            transition_provider_factory=self.transitionProviderRegistry.get(config["transitions"]["type"],
                                                                            config["transitions"]["args"]),
            duration_provider=self.durationProviderRegistry.get(config["duration"]["type"], config["duration"]["args"]),
            send_provider=self.sinkProviderRegistry.get(config["sink"]["type"]),
            activity_emission_provider=
            UniformActivityEmissionProviderFactory(
                potential_activities_provider=
                # ListBasedActivityGenerationProvider(
                #    sensor_id_activity_map=[
                #        ["1", "2", "3"],
                #        ["4", "5", "6"],
                #        ["7", "8", "9"],
                #        ["10", "11", "12"],
                #        ["13", "14", "15"],
                #        ["13", "14", "15"],
                #        ["16", "17", "18"],
                #        ["19"],
                #        ["20", "21"],
                #        ["25"],
                #        ["26", "27", "28"],
                #    ]
                # )
                DistinctActivityGenerationProvider(
                    number_of_activities_provider=StaticCountProvider(5)
                )
            )
        )
        return registry[type](args)


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
        sensors.append(StartDataSource(transition_provider=self.transition_provider.get(number_of_sensors + 1),
                                       sender=self.send_provider.get_sender(START_SENSOR_ID.get_name())))
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
