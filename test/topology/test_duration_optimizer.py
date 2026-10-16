from contextlib import redirect_stdout
from io import StringIO
import unittest

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec
from distributed_event_factory.topology.optimizer.duration_optimizer import DurationOptimizer


class DurationOptimizerTest(unittest.TestCase):
    def test_optimizes_average_duration_and_step_entropy_with_integer_minutes(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(4, 0),
            distinct_traces=TopologyConstraint(16, 1),
            initial_branching=2,
            max_iterations=10,
            sample_size=100,
            average_trace_duration=TopologyConstraint(20, 2),
            duration_entropy=TopologyConstraint(0.65, 0.1),
            max_duration_per_transition=10,
        )

        with redirect_stdout(StringIO()):
            result = DurationOptimizer().optimize(TopologyGraph.create_initial(spec), spec)

        self.assertLessEqual(abs(result.average_trace_duration - 20), 2)
        self.assertTrue(result.duration_target_reached)
        self.assertTrue(result.entropy_target_reached)
        self.assertTrue(all(isinstance(value, int) for value in result.graph.durations.values()))
        self.assertTrue(all(1 <= value <= 10 for value in result.graph.durations.values()))


if __name__ == "__main__":
    unittest.main()
