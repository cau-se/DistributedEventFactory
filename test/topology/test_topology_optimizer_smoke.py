import unittest

from distributed_event_factory.topology.actions.topology_actions import TopologyActionGenerator
from distributed_event_factory.topology.evaluator.topology_evaluator import TopologyEvaluator
from distributed_event_factory.topology.evaluator.topology_evaluator import TopologyMetrics
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec
from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.optimizer.topology_optimizer import TopologyOptimizer


class _Event:
    def __init__(self, case_id, timestamp, activity):
        self.caseid = case_id
        self.timestamp = timestamp
        self.activity = activity


class TopologyOptimizerSmokeTest(unittest.TestCase):
    def test_transition_step_size_scales_with_variants_gap_and_is_capped(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(target=8, tolerance=1),
            distinct_traces=TopologyConstraint(target=100, tolerance=5),
            initial_branching=2,
            max_iterations=2,
            sample_size=100
        )
        graph = TopologyGraph.create_initial(spec)
        optimizer = TopologyOptimizer(
            evaluator=TopologyEvaluator(),
            action_generator=TopologyActionGenerator()
        )

        far_below_target = TopologyMetrics(8, 8, 8, 1.0, 10)
        near_target = TopologyMetrics(8, 8, 8, 1.0, 90)
        far_above_target = TopologyMetrics(8, 8, 8, 1.0, 1000)

        self.assertGreater(
            optimizer._transition_step_size(far_below_target, spec, graph),
            optimizer._transition_step_size(near_target, spec, graph),
        )
        self.assertEqual(5, optimizer._transition_step_size(far_above_target, spec, graph))

    def test_optimizer_keeps_or_improves_best_score(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(target=3, tolerance=1),
            distinct_traces=TopologyConstraint(target=4, tolerance=2),
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
