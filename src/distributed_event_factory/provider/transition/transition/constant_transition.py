from distributed_event_factory.provider.transition.transition_provider import TransitionProvider

class ConstantTransitionProvider(TransitionProvider):
    def __init__(self, next_sensor_index):
        self.next_sensor_index = next_sensor_index

    def get_transition(self):
        return self.next_sensor_index
