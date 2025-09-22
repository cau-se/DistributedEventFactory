from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()
    (event_factory
     .add_file(configurator.get_sink_file())
     .add_directory("../config/datasource/assemblyline")
     .add_file("../config/simulation/countbased.yaml")
     .add_file("../config/process_simulation/process_simulation.yaml")
     )
    event_factory.run()