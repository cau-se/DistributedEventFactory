from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    event_factory = EventFactory()
    (event_factory
     .add_directory("../config/assemblyline/simulation")
     .add_directory("../config/assemblyline/datasource")
     .add_directory("../config/assemblyline/sink/loadtest")
     ).run()
