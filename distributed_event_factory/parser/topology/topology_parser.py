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

        return TopologySpec(
            trace_length=TopologyConstraint(
                target=constraints["traceLength"]["target"],
                tolerance=constraints["traceLength"]["tolerance"]
            ),
            distinct_traces=TopologyConstraint(
                target=constraints["distinctTraces"]["target"],
                tolerance=constraints["distinctTraces"]["tolerance"]
            ),
            initial_datasource_count=generation["initialDatasourceCount"],
            initial_branching=generation["initialBranching"],
            max_iterations=optimize["maxIterations"],
            sample_size=optimize["sampleSize"]
        )
