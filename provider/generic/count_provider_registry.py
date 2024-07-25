from provider.generic.count_provider import CountProvider, UniformCountProvider, StaticCountProvider

class CountProviderRegistry:
    def get(self, config) -> CountProvider:
        registry = dict()
        registry["static"] = lambda config: StaticCountProvider(config["count"])
        registry["uniform"] = lambda config: UniformCountProvider(config["min"], config["max"])
        return registry[config["type"]](config)
