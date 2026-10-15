from distributed_event_factory.parser.parser import Parser
from distributed_event_factory.topology.model.topology_spec import TopologyConstraint, TopologySpec


class TopologyParser(Parser):
    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        constraints = config["constraints"]
        generation = config["generation"]
        optimize = config["optimize"]
        payload = config.get("payload", {})
        successful_case_ratio = payload.get("successfulCaseRatio", {})
        payload_entropy = payload.get("entropy", {})
        trace_entropy = config.get("traceEntropy", config.get("trace_entropy", {}))

        topology_spec = TopologySpec(
            trace_length=TopologyConstraint(
                target=constraints["traceLength"]["target"],
                tolerance=constraints["traceLength"]["tolerance"]
            ),
            distinct_traces=TopologyConstraint(
                target=constraints["distinctTraces"]["target"],
                tolerance=constraints["distinctTraces"]["tolerance"]
            ),
            initial_branching=generation["initialBranching"],
            max_iterations=optimize["maxIterations"],
            sample_size=optimize["sampleSize"],
            payload_success_threshold=payload.get("successThreshold", 80),
            successful_case_ratio=TopologyConstraint(
                target=successful_case_ratio.get("target", 80),
                tolerance=successful_case_ratio.get("tolerance", 2),
            ),
            payload_entropy=TopologyConstraint(
                target=payload_entropy.get("target", 0.7),
                tolerance=payload_entropy.get("tolerance", 0.1),
            ),
            trace_entropy=TopologyConstraint(
                target=trace_entropy.get("target", 1.0),
                tolerance=trace_entropy.get("tolerance", 0.1),
            ),
        )
        topology_spec.validate()
        return topology_spec
