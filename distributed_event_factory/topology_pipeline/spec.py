"""Target values for the staged topology optimization pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizationTarget:
    """A target value and its accepted absolute tolerance."""

    target: float
    tolerance: float


@dataclass(frozen=True)
class TopologyPipelineSpec:
    """Targets and simulation settings for one pipeline run.

    The layer-count target is also the initial case-length target because v1
    emits exactly one event from every visited layer. Variant entropy is the
    normalized Shannon entropy over process variants. Duration targets the
    average total duration per trace. Payload success is the share of traces
    whose final payload is above ``payload_success_threshold``. The data-source
    target is the average number of distinct data sources per case.
    """

    layer_count: OptimizationTarget
    variant_count: OptimizationTarget
    variant_entropy: OptimizationTarget
    average_trace_duration: OptimizationTarget
    successful_trace_ratio: OptimizationTarget
    payload_success_threshold: float
    datasources_per_case: OptimizationTarget
    sample_size: int
