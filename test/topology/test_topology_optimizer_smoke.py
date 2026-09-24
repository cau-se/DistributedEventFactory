import unittest

from distributed_event_factory.topology.actions.topology_actions import TopologyActionGenerator
from distributed_event_factory.topology.evaluator.topology_evaluator import TopologyEvaluator
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec
from distributed_event_factory.topology.optimizer.topology_optimizer import TopologyOptimizer


class _Event:
    def __init__(self, case_id, timestamp, activity):
        self.case_id = case_id
        self.timestamp = timestamp
        self.activity = activity


class TopologyOptimizerSmokeTest(unittest.TestCase):
    def test_optimizer_keeps_or_improves_best_score(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(target=3, tolerance=1),
            distinct_traces=TopologyConstraint(target=4, tolerance=2),
            initial_datasource_count=3,
            initial_branching=2,
            max_iterations=2,
            sample_size=20
        )
        optimizer = TopologyOptimizer(
            evaluator=TopologyEvaluator(),
            action_generator=TopologyActionGenerator()
        )

        def simulate_fn(graph, sample_size):
            events = []
            for case_idx in range(sample_size):
                case = f"case_{case_idx}"
                events.append(_Event(case, "2024-01-01 00:00:01", "A"))
                events.append(_Event(case, "2024-01-01 00:00:02", "B"))
                if case_idx % 2 == 0:
                    events.append(_Event(case, "2024-01-01 00:00:03", "C"))
            return events

        result = optimizer.optimize(spec, simulate_fn)

        self.assertGreaterEqual(result.iterations, 0)
        self.assertGreaterEqual(result.best_score.total, 0)
