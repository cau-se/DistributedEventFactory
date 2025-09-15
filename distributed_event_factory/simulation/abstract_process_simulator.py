from abc import ABC

from distributed_event_factory.simulation.abstract_process_simulator_config import ProcessSimulatorConfig
from process_mining_core.datastructure.core.event import Event

class ProcessSimulator(ABC):

    def simulate(self) -> Event:
        pass

    def configure(self, config: ProcessSimulatorConfig):
        pass