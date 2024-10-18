from abc import abstractmethod, ABC

from distributed_event_factory.core.datasource_id import DataSourceId


class DataSourceIdProvider(ABC):
    @abstractmethod
    def get_id(self) -> DataSourceId:
        pass


class DataSourceIdProviderRegistry():

    def get(self, config) -> DataSourceIdProvider:
        registry = dict()
        registry["list"] = lambda config: ListBasedSourceIdProvider(config["ids"])
        return registry[config["type"]](config)


class NumberDataSourceIdProvider(DataSourceIdProvider):

    def __init__(self):
        self.id = 0

    def get_id(self) -> DataSourceId:
        data_source_id = DataSourceId(str(self.id))
        self.id += 1
        return data_source_id


class ListBasedSourceIdProvider(DataSourceIdProvider):

    def __init__(self, id_list):
        self.id_list = id_list
        self.pointer = 0

    def get_id(self) -> DataSourceId:
        data_source_id = DataSourceId(str(self.id_list[self.pointer]))
        self.pointer += 1
        return data_source_id
