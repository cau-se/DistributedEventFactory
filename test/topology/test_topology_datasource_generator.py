import unittest

from distributed_event_factory.topology.generator.topology_datasource_generator import TopologyDatasourceGenerator
from distributed_event_factory.topology.model.topology_graph import TopologyGraph, TopologyNode


class TopologyDatasourceGeneratorTest(unittest.TestCase):
    def test_activity_names_count_edges_per_source_layer(self):
        graph = TopologyGraph(
            nodes={
                "<start>": TopologyNode("<start>", 0),
                "source-a": TopologyNode("source-a", 1),
                "source-b": TopologyNode("source-b", 1),
                "target-a": TopologyNode("target-a", 2),
                "target-b": TopologyNode("target-b", 2),
                "<end>": TopologyNode("<end>", 3),
            },
            edges={
                "<start>": {"source-a"},
                "source-a": {"target-b", "target-a"},
                "source-b": {"target-a", "<end>"},
                "target-a": {"<end>"},
                "target-b": {"<end>"},
                "<end>": set(),
            }
        )
        generator = TopologyDatasourceGenerator()

        self.assertEqual(
            {
                ("source-a", "target-a", 1): "A1",
                ("source-a", "target-b", 1): "A2",
                ("source-b", "<end>", 1): "A4",
                ("source-b", "target-a", 1): "A3",
                ("target-a", "<end>", 1): "B1",
                ("target-b", "<end>", 1): "B2",
            },
            generator.build_activity_names(graph)
        )

    def test_generated_configs_use_activity_names_and_identify_end_activities(self):
        graph = TopologyGraph(
            nodes={
                "<start>": TopologyNode("<start>", 0),
                "source": TopologyNode("source", 1),
                "target": TopologyNode("target", 2),
                "<end>": TopologyNode("<end>", 3),
            },
            edges={
                "<start>": {"source"},
                "source": {"target", "<end>"},
                "target": {"<end>"},
                "<end>": set(),
            },
            transition_counts={
                ("<start>", "source"): 1,
                ("source", "target"): 3,
                ("source", "<end>"): 1,
                ("target", "<end>"): 1,
            },
        )
        generator = TopologyDatasourceGenerator()
        configs = generator.build_datasource_configs(graph)

        self.assertEqual(
            ["A1", "A2", "A3", "A4"],
            [event["activity"] for event in configs["source"]["eventData"]]
        )
        self.assertEqual([0.25] * 4, configs["source"]["distribution"])
        self.assertEqual(["<end>", "target", "target", "target"], [
            event["transition"] for event in configs["source"]["eventData"]
        ])
        self.assertEqual({"A1", "B1"}, generator.build_end_activity_names(graph))

    def test_generated_distribution_uses_graph_transition_probabilities(self):
        graph = TopologyGraph(
            nodes={
                "<start>": TopologyNode("<start>", 0),
                "source": TopologyNode("source", 1),
                "target": TopologyNode("target", 2),
                "<end>": TopologyNode("<end>", 3),
            },
            edges={
                "<start>": {"source"},
                "source": {"target"},
                "target": {"<end>"},
                "<end>": set(),
            },
            transition_counts={
                ("<start>", "source"): 1,
                ("source", "target"): 2,
                ("target", "<end>"): 1,
            },
            transition_probabilities={
                ("source", "target", 1): 0.8,
                ("source", "target", 2): 0.2,
            },
        )

        configs = TopologyDatasourceGenerator().build_datasource_configs(graph)

        self.assertEqual([0.8, 0.2], configs["source"]["distribution"])

    def test_layer_labels_continue_after_z(self):
        self.assertEqual("AA", TopologyDatasourceGenerator._layer_label(27))


if __name__ == "__main__":
    unittest.main()
