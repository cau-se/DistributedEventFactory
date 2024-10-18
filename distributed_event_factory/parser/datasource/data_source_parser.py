from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.core.datasource import GenericDataSource
from distributed_event_factory.core.datasource_id import DataSourceId

class DataSourceParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return GenericDataSource(
            data_source_id=DataSourceId(config["name"]),
            group_id=config["group"],
            event_provider=self.dependencies["eventData"].parse(config)
        )

