from provider.sensor.sensor_provider import SensorProvider
from provider.transition.transition_provider import TransitionProvider


class ProviderRegistry:
    def __init__(self,
                 transition_provider,
                 sensor_provider):
        self.transition_provider: TransitionProvider = transition_provider
        self.sensor_provider: SensorProvider = sensor_provider

    def get_sensor_provider(self):
        return self.sensor_provider

    def get_transition_provider(self):
        return self.transition_provider
