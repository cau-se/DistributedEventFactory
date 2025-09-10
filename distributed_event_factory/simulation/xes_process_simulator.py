import pm4py

from distributed_event_factory.simulation.abstract_process_simulator import ProcessSimulator
from process_mining_core.datastructure.core.event import Event

class XesProcessSimulator(ProcessSimulator):

    def __init__(
        self,
        xes_file_path,
        activity_key="concept:name",
        case_id_key="case:concept:name",
        timestamp_key="time:timestamp",
        node_key="org:resource",
        group_id_key="org:resource"
    ):
        self.log = pm4py.read_xes(xes_file_path)
        self.length = len(self.log)
        self.index = 0
        self.nodes = set()
        self.activity_key = activity_key
        self.case_id_key = case_id_key
        self.timestamp_key = timestamp_key
        self.node_key = node_key
        self.group_id_key = group_id_key

    def simulate(self) -> Event:
        i = self.index % self.length
        node = self.log[self.node_key][i]
        event = Event(
            activity=self.log[self.activity_key][i],
            case_id=self.log[self.case_id_key][i],
            timestamp=self.log[self.timestamp_key][i],
            group_id=self.log[self.group_id_key][i],
            node=node,
        )
        self.index = self.index + 1
        self.nodes.add(node)
        print(self.nodes)
        return event
