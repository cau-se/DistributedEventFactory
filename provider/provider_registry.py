from provider.data.case_provider import CaseIdProviderRegistry
from provider.datasource.sensor_topology_registry import DataSourceProviderRegistry
from provider.generic.count_provider_registry import CountProviderRegistry
from provider.load.load_provider_registry import LoadProviderRegistry
from provider.transition.duration.duration_registry import DurationProviderRegistry

providers = dict()
providers["numberOfDataSources"] = lambda config: CountProviderRegistry().get(config)
providers["caseId"] = lambda config: CaseIdProviderRegistry().get(config)
providers["duration"] = lambda config: DurationProviderRegistry().get(config)
providers["loadProfile"] = lambda config: LoadProviderRegistry().get(config)
providers["dataSourceTopology"] = lambda config: DataSourceProviderRegistry().get(config)

class ProviderRegistry:

    def __init__(self, configuration):
        self.configuration = configuration

    def get(self, field):
        return providers[field](self.configuration[field])
