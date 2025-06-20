import pm4py

from distributed_event_factory.simulation.abstract_process_simulator import ProcessSimulator
from process_mining_core.datastructure.core.SEvent import SEvent

class XesProcessSimulator(ProcessSimulator):

    def __init__(self, xes_file_path):
        self.log = pm4py.read_xes(xes_file_path)
        self.length = len(self.log)
        self.index = 0
        self.nodes = set()

    def simulate(self) -> SEvent:
        i = self.index % self.length
        node = self.log["org:resource"][i]
        event = SEvent(
            activity=self.log["concept:name"][i],
            caseid=self.log["case"][i],
            timestamp=self.log["time:timestamp"][i],
            group=self.log["org:resource"][i],
            node=self.log["org:resource"][i],
        )
        self.index = self.index + 1
        self.nodes.add(node)
        print(self.nodes)
        return event