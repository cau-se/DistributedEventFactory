import unittest

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec
from distributed_event_factory.topology.optimizer.entropy_optimizer import TraceEntropyOptimizer


class TraceEntropyOptimizerTest(unittest.TestCase):
    def test_uniform_target_keeps_equal_transition_probabilities(self):
        spec = self._spec(target=1.0)
        graph = TopologyGraph.create_initial(spec)

        result = TraceEntropyOptimizer().optimize(graph, spec)

        self.assertTrue(result.target_reached)
        self.assertAlmostEqual(1.0, result.normalized_entropy)
        self.assertAlmostEqual(1 / 8, result.most_likely_trace_probability)
        self.assertAlmostEqual(0.5, result.graph.transition_probability("Node-1", "Node-2", 1))

    def test_low_target_concentrates_probability_on_preferred_trace(self):
        spec = self._spec(target=0.2, tolerance=0.03)
        graph = TopologyGraph.create_initial(spec)

        result = TraceEntropyOptimizer().optimize(graph, spec)

        self.assertTrue(result.target_reached)
        self.assertLess(result.normalized_entropy, 0.25)
        self.assertGreater(result.most_likely_trace_probability, 0.9)
        self.assertGreater(result.graph.transition_probability("Node-1", "Node-2", 1), 0.9)

    @staticmethod
    def _spec(target, tolerance=0.02):
        return TopologySpec(
            trace_length=TopologyConstraint(target=3, tolerance=0),
            distinct_traces=TopologyConstraint(target=8, tolerance=0),
            initial_branching=2,
            max_iterations=5,
            sample_size=100,
            trace_entropy=TopologyConstraint(target=target, tolerance=tolerance),
        )


if __name__ == "__main__":
    unittest.main()
