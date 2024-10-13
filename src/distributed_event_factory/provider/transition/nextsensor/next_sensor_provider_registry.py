from src.distributed_event_factory.provider.transition.nextsensor.next_sensor_provider import NextSensorProvider, ConstantNextSensorProvider

class NextSensorProviderRegistry:

    def get(self, config):
        registry = dict()

        registry["classic"] = lambda config: NextSensorProvider(config["transition"])
        registry["next_sensor"] = lambda config: ConstantNextSensorProvider(config["index"])

        if type(config) is int:
            return ConstantNextSensorProvider(config)

        return registry[config["type"]](config)