import os
import threading

from simulation.distributed_event_factory import DistributedEventFactory

if __name__ == '__main__':
    if "CONFIG_FILE" in os.environ:
        config_file = os.environ["CONFIG_FILE"]
    else:
        config_file = "config/maturity-test.yml"

    distributed_event_factory = DistributedEventFactory(config_file)

    threading.Timer(10.0, distributed_event_factory.start).start()