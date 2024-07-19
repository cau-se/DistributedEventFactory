from provider.data.case_provider import CaseIdProviderRegistry
from provider.datasource.datasource_id_provider import DataSourceIdProviderRegistry
from provider.datasource.sensor_topology import SensorTopologyProviderRegistry
from provider.generic.count_provider import CountProviderRegistry
from provider.load.load_provider import LoadProviderRegistry
from provider.transition.duration_provider import DurationProviderRegistry

providers = dict()
providers["numberOfSensors"] = lambda config: CountProviderRegistry().get(config["type"], config["args"])
providers["caseId"] = lambda config: CaseIdProviderRegistry().get(config)
providers["duration"] = lambda config: DurationProviderRegistry().get(config["type"], config["args"])
providers["loadProfile"] = lambda config: LoadProviderRegistry().get(config["type"], config["args"])
providers["sensorTopology"] = lambda config: SensorTopologyProviderRegistry().get(config["type"], config["args"])
providers["dataSourceId"] = lambda config: DataSourceIdProviderRegistry().get(config["dataSources"]["type"], config["dataSources"]["args"])

class ProviderRegistry:

    def __init__(self, configuration):
        self.configuration = configuration

    def get(self, field):
        return providers[field](self.configuration[field])
