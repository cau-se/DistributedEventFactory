import requests

from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.datastructure.core.event import Event


class HttpSink(Sink):

    def __init__(self, url, data_source_ref):
        super().__init__(data_source_ref)
        self.url = url

    def send(self, event: Event) -> None:
        requests.post(url=self.url, json=event.__dict__)

    def get_datasource_ref(self):
        return super().get_datasource_ref()
