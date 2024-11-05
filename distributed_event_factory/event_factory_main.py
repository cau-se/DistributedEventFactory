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
    content_root = os.environ["ROOT"]

    print("Running with config:")
    print(f"datasource directory: {datasource}")
    print(f"Sink: {sink}")
    print(f"Simulation: {simulation}")
    print(f"Content root: {content_root}")

    (event_factory
     .add_directory(f"{content_root}/config/datasource/{datasource}")
     .add_file(f"{content_root}/config/simulation/{simulation}.yaml")
     .add_file(f"{content_root}/config/sink/{sink}.yaml")
     ).run()
    sleep(10)
