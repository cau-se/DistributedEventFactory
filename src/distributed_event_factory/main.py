import os

from src.distributed_event_factory.simulation.distributed_event_factory import DistributedEventFactory

if __name__ == '__main__':
    if "CONFIG_FILE" in os.environ:
        config_file = os.environ["CONFIG_FILE"]
    else:
        config_file = "config/assembly_line.yml"

    DistributedEventFactory(config_file).start()
