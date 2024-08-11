from provider.load.load_provider import LoadProvider, ConstantLoadProvider, GradualIncreasingLoadProvider

class LoadProviderRegistry:
    def get(self, config) -> LoadProvider:
        registry = dict()
        registry["constant"] = lambda config: ConstantLoadProvider(config["load"])
        registry["gradual"] = lambda config: GradualIncreasingLoadProvider(config["tickCount"], config["minimalLoad"],
                                                                           config["load"])
        return registry[config["loadType"]](config)
