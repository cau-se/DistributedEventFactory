import os
import sys

from dotenv import load_dotenv

class DefConfigurator:

    def __init__(self):
        self.content_root = None
        self.datasource_dir = None
        self.sink = None
        self.simulation = None
        self.parse_config_files()

    def parse_config_files(self):
        if "local" in sys.argv:
            load_dotenv()
        self.datasource_dir = os.environ["DATASOURCE"]
        self.sink = os.environ["SINK"]
        self.simulation = os.environ["SIMULATION"]
        self.content_root = os.environ["ROOT"]

        print("Running with config:")
        print(f"datasource directory: {self.datasource_dir}")
        print(f"Sink: {self.sink}")
        print(f"Simulation: {self.simulation}")
        print(f"Content root: {self.content_root}")


    def get_datasource_dir(self):
        return f"{self.content_root}/{self.datasource_dir}"

    def get_simulation_file(self):
        return f"{self.content_root}/{self.simulation}"

    def get_sink_file(self):
        return f"{self.content_root}/{self.sink}"
