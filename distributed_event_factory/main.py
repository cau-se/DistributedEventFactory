from time import sleep

from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    event_factory = EventFactory()
    (event_factory
     .add_file("../config/assemblyline/simulation/simulation_countbased.yaml")
     .add_directory("../config/assemblyline/datasource")
     .add_file("../config/assemblyline/sink/kafka-sink.yaml")
     ).run()
    sleep(1)