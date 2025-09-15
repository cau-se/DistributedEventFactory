from abc import ABC


class ProcessSimulatorConfig(ABC):

    def get_configs_of_type(self, type: str):
        pass