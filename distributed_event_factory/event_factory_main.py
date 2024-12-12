import os
import sys

from dotenv import load_dotenv
from distributed_event_factory.event_factory import EventFactory

def print_dir(directory):
    print("-"*20)
    for filename in os.listdir(directory):
        print(filename)


if __name__ == '__main__':
    datasource = os.environ["DATASOURCE"]
    sink = os.environ["SINK"]
    simulation = os.environ["SIMULATION"]
    content_root = os.environ["ROOT"]

    print_dir(f"{content_root}/config/datasource/{datasource}")
    event_factory = EventFactory()

    if "local" in sys.argv:
        load_dotenv()

    print_dir(f"{content_root}/config/datasource/{datasource}")

    print("Running with config:")
    print(f"datasource directory: {datasource}")
    print(f"Sink: {sink}")
    print(f"Simulation: {simulation}")
    print(f"Content root: {content_root}")


    (event_factory
     .add_directory(f"{content_root}/config/datasource/{datasource}")
     .add_file(f"{content_root}/config/simulation/{simulation}")
     .add_file(f"{content_root}/config/sink/{sink}")
     ).run()
