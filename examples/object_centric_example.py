from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()
    (event_factory
    .add_file(configurator.get_simulation_file())
    .add_file(configurator.get_sink_file())
    .add_directory("../config/datasource/smart-factory-1P-withTR")
    .add_file("../config/process_simulation/process_simulation_oc.yaml"))
    event_factory.run()
    event_factory.get_sink("ocelConsole").end_timeframe()
