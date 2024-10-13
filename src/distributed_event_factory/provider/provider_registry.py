from distributed_event_factory.provider.data.case_provider import CaseIdProviderRegistry
from distributed_event_factory.provider.datasource.sensor_topology_registry import DataSourceProviderRegistry
from distributed_event_factory.provider.generic.count_provider_registry import CountProviderRegistry
from distributed_event_factory.provider.load.load_provider_registry import LoadProviderRegistry
from distributed_event_factory.provider.transition.duration.duration_registry import DurationProviderRegistry
from distributed_event_factory.simulation.eventloop.event_loop_registry import EventLoopRegistry

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
