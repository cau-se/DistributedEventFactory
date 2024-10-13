from src.distributed_event_factory.parser.datasource.event.activity.activity_parser import ActivityParser
from src.distributed_event_factory.parser.datasource.event.duration.constant_duration_parser import \
    ConstantDurationParser
from src.distributed_event_factory.parser.datasource.event.duration.duration_parser import DurationParser
from src.distributed_event_factory.parser.datasource.event.duration.gaussian_duration_parser import \
    GaussianDurationParser
from src.distributed_event_factory.parser.datasource.event.duration.uniform_duration_parser import \
    UniformDurationParser
from src.distributed_event_factory.parser.datasource.event.transition.transition_parser import TransitionParser
from src.distributed_event_factory.parser.simulation.case.case_id_parser import CaseIdParser
from src.distributed_event_factory.parser.datasource.data_source_parser import DataSourceParser
from src.distributed_event_factory.parser.datasource.event.distribution_parser import DistributionParser
from src.distributed_event_factory.parser.datasource.event.event_data_list_parser import EventDataListParser
from src.distributed_event_factory.parser.datasource.event.event_data_parser import EventDataParser
from src.distributed_event_factory.parser.datasource.event.event_selection_parser import EventSelectionParser
from src.distributed_event_factory.parser.kind_parser import KindParser
from src.distributed_event_factory.parser.simulation.load.constant_load_parser import ConstantLoadParser
from src.distributed_event_factory.parser.simulation.load.gradual_load_parser import GradualLoadParser
from src.distributed_event_factory.parser.simulation.load.load_parser import LoadParser
from src.distributed_event_factory.parser.simulation.simulation_parser import SimulationParser
from src.distributed_event_factory.parser.sink.print_console_sink_parser import PrintConsoleSinkParser
from src.distributed_event_factory.parser.sink.sink_parser import SinkParser
from src.distributed_event_factory.parser.sink.ui_sink_parser import UiSinkParser
from src.distributed_event_factory.provider.data.case_provider import IncreasingCaseIdProvider


class ParserRegistry:

    def __init__(self):
        # Sinks
        self.console_sink_parser = (PrintConsoleSinkParser())
        self.ui_sink_parser = (UiSinkParser())
        self.sink_parser = (SinkParser()
                            .add_dependency("console", self.console_sink_parser)
                            .add_dependency("ui", self.ui_sink_parser))

        ##########
        # Event Data
        self.event_data_parser = EventDataParser()

        # Activity
        self.activity_parser = ActivityParser()

        # Duration
        self.constant_duration_parser = ConstantDurationParser()
        self.uniform_duration_parser = UniformDurationParser()
        self.gaussian_duration_parser = GaussianDurationParser()
        self.duration_parser = (DurationParser()
                                .add_dependency("constant", self.constant_duration_parser)
                                .add_dependency("uniform", self.uniform_duration_parser)
                                .add_dependency("gaussian", self.gaussian_duration_parser))

        # Transition
        self.transition_parser = TransitionParser()


        # Event Data List
        self.event_data_list_parser = (EventDataListParser()
                                       .add_dependency("duration", self.duration_parser)
                                       .add_dependency("activity", self.activity_parser)
                                       .add_dependency("transition", self.transition_parser)
                                       .add_dependency("eventData", self.event_data_parser))

        # Distribution
        self.distribution_parser = (DistributionParser())

        # Event Selection
        self.event_selection_parser = (EventSelectionParser()
                                       .add_dependency("distribution", self.distribution_parser)
                                       .add_dependency("eventDataList", self.event_data_list_parser))

        # DataSource
        self.datasource_parser = (DataSourceParser()
                                  .add_dependency("eventData", self.event_selection_parser))

        ##########
        # Case
        self.increasing_case_id_parser = IncreasingCaseIdProvider()
        self.case_id_parser: CaseIdParser = (CaseIdParser()
                                             .add_dependency("increasing", self.increasing_case_id_parser))

        # Load
        self.constant_load_parser = ConstantLoadParser()
        self.gradual_load_parser = GradualLoadParser()
        self.gaussian_load_parser = GradualLoadParser()
        self.load_parser: LoadParser = (LoadParser()
                                        .add_dependency("constant", self.constant_load_parser)
                                        .add_dependency("gradual", self.gradual_load_parser))

        # Simulation
        self.simulation_parser: SimulationParser = (SimulationParser()
                                  .add_dependency("load", self.load_parser)
                                  .add_dependency("caseId", self.case_id_parser))

        # Kind
        self.kind_parser: KindParser = (KindParser()
                            .add_dependency("sink", self.sink_parser)
                            .add_dependency("datasource", self.datasource_parser)
                            .add_dependency("simulation", self.simulation_parser))

