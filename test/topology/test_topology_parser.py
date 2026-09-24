import unittest

from distributed_event_factory.parser.topology.topology_parser import TopologyParser


class TopologyParserTest(unittest.TestCase):
    def test_parse(self):
        parser = TopologyParser()

        parsed = parser.parse({
            "constraints": {
                "traceLength": {"target": 10, "tolerance": 1},
                "distinctTraces": {"target": 50, "tolerance": 10}
            },
            "generation": {
                "initialDatasourceCount": 6,
                "initialBranching": 2
            },
            "optimize": {
                "maxIterations": 20,
                "sampleSize": 500
            }
        })

        self.assertEqual(10, parsed.trace_length.target)
        self.assertEqual(1, parsed.trace_length.tolerance)
        self.assertEqual(50, parsed.distinct_traces.target)
        self.assertEqual(10, parsed.distinct_traces.tolerance)
        self.assertEqual(6, parsed.initial_datasource_count)
        self.assertEqual(2, parsed.initial_branching)
        self.assertEqual(20, parsed.max_iterations)
        self.assertEqual(500, parsed.sample_size)
