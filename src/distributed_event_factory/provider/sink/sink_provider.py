import abc

from distributed_event_factory.core.event import Event


class Sink:

    @abc.abstractmethod
    def send(self, event: Event) -> None:
        pass


class SinkProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sink:
        pass
