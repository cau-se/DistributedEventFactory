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
                "initialBranching": 2
            },
            "optimize": {
                "maxIterations": 20,
                "sampleSize": 500
            },
            "payload": {
                "successThreshold": 80,
                "successfulCaseRatio": {"target": 80, "tolerance": 2}
            }
        })

        self.assertEqual(10, parsed.trace_length.target)
        self.assertEqual(1, parsed.trace_length.tolerance)
        self.assertEqual(50, parsed.distinct_traces.target)
        self.assertEqual(10, parsed.distinct_traces.tolerance)
        self.assertEqual(2, parsed.initial_branching)
        self.assertEqual(20, parsed.max_iterations)
        self.assertEqual(500, parsed.sample_size)
        self.assertEqual(80, parsed.payload_success_threshold)
        self.assertEqual(80, parsed.successful_case_ratio.target)
        self.assertEqual(2, parsed.successful_case_ratio.tolerance)
