from distributed_event_factory.provider.data.count_provider import CountProvider


class ConstantCountProvider(CountProvider):

    def __init__(self, count):
        self.count=count

    def get(self) -> int:
        return self.count