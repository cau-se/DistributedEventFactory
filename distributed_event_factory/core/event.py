from distributed_event_factory.provider.transition.transition.transition_provider import TransitionProvider

class CaseId:
    def __init__(self, case_id: str):
        self.case_id = case_id

class Activity:
    def __init__(self, activity: str):
        self.activity = activity

class StartEvent:
    def __init__(self, case_id: CaseId, transition_provider: TransitionProvider):
        self.case_id = case_id
        self.transition_provider = transition_provider
        self.node = "start"

    def get_case(self):
        return self.case_id

    def get_next_sensor(self):
        return self.transition_provider.get_transition()

    def __str__(self):
        return f"<Start of case {self.case_id}>"


class EndEvent:
    def __init__(self, case_id: CaseId):
        self.case_id = case_id

    def get_case(self):
        return self.case_id

    def __str__(self):
        return f"<End of case {self.case_id}>"


