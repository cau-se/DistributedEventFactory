from provider.load.load_provider_registry import LoadProviderRegistry
from simulation.event_loop import DebugEventLoop, LoadEventLoop


class EventLoopRegistry:

    def get(self, config):
        registry = dict()
        registry["debug"] = lambda config: DebugEventLoop()
        registry["load"] = lambda config: LoadEventLoop(LoadProviderRegistry().get(config["loadProfile"]))
        return registry[config["type"]](config)
