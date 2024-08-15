from core.event import Activity
from provider.activity.selection.activity_selection_provider import ActivitySelectionProvider, \
    ActivitySelectionProviderFactory


class SingleActivitySelectionProviderFactory(ActivitySelectionProviderFactory):

    def __init__(self, activity: Activity):
        self.activity = activity

    def get_activity_provider(self) -> ActivitySelectionProvider:
        return SingleActivitySelectionProvider(self.activity)


class SingleActivitySelectionProvider(ActivitySelectionProvider):
    def __init__(self, activity: Activity):
        self.activity = activity

    def emit_activity(self) -> Activity:
        return self.activity
