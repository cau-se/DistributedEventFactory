from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.workforce.InputWorkforceProvider import WorkforceStartPositionProvider


class WorkforceStartPositionParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        workforce_with_start_position = []
        if config["workforces"]:
            for workforce in config["workforces"]:
                workforce_with_start_position.append(WorkforceStartPositionProvider(
                    name=workforce["name"],
                    numberOfWorkforce=workforce["number"],
                    location=workforce["startLocation"],
                ))
        return workforce_with_start_position