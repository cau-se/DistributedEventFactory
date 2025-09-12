from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.provider.object.size_params_provider import SizeParamsProvider


class StockParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        pass

    def parse(self, config):
        stocks_list = []
        for stock in config["stocks"]:
            size_params = None
            if stock["size"]:
                size_params = SizeParamsProvider(width=stock["size"]["width"],
                                                 depth=stock["size"]["depth"],
                                                 length=stock["size"]["length"])
            stocks_list.append(InputObjectProvider(
                objectName=stock["object"],
                numberOfObject=stock["number"],
                lastState=stock["lastState"],
                size=size_params,
            ))
        return stocks_list