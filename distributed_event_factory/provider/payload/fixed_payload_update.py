from distributed_event_factory.provider.payload.payload_update_provider import PayloadUpdateProvider


class FixedPayloadUpdateProvider(PayloadUpdateProvider):
    def __init__(self, value):
        self.value = value

    def get_payload_delta(self):
        return self.value
