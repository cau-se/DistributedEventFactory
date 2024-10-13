from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.data.case_provider import IncreasingCaseIdProvider


class IncreasingCaseIdParser(Parser):

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        return IncreasingCaseIdProvider()