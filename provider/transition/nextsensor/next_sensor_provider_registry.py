from provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, DistinctNextSensorProvider

class NextSensorProviderRegistry:

    def get(self, config):
        registry = dict()

        registry["classic"] = lambda config: NextSensorProvider(config["transition"])
        registry["next_sensor"] = lambda config: DistinctNextSensorProvider(config["index"])

        return registry[config["type"]](config)