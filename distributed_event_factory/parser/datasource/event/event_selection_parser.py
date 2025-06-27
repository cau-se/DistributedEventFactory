from core.core_decisions_datasource import GenericDecisions
from distributed_event_factory.parser.parser import Parser


class EventSelectionParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return GenericDecisions(self.dependencies[config['selection']].parse(config),
                                self.dependencies[config['type']].parse(config),
                                config['workstation'])
