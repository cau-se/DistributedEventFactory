from provider.data.case_provider import CaseIdProviderRegistry
from provider.datasource.sensor_topology_registry import DataSourceProviderRegistry
from provider.generic.count_provider_registry import CountProviderRegistry
from provider.load.load_provider_registry import LoadProviderRegistry
from provider.transition.duration.duration_registry import DurationProviderRegistry
from simulation.event_loop_registry import EventLoopRegistry

providers = dict()
providers["numberOfDataSources"] = lambda config, field: CountProviderRegistry().get(config[field])
providers["caseId"] = lambda config, field: CaseIdProviderRegistry().get(config[field])
providers["duration"] = lambda config, field: DurationProviderRegistry().get(config[field])
providers["eventLoop"] = lambda config, field: EventLoopRegistry().get(config)
providers["loadProfile"] = lambda config, field: LoadProviderRegistry().get(config[field])
providers["dataSourceTopology"] = lambda config, field: DataSourceProviderRegistry().get(config[field])


class ProviderRegistry:

    def __init__(self, configuration):
        self.configuration = configuration

    def get(self, field):
        return providers[field](self.configuration, field)
