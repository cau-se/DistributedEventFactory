import unittest

from distributed_event_factory.topology.evaluator.topology_evaluator import TopologyEvaluator
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec


class _Event:
    def __init__(self, case_id, timestamp, activity):
        self.case_id = case_id
        self.timestamp = timestamp
        self.activity = activity


class TopologyEvaluatorTest(unittest.TestCase):
    def test_extract_and_score(self):
        evaluator = TopologyEvaluator()
        events = [
            _Event("case_1", "2024-01-01 00:00:01", "A"),
            _Event("case_1", "2024-01-01 00:00:02", "B"),
            _Event("case_2", "2024-01-01 00:00:01", "A"),
            _Event("case_2", "2024-01-01 00:00:02", "C"),
        ]

        traces = evaluator.extract_traces(events)
        metrics = evaluator.compute_metrics(traces, self._spec())
        score = evaluator.score(metrics, self._spec())

        self.assertEqual(2, metrics.distinct_traces_count)
        self.assertEqual(0.0, score.trace_length_penalty)
        self.assertEqual(0.0, score.distinct_traces_penalty)
        self.assertTrue(score.is_within_target)

    @staticmethod
    def _spec() -> TopologySpec:
        return TopologySpec(
            trace_length=TopologyConstraint(target=2, tolerance=0),
            distinct_traces=TopologyConstraint(target=2, tolerance=0),
            initial_datasource_count=2,
            initial_branching=1,
            max_iterations=5,
            sample_size=100
        )
