from distributed_event_factory.parser.parser import Parser
from provider.workforce.InputWorkforceProvider import InputWorkforceProvider


class WorkforceParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        workforce_for_step_list = []
        if config["workforces"]:
            for input in config["workforces"]:
                workforce_for_step_list.append(InputWorkforceProvider(
                    name=input["workforce"],
                    numberOfWorkforce=input["number"]
                ))
        return workforce_for_step_list

class DummyWorkforceParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        workforce_for_step_list = []
        return workforce_for_step_list