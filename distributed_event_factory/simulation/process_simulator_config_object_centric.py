from typing import Dict, Any

from kafka.errors import IllegalArgumentError

from distributed_event_factory.simulation.abstract_process_simulator_config import ProcessSimulatorConfig

class ProcessSimulatorConfigObjectCentric(ProcessSimulatorConfig):

    def __init__(self):
        self.configs: Dict[str, Dict[str, Any]] = dict()

    def get_configs_of_type(self, config_type: str):
        if config_type not in self.configs:
            raise IllegalArgumentError(f"Config key \"{config_type}\" is not available")
        return self.configs[config_type]

    def add_datasources(self, datasource_config: Dict[str, Any]):
        self.configs["datasource"] = datasource_config

    def add_objects(self, object_config: Dict[str, Any]):
        self.configs["object"] = object_config

    def add_routes(self, route_config: Dict[str, Any]):
        self.configs["route"] = route_config

    def add_stocks(self, stock_config: Dict[str, Any]):
        self.configs["stock"] = stock_config

    def add_workforce_start_position(self, workforce_start_position: Dict[str, Any]):
        self.configs["workforcePosition"] = workforce_start_position
