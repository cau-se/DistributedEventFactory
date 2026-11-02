from contextlib import redirect_stdout
from io import StringIO
import unittest

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec
from distributed_event_factory.topology.optimizer.payload_optimizer import PayloadOptimizer


class PayloadOptimizerTest(unittest.TestCase):
    def test_payload_stage_reaches_target_success_ratio_with_integer_deltas(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(target=8, tolerance=1),
            distinct_traces=TopologyConstraint(target=1000, tolerance=5),
            initial_branching=5,
            max_iterations=10,
            sample_size=1000,
            payload_success_threshold=80,
            successful_case_ratio=TopologyConstraint(target=80, tolerance=2),
            payload_entropy=TopologyConstraint(target=0.7, tolerance=0.1),
        )

        with redirect_stdout(StringIO()):
            result = PayloadOptimizer().optimize(TopologyGraph.create_initial(spec), spec)

        self.assertGreaterEqual(result.expected_success_ratio, 0.78)
        self.assertLessEqual(result.expected_success_ratio, 0.82)
        self.assertTrue(result.target_reached)
        self.assertTrue(result.entropy_target_reached)
        self.assertTrue(result.success_ratio_target_reached)
        self.assertGreaterEqual(result.normalized_entropy, 0.0)
        self.assertLessEqual(result.normalized_entropy, 1.0)
        self.assertGreater(len(result.expected_contributions), 0)
        self.assertTrue(any(entry["type"] == "iteration" for entry in result.optimization_log))
        for delta in result.graph.payload_deltas.values():
            self.assertIsInstance(delta, int)
            self.assertGreaterEqual(delta, 0)
        self.assertGreater(result.iterations, 0)
        self.assertTrue(all(1 <= entry["stepSize"] <= 10 for entry in result.optimization_log if entry["type"] == "iteration"))

    def test_step_size_scales_with_success_gap_and_is_capped(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(target=8, tolerance=1),
            distinct_traces=TopologyConstraint(target=1000, tolerance=5),
            initial_branching=5,
            max_iterations=10,
            sample_size=1000,
            payload_success_threshold=80,
            successful_case_ratio=TopologyConstraint(target=80, tolerance=2),
            payload_entropy=TopologyConstraint(target=0.7, tolerance=0.1),
        )

        self.assertEqual(3, PayloadOptimizer._step_size(1.0, spec))
        self.assertEqual(1, PayloadOptimizer._step_size(0.81, spec))
        self.assertEqual(9, PayloadOptimizer._step_size(0.0, spec))

        short_trace_spec = TopologySpec(
            trace_length=TopologyConstraint(target=1, tolerance=0),
            distinct_traces=TopologyConstraint(target=1000, tolerance=5),
            initial_branching=1,
            max_iterations=10,
            sample_size=100,
            payload_success_threshold=80,
            successful_case_ratio=TopologyConstraint(target=0, tolerance=0),
            payload_entropy=TopologyConstraint(target=0.7, tolerance=0.1),
        )
        self.assertEqual(10, PayloadOptimizer._step_size(1.0, short_trace_spec))


if __name__ == "__main__":
    unittest.main()
