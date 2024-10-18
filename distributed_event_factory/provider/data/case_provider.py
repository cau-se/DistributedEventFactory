import abc
from random import random


class CaseIdProvider:

    @abc.abstractmethod
    def get(self):
        pass
