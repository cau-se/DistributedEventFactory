from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()
    (event_factory
    .add_file(configurator.get_simulation_file())
    .add_file(configurator.get_sink_file())
    .add_process_simulator(
        XesProcessSimulator(
            "../config/xes/Road_Traffic_Fine_Management_Process.xes",
            node_key="concept:name",
            group_id_key="concept:name"
        ))
    )

    event_factory.run()
