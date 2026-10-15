"""Data structures shared by the topology pipeline stages."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ProcessStep:
    """An event-producing process step, independent of its data source."""

    step_id: str
    layer: int
    duration: Optional[float] = None
    payload_delta: Optional[float] = None


@dataclass
class Transition:
    """A directed connection between process steps."""

    source_step_id: str
    target_step_id: str
    probability: Optional[float] = None


@dataclass(frozen=True)
class DataSourceAssignment:
    """Assignment of a data source to a process step."""

    step_id: str
    datasource_id: str


@dataclass
class ProcessModel:
    """Process structure and its separately configurable event attributes."""

    steps: Dict[str, ProcessStep] = field(default_factory=dict)
    transitions: List[Transition] = field(default_factory=list)
    datasource_assignments: List[DataSourceAssignment] = field(default_factory=list)
