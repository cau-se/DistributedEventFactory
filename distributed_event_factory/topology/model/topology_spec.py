from dataclasses import dataclass


@dataclass(frozen=True)
class TopologyConstraint:
    target: int
    tolerance: int

    def lower(self) -> int:
        return self.target - self.tolerance

    def upper(self) -> int:
        return self.target + self.tolerance


@dataclass(frozen=True)
class TopologySpec:
    trace_length: TopologyConstraint
    distinct_traces: TopologyConstraint
    initial_branching: int
    max_iterations: int
    sample_size: int
