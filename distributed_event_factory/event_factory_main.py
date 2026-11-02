import os
import sys

from dotenv import load_dotenv
from distributed_event_factory.event_factory import EventFactory

if __name__ == '__main__':
    if "local" in sys.argv:
        load_dotenv()
    datasource = os.environ.get("DATASOURCE")
    topology = os.environ.get("TOPOLOGY")
    sink = os.environ["SINK"]
    simulation = os.environ["SIMULATION"]
    postprocessor = os.environ.get("POSTPROCESSOR")
    content_root = os.environ["ROOT"]

    if not datasource and not topology:
        raise ValueError("Either DATASOURCE or TOPOLOGY must be set")

    event_factory = EventFactory()

    print("Running with config:")
    if datasource:
        print(f"datasource directory: {datasource}")
    if topology:
        print(f"topology: {topology}")
    print(f"Sink: {sink}")
    print(f"Simulation: {simulation}")
    if postprocessor:
        print(f"PostProcessor: {postprocessor}")
    print(f"Content root: {content_root}")

    if datasource:
        event_factory.add_directory(f"{content_root}/config/datasource/{datasource}")
    if topology:
        event_factory.add_file(f"{content_root}/config/topology/{topology}")
    event_factory.add_file(f"{content_root}/config/simulation/{simulation}")
    if postprocessor:
        event_factory.add_file(f"{content_root}/config/postprocessor/{postprocessor}")
    event_factory.add_file(f"{content_root}/config/sink/{sink}")
    event_factory.run()
