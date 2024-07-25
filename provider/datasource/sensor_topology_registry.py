from typing import List

from core.datasource import DataSource, GenericDataSource
from provider.activity.activity_emission_provider import ActivityEmissionProviderRegistry
from provider.datasource.data_source_registry import DataSourceRegistry
from provider.datasource.datasource_id_provider import DataSourceIdProviderRegistry
from provider.datasource.sensor_topology import SensorTopologyProvider, GenericSensorTopologyProvider, \
    ConcreteSensorTopologyProvider
from provider.sink.send_provider import SinkProviderRegistry
from provider.transition.duration_provider import DurationProviderRegistry
from provider.transition.next_sensor_provider import NextSensorProvider
from provider.transition.transition_provider_factory import TransitionProviderRegistry


class DataSourceConverter:
    def convert(self, data_source_definition) -> List[DataSource]:
        # TODO here integrate number of sensors
        number_of_sensors = len(data_source_definition)

        data_sources = []
        for definition in data_source_definition:
            sensor_id = data_source_definition.name
            data_sources.append(
                GenericDataSource(
                    sensor_id=sensor_id,
                    duration_provider=DurationProviderRegistry()
                        .get(config=DurationProviderRegistry()
                            .get(config=definition.duration)
                        ),
                    transition_provider=NextSensorProvider(definition.transition),
                    activity_emission_provider=ActivityEmissionProviderRegistry()
                        .get(config=definition.activities)
                    .get_activity_provider(),
                    sender=SinkProviderRegistry().get(config=definition.sink).get_sender(sensor_id),
                )
            )

        return data_sources


class SensorTopologyProviderRegistry:

    def get(self, config) -> SensorTopologyProvider:
        registry = dict()
        #registry["classic"] = lambda config: GenericSensorTopologyProvider(
        #    data_source_id_provider=DataSourceIdProviderRegistry().get(config["dataSources"]),
        #    transition_provider_factory=TransitionProviderRegistry().get(config["transitions"]["type"],
        #                                                                 config["transitions"]["args"]),
        #    duration_provider=DurationProviderRegistry().get(config["duration"]),
        #    send_provider=SinkProviderRegistry().get(config["sink"]),
        #    activity_emission_provider=ActivityEmissionProviderRegistry().get(config["activities"]))

        registry["concrete"] = lambda config: ConcreteSensorTopologyProvider(
            data_source_list=DataSourceRegistry().get(data_source_definitions=config["sensors"])
        )
        return registry["concrete"](config)

