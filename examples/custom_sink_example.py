from pm4py.algo.discovery.alpha.variants.plus import add_sink

from algorithms.conformance_sink import ConformanceSink
from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.sink.sink_provider import Sink
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator
from process_mining_core.datastructure.core.event import Event


class MySink(Sink):
    def send(self, event: Event) -> None:
        print(f"My sink: {event}")

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()
    (event_factory
    .add_file(configurator.get_simulation_file())
    .add_process_simulator(
        XesProcessSimulator(
            "../config/xes/Road_Traffic_Fine_Management_Process.xes",
            node_key="concept:name",
            group_id_key="concept:name"
        ))
    .add_sink("my", ConformanceSink(["<any>"])))
    event_factory.run()