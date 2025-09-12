from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.simulation.process_simulation_object_centric import ProcessSimulationObjectCentric
from distributed_event_factory.simulation.simulator_objects.object_storage import ObjectStorage

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()
    (event_factory
    .add_file(configurator.get_simulation_file())
    .add_file(configurator.get_sink_file())
    .add_directory("../config/datasource/smart-factory-1P-withTR")
    .add_file("../config/process_simulation/process_simulation.yaml")
    #.add_process_simulator(
    #    ProcessSimulationObjectCentric(
    #        data_sources=datasources,
    #        objects=objects,
    #        routes=routes,
    #        stocks=stocks,
    #        workforce_start_positions=workforce_start_positions
    #    )
    #)
    )
    event_factory.run()
