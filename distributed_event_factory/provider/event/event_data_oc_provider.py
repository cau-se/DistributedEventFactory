from distributed_event_factory.provider.activity.activity_provider import ActivityProvider
from distributed_event_factory.provider.event.event_data_case_provider import EventDataProvider
from distributed_event_factory.provider.object.input.input_provider import InputObjectProvider
from distributed_event_factory.provider.transition.duration.duration_provider import DurationProvider
from distributed_event_factory.provider.transition.output.output_provider import OutputObjectProvider
from distributed_event_factory.provider.transition.transition.transition_provider import TransitionProvider


class EventDataOcProvider(EventDataProvider):

    def get_event_data(self):
        pass

    def __init__(
            self,
            duration_provider: DurationProvider,
            activity_provider: ActivityProvider,
            transition_provider: TransitionProvider,
            output_provider: OutputObjectProvider,
            input_provider: InputObjectProvider
    ):
        self.duration_provider: DurationProvider = duration_provider
        self.activity_provider: ActivityProvider = activity_provider
        self.transition_provider: TransitionProvider = transition_provider
        self.output_provider: OutputObjectProvider = output_provider
        self.input_provider: InputObjectProvider = input_provider

