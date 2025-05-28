from abc import ABC, abstractmethod


class ActivityProvider(ABC):

    @abstractmethod
    def get_activity(self):
        pass


class ConstantActivityProvider(ActivityProvider):

    def __init__(self, activity_name):
        self.activity_name = activity_name

    def get_activity(self):
        return self.activity_name

class ObjectConstantActivityProvider(ActivityProvider):

    def __init__(self, activity_name, output):
        self.activity_name = activity_name
        self.output = output

    def get_activity(self):
        return self.activity_name
