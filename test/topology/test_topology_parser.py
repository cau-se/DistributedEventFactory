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
                "successfulCaseRatio": {"target": 80, "tolerance": 2},
                "entropy": {"target": 0.7, "tolerance": 0.1},
            },
            "traceEntropy": {
                "target": 0.7,
                "tolerance": 0.1
            },
            "duration": {
                "averageTraceDuration": {"target": 120, "tolerance": 5},
                "entropy": {"target": 0.65, "tolerance": 0.1},
                "maxPerTransition": 45,
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
        self.assertEqual(0.7, parsed.payload_entropy.target)
        self.assertEqual(0.1, parsed.payload_entropy.tolerance)
        self.assertEqual(0.7, parsed.trace_entropy.target)
        self.assertEqual(0.1, parsed.trace_entropy.tolerance)
        self.assertEqual(120, parsed.average_trace_duration.target)
        self.assertEqual(5, parsed.average_trace_duration.tolerance)
        self.assertEqual(0.65, parsed.duration_entropy.target)
        self.assertEqual(0.1, parsed.duration_entropy.tolerance)
        self.assertEqual(45, parsed.max_duration_per_transition)

    def test_trace_entropy_defaults_to_uniform(self):
        parsed = TopologyParser().parse({
            "constraints": {
                "traceLength": {"target": 3, "tolerance": 0},
                "distinctTraces": {"target": 8, "tolerance": 0},
            },
            "generation": {"initialBranching": 2},
            "optimize": {"maxIterations": 5, "sampleSize": 100},
        })

        self.assertEqual(1.0, parsed.trace_entropy.target)
        self.assertEqual(0.1, parsed.trace_entropy.tolerance)
        self.assertEqual(0.7, parsed.payload_entropy.target)
        self.assertEqual(0.1, parsed.payload_entropy.tolerance)
        self.assertEqual(3, parsed.average_trace_duration.target)
        self.assertEqual(60, parsed.max_duration_per_transition)
