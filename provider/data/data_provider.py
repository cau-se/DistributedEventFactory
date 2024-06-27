import abc

from utils.markov_chain import MarkovChain
from utils.utils_types import GeneratedEvent


class DataProvider:

    @abc.abstractmethod
    def get_data(self) -> GeneratedEvent:
        pass


class NodeDataProvider(DataProvider):

    def __init__(self, nodes, join_function):
        self.nodes = nodes
        self.join_function = join_function

    def get_data(self) -> GeneratedEvent:
        for node in self.nodes:
            node.refresh_data()

        if self.join_function is not None:
            data: GeneratedEvent = self.join_function([node.data for node in self.nodes if node.data])
            data.timestamp = str(data.timestamp)
            return data

class MarkovChainDataProvider(DataProvider):

    def __init__(self, markov_chain: MarkovChain):
        self.markov_chain = markov_chain

    def get_data(self) -> GeneratedEvent:
        return self.markov_chain.simulate(0, 1)[0]


