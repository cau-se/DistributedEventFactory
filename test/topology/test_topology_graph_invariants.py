import unittest

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec


class TopologyGraphInvariantTest(unittest.TestCase):
    def test_initial_graph_valid(self):
        graph = TopologyGraph.create_initial(self._spec())
        self.assertIn("<start>", graph.nodes)
        self.assertIn("<end>", graph.nodes)

    def test_backward_edge_rejected(self):
        graph = TopologyGraph.create_initial(self._spec())
        with self.assertRaises(ValueError):
            graph.add_edge("AutoDS2", "AutoDS1")

    @staticmethod
    def _spec() -> TopologySpec:
        return TopologySpec(
            trace_length=TopologyConstraint(target=10, tolerance=1),
            distinct_traces=TopologyConstraint(target=10, tolerance=2),
            initial_datasource_count=3,
            initial_branching=2,
            max_iterations=5,
            sample_size=100
        )
