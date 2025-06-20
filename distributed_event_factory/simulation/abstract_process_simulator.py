from abc import ABC

from process_mining_core.datastructure.core.event import Event

class ProcessSimulator(ABC):

    def simulate(self) -> Event:
        pass

    def add_datasource(self, name, data_source):
        pass