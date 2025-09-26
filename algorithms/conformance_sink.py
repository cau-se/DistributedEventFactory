from typing import List

import pm4py.discovery
from pm4py.objects.log.obj import EventLog

from distributed_event_factory.provider.sink.sink_provider import Sink
from process_mining_core.converter.pm4py_converter import Pm4PyConverter
from process_mining_core.datastructure.core.event import Event
from process_mining_core.eventlog_features.measures import EventLogFeatureMeasures
from process_mining_core.eventlog_features.variants import VariantEventLogFeatures


class ConformanceSink(Sink):

    def send(self, event: Event) -> None:
        self.log.append(event)

    def __init__(
        self,
        data_source_ref,
        algorithm=lambda log: pm4py.discovery.discover_petri_net_inductive(log)
    ):
        super().__init__(data_source_ref)
        self.mined_log = []
        self.log: List[Event] = []
        self.algorithm = algorithm
        self.event_log = EventLog()

    def end(self):
        event_log = Pm4PyConverter().from_event_log(self.log)
        self.petri_net, self.initial_marking, self.final_marking = pm4py.discovery.discover_petri_net_inductive(
            event_log)
        petri_net, initial_marking, final_marking = self.algorithm(event_log)
            #pm4py.filtering.filter_log_relative_occurrence_event_attribute(
            #    log=event_log,
            #    level="events",
            #    min_relative_stake=0
            #)
        #)
        self.mined_log = Pm4PyConverter().to_event_log(
            pm4py.sim.play_out(self.petri_net, self.initial_marking, self.final_marking))
        view = pm4py.visualization.petri_net.visualizer.apply(self.petri_net, self.initial_marking, self.final_marking)
        pm4py.visualization.petri_net.visualizer.view(view)

    def get_recall_n_gram(self, threshold_percentage):
        predict = VariantEventLogFeatures().get_top_percent(
            VariantEventLogFeatures().count_ngrams(self.mined_log[0:1000], 2), threshold_percentage)
        ground_truth = VariantEventLogFeatures().get_top_percent(
            VariantEventLogFeatures().count_ngrams(self.log[0:1000], 2), threshold_percentage)
        print("Recall ngram:")
        print(f"Predict: {predict}")
        print(f"Ground Truth: {ground_truth}")
        return EventLogFeatureMeasures().recall(predict, ground_truth)

    def get_precision_n_gram(self, threshold_percentage):
        predict = VariantEventLogFeatures().get_top_percent(
            VariantEventLogFeatures().count_ngrams(self.mined_log[0:1000], 2), threshold_percentage)
        ground_truth = VariantEventLogFeatures().get_top_percent(
            VariantEventLogFeatures().count_ngrams(self.log[0:1000], 2), threshold_percentage)
        return EventLogFeatureMeasures().precision(predict, ground_truth)

    def get_recall_outlier(self, threshold):
        predict = VariantEventLogFeatures().get_outlier_activities(self.mined_log[0:1000], threshold)
        ground_truth = VariantEventLogFeatures().get_outlier_activities(self.log[0:1000], threshold)

        print("Recall outlier:")
        print(f"Predict: {predict}")
        print(f"Ground Truth: {ground_truth}")
        return EventLogFeatureMeasures().recall(predict, ground_truth)

    def get_precision_outlier(self, threshold):
        predict = VariantEventLogFeatures().get_outlier_activities(self.mined_log[0:1000], threshold)
        ground_truth = VariantEventLogFeatures().get_outlier_activities(self.log[0:1000], threshold)
        return EventLogFeatureMeasures().precision(predict, ground_truth)

    def get_recall(self):
        return pm4py.conformance.fitness_alignments(
            Pm4PyConverter().from_event_log(self.log),
            self.petri_net,
            self.initial_marking,
            self.final_marking
        )["averageFitness"]

    def get_precision(self):
        return pm4py.conformance.precision_alignments(
            Pm4PyConverter().from_event_log(self.log),
            self.petri_net,
            self.initial_marking,
            self.final_marking
        )
