from distributed_event_factory.core.event import Activity
from distributed_event_factory.provider.activity.selection.activity_selection_provider import \
    ActivitySelectionProviderFactory, ActivitySelectionProvider


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
