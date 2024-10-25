import os
import sys
from time import sleep

from dotenv import load_dotenv

from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    event_factory = EventFactory()

    if "local" in sys.argv:
        load_dotenv()

    datasource = os.environ["DATASOURCE"]
    sink = os.environ["SINK"]
    simulation = os.environ["SIMULATION"]

    (event_factory
     .add_directory(f"../config/datasource/{datasource}")
     .add_file(f"../config/simulation/{simulation}.yaml")
     .add_file(f"../config/sink/{sink}.yaml")
     ).run()
    sleep(10)
    #for sinks in event_factory.sinks:
    #    for sink in sinks:
    #        sink.start()
