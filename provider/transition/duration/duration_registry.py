from provider.transition.duration.duration_provider import DurationProvider, StaticDurationProvider, \
    UniformDurationProvider, GaussianDurationProvider

class DurationProviderRegistry(DurationProvider):
    def get(self, config) -> DurationProvider:
        registry = dict()
        registry["static"] = lambda config: StaticDurationProvider(config["duration"])
        registry["uniform"] = lambda config: UniformDurationProvider(config["lower_bound"], config["upper_bound"])
        registry["gaussian"] = lambda config: GaussianDurationProvider(config["mu"], config["sigma"])
        return registry[config["type"]](config)
