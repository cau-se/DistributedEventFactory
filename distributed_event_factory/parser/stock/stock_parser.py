from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider


class StockParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        stocks_list = []
        for stock in config["stocks"]:
            stocks_list.append(InputObjectProvider(
                objectName=stock["object"],
                numberOfObject=stock["number"],
                lastState=stock["lastState"]
            ))
        return stocks_list