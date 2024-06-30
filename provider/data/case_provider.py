import abc


class CaseIdProvider:

    @abc.abstractmethod
    def get(self):
        pass

class IncreasingCaseIdProvider(CaseIdProvider):

    def __init__(self):
        self.current_case_id = 0

    def get(self):
        self.current_case_id += 1
        return "case " + str(self.current_case_id)

