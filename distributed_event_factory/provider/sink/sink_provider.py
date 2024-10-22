import abc

from process_mining_core.datastructure.core.event import Event


class Sink:
    def __init__(self, data_source_ref):
        self.data_source_ref = data_source_ref

    @abc.abstractmethod
    def send(self, event: Event) -> None:
        pass

    def get_datasource_ref(self):
        return self.data_source_ref


class SinkProvider:

    @abc.abstractmethod
    def get_sender(self, id) -> Sink:
        pass
