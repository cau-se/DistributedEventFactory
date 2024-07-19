from provider.activity.activity_emission_provider import ActivityEmissionProviderRegistry
from provider.datasource.datasource_id_provider import DataSourceIdProviderRegistry
from provider.datasource.sensor_topology import SensorTopologyProvider, GenericSensorTopologyProvider
from provider.sender.send_provider import SinkProviderRegistry
from provider.transition.duration_provider import DurationProviderRegistry
from provider.transition.transition_provider_factory import TransitionProviderRegistry


class SensorTopologyProviderRegistry:

    def get(self, type: str, args) -> SensorTopologyProvider:
        registry = dict()
        registry["classic"] = lambda config: GenericSensorTopologyProvider(
            data_source_id_provider=DataSourceIdProviderRegistry().get(config["dataSources"]),
            transition_provider_factory=TransitionProviderRegistry().get(config["transitions"]["type"],
                                                                         config["transitions"]["args"]),
            duration_provider=DurationProviderRegistry().get(config["duration"]),
            send_provider=SinkProviderRegistry().get(config["sink"]),
            activity_emission_provider=ActivityEmissionProviderRegistry().get(config["activities"]))
        return registry[type](args)
