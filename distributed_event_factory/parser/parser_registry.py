from distributed_event_factory.parser.datasource.event.activity.activity_parser import ActivityParser
from distributed_event_factory.parser.datasource.event.duration.constant_duration_parser import \
    ConstantDurationParser
from distributed_event_factory.parser.datasource.event.duration.duration_parser import DurationParser
from distributed_event_factory.parser.datasource.event.duration.gaussian_duration_parser import \
    GaussianDurationParser
from distributed_event_factory.parser.datasource.event.duration.uniform_duration_parser import \
    UniformDurationParser
from distributed_event_factory.parser.datasource.event.selection.drifting_probability_event_selection_parser import \
    DriftingProbabilityEventSelectionParser
from distributed_event_factory.parser.datasource.event.selection.generic_probability_event_selection_parser import \
    GenericProbabilityEventSelectionParser
from distributed_event_factory.parser.datasource.event.selection.ordered_event_selection_parser import \
    OrderedEventSelectionParser
from distributed_event_factory.parser.datasource.event.selection.uniform_event_selection import \
    UniformEventSelectionParser
from distributed_event_factory.parser.datasource.event.transition.transition_parser import TransitionParser
from distributed_event_factory.parser.simulation.case.case_id_parser import CaseIdParser
from distributed_event_factory.parser.datasource.data_source_parser import DataSourceParser
from distributed_event_factory.parser.datasource.event.distribution_parser import DistributionParser
from distributed_event_factory.parser.datasource.event.event_data_list_parser import EventDataListParser
from distributed_event_factory.parser.datasource.event.event_selection_parser import EventSelectionParser
from distributed_event_factory.parser.kind_parser import KindParser
from distributed_event_factory.parser.simulation.load.constant_load_parser import ConstantLoadParser
from distributed_event_factory.parser.simulation.load.gradual_load_parser import GradualLoadParser
from distributed_event_factory.parser.simulation.load.load_parser import LoadParser
from distributed_event_factory.parser.simulation.load.sinus_load_parser import SinusLoadParser
from distributed_event_factory.parser.simulation.simulation_parser import SimulationParser
from distributed_event_factory.parser.simulation.variant.countbased_simulation_parser import CountBasedSimulationParser
from distributed_event_factory.parser.simulation.variant.loadtest_simulation_parser import LoadTestSimulationParser
from distributed_event_factory.parser.simulation.variant.stream_simulation_parser import StreamSimulationParser
from distributed_event_factory.parser.sink.http_sink_parser import HttpSinkParser
from distributed_event_factory.parser.sink.kafka.case_partition_parser import CasePartitionParser
from distributed_event_factory.parser.sink.kafka.constant_partition_parser import ConstantPartitionParser
from distributed_event_factory.parser.sink.kafka.kafka_sink_parser import KafkaSinkParser
from distributed_event_factory.parser.sink.kafka.partition_parser import PartitionParser
from distributed_event_factory.parser.sink.print_console_sink_parser import PrintConsoleSinkParser
from distributed_event_factory.parser.sink.sink_parser import SinkParser
from distributed_event_factory.parser.sink.ui_sink_parser import UiSinkParser
from distributed_event_factory.provider.data.increasing_case import IncreasingCaseIdProvider


class ParserRegistry:

    def __init__(self):
        # Partitioning
        self.constant_partition_parser = ConstantPartitionParser()
        self.case_partition_parser = CasePartitionParser()
        self.partition_parser = (PartitionParser()
                                 .add_dependency("constant", self.constant_partition_parser)
                                 .add_dependency("case", self.case_partition_parser))

        # Sinks
        self.kafka_sink_parser = (KafkaSinkParser()).add_dependency("partition", self.partition_parser)
        self.console_sink_parser = (PrintConsoleSinkParser())
        self.ui_sink_parser = (UiSinkParser())
        self.http_sink_parser = (HttpSinkParser())
        self.sink_parser = (SinkParser()
                            .add_dependency("console", self.console_sink_parser)
                            .add_dependency("ui", self.ui_sink_parser)
                            .add_dependency("http", self.http_sink_parser)
                            .add_dependency("kafka", self.kafka_sink_parser))
        ##########
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
                                       .add_dependency("transition", self.transition_parser))

        # Distribution
        self.distribution_parser = (DistributionParser())

        self.uniform_event_selection_parser = (UniformEventSelectionParser())
        self.ordered_event_selection_parser = (OrderedEventSelectionParser())

        self.drifting_selection_parser = (DriftingProbabilityEventSelectionParser()
                                          .add_dependency("distribution", self.distribution_parser)
                                          .add_dependency("eventData", self.event_data_list_parser))

        self.probability_selection_parser = (GenericProbabilityEventSelectionParser()
                                             .add_dependency("distribution", self.distribution_parser)
                                             .add_dependency("eventData", self.event_data_list_parser))

        # Event Selection
        self.event_selection_parser = (EventSelectionParser()
                                       .add_dependency("ordered", self.ordered_event_selection_parser)
                                       .add_dependency("uniform", self.uniform_event_selection_parser)
                                       .add_dependency("genericProbability", self.probability_selection_parser)
                                       .add_dependency("driftingProbability", self.drifting_selection_parser))

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
        self.sinus_load_parser = SinusLoadParser()
        self.load_parser: LoadParser = (LoadParser()
                                        .add_dependency("constant", self.constant_load_parser)
                                        .add_dependency("gradual", self.gradual_load_parser)
                                        .add_dependency("sinus", self.sinus_load_parser))

        # Simulation
        self.count_based_simulation: CountBasedSimulationParser = (CountBasedSimulationParser()
                                                                   .add_dependency("caseId", self.case_id_parser))

        self.load_test_simulation: LoadTestSimulationParser = (LoadTestSimulationParser()
                                                               .add_dependency("load", self.load_parser)
                                                               .add_dependency("caseId", self.case_id_parser))

        self.stream_simulation: StreamSimulationParser = (StreamSimulationParser()
                                                          .add_dependency("load", self.load_parser)
                                                          .add_dependency("caseId", self.case_id_parser))

        self.simulation_parser: SimulationParser = (SimulationParser()
                                                    .add_dependency("stream", self.stream_simulation)
                                                    .add_dependency("countBased", self.count_based_simulation)
                                                    .add_dependency("loadTest", self.load_test_simulation))

        # Kind
        self.kind_parser: KindParser = (KindParser()
                                        .add_dependency("sink", self.sink_parser)
                                        .add_dependency("datasource", self.datasource_parser)
                                        .add_dependency("simulation", self.simulation_parser))
