from distributed_event_factory.provider.data.case_provider import CaseIdProvider

class IncreasingCaseIdProvider(CaseIdProvider):

    def __init__(self):
        self.current_case_id = 0

    def get(self):
        self.current_case_id += 1
        return f"case_{str(self.current_case_id)}"
