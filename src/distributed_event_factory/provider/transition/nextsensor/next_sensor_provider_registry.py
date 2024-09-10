from src.distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, DistinctNextSensorProvider

class NextSensorProviderRegistry:

    def get(self, config):
        registry = dict()

        registry["classic"] = lambda config: NextSensorProvider(config["transition"])
        registry["next_sensor"] = lambda config: DistinctNextSensorProvider(config["index"])

        if type(config) is int:
            return DistinctNextSensorProvider(config)

        return registry[config["type"]](config)