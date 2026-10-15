from dataclasses import dataclass, field
@dataclass(frozen=True)
class TopologyConstraint:
    target: float
    tolerance: float

    def lower(self) -> float:
        return self.target - self.tolerance

    def upper(self) -> float:
        return self.target + self.tolerance


@dataclass(frozen=True)
class TopologySpec:
    trace_length: TopologyConstraint
    distinct_traces: TopologyConstraint
    initial_branching: int
    max_iterations: int
    sample_size: int
    payload_success_threshold: int = 80
    successful_case_ratio: TopologyConstraint = field(
        default_factory=lambda: TopologyConstraint(target=80, tolerance=2)
    )
    trace_entropy: TopologyConstraint = field(
        default_factory=lambda: TopologyConstraint(target=1.0, tolerance=0.1)
    )
    payload_entropy: TopologyConstraint = field(
        default_factory=lambda: TopologyConstraint(target=0.7, tolerance=0.1)
    )

    def validate(self) -> None:
        for name, constraint in (
            ("trace_length", self.trace_length),
            ("distinct_traces", self.distinct_traces),
            ("successful_case_ratio", self.successful_case_ratio),
            ("trace_entropy", self.trace_entropy),
            ("payload_entropy", self.payload_entropy),
        ):
            if constraint.tolerance < 0:
                raise ValueError(f"{name} tolerance must be non-negative")
        for name, constraint in (("trace_entropy", self.trace_entropy), ("payload_entropy", self.payload_entropy)):
            if not 0.0 <= constraint.target <= 1.0:
                raise ValueError(f"{name} target must be between 0 and 1")
            if constraint.tolerance > 1.0:
                raise ValueError(f"{name} tolerance must not exceed 1")
        if not 0 <= self.payload_success_threshold <= 100:
            raise ValueError("payload success threshold must be between 0 and 100")
