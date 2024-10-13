from src.distributed_event_factory.event_factory import EventFactory
from src.distributed_event_factory.parser.parser import Parser
from src.distributed_event_factory.provider.load.load_provider import LoadProvider
import math

class SinusLoadProvider(LoadProvider):
    def __init__(self, mean, amplitude, phase):
        self.i = 0
        self.mean = mean
        self.amplitude = amplitude
        self.phase = phase

    def get_load_value(self):
        self.i = self.i + 1
        return self.amplitude * math.sin(self.i*(math.pi/self.phase)) + self.mean


class SinusLoadParser(Parser):
    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return SinusLoadProvider(config["mean"], config["amplitude"], config["phase"])


if __name__ == '__main__':
    #if "CONFIG_FILE" in os.environ:
    #    config_file = os.environ["CONFIG_FILE"]
    #else:
    #    config_file = "config/syntheticpetrinet.yaml"

    event_factory = EventFactory()
    event_factory.parser.load_parser.add_dependency("sinus", SinusLoadParser())
    event_factory.run("config/assemblyline")

    #DistributedEventFactory.from_config_file(config_file).start()
