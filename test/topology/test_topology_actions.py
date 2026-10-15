import unittest

from distributed_event_factory.topology.actions.topology_actions import TopologyActionGenerator
from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec


class TopologyActionGeneratorTest(unittest.TestCase):
    def test_candidates_only_change_transition_counts_on_existing_edges(self):
        graph = TopologyGraph.create_initial(self._spec())
        generator = TopologyActionGenerator()

        change_amount = 3
        actions = generator.generate_candidates(graph, change_amount)

        self.assertTrue(actions)
        self.assertTrue(all(action.name in {"increase_transition", "decrease_transition"} for action in actions))
        self.assertFalse(any(action.name == "decrease_transition" and graph.transition_count(
            action.payload["src"], action.payload["dst"]
        ) == 1 for action in actions))

        for action in actions:
            src, dst = action.payload["src"], action.payload["dst"]
            self.assertIn(dst, graph.successors(src))
            candidate = generator.apply(graph, action)
            change = change_amount if action.name == "increase_transition" else -change_amount
            self.assertEqual(
                max(1, graph.transition_count(src, dst) + change),
                candidate.transition_count(src, dst)
            )
            self.assertEqual(graph.nodes, candidate.nodes)
            self.assertEqual(graph.edges, candidate.edges)

    @staticmethod
    def _spec() -> TopologySpec:
        return TopologySpec(
            trace_length=TopologyConstraint(target=3, tolerance=0),
            distinct_traces=TopologyConstraint(target=10, tolerance=2),
            initial_branching=2,
            max_iterations=1,
            sample_size=5,
        )


if __name__ == "__main__":
    unittest.main()
