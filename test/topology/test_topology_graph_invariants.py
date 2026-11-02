import unittest

from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec


class TopologyGraphInvariantTest(unittest.TestCase):
    def test_initial_graph_valid(self):
        graph = TopologyGraph.create_initial(self._spec())
        self.assertIn("<start>", graph.nodes)
        self.assertIn("<end>", graph.nodes)
        self.assertIn("Node-1", graph.nodes)
        self.assertIn("Node-3", graph.nodes)

    def test_initial_graph_uses_one_datasource_per_layer_with_parallel_transitions(self):
        spec = TopologySpec(
            trace_length=TopologyConstraint(target=4, tolerance=0),
            distinct_traces=TopologyConstraint(target=10, tolerance=2),
            initial_branching=3,
            max_iterations=5,
            sample_size=100
        )

        graph = TopologyGraph.create_initial(spec)

        self.assertEqual({"Node-1"}, graph.successors("<start>"))
        self.assertEqual({"Node-2"}, graph.successors("Node-1"))
        self.assertEqual({"Node-3"}, graph.successors("Node-2"))
        self.assertEqual({"Node-4"}, graph.successors("Node-3"))
        self.assertEqual({"<end>"}, graph.successors("Node-4"))
        self.assertEqual(3, graph.transition_count("Node-1", "Node-2"))
        self.assertEqual(3, graph.transition_count("Node-2", "Node-3"))
        self.assertEqual(3, graph.transition_count("Node-3", "Node-4"))
        self.assertEqual(3, graph.transition_count("Node-4", "<end>"))

    def test_backward_edge_rejected(self):
        graph = TopologyGraph.create_initial(self._spec())
        with self.assertRaises(ValueError):
            graph.add_edge("Node-2", "Node-1")

    @staticmethod
    def _spec() -> TopologySpec:
        return TopologySpec(
            trace_length=TopologyConstraint(target=10, tolerance=1),
            distinct_traces=TopologyConstraint(target=10, tolerance=2),
            initial_branching=2,
            max_iterations=5,
            sample_size=100
        )
