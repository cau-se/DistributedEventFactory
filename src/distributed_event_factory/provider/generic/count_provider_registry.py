from src.distributed_event_factory.provider.generic.count_provider import CountProvider, StaticCountProvider, \
    UniformCountProvider


class CountProviderRegistry:
    def get(self, config) -> CountProvider:
        registry = dict()
        registry["static"] = lambda config: StaticCountProvider(config["count"])
        registry["uniform"] = lambda config: UniformCountProvider(config["min"], config["max"])
        return registry[config["type"]](config)
