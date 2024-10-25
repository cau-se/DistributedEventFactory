from time import sleep

from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    event_factory = EventFactory()
    (event_factory
     .add_directory("../config/datasource/assemblyline")
     .add_file("../config/simulation/loadtest.yaml")
     .add_file("../config/sink/loadtest-sink.yaml")
     ).run()
    sleep(1)