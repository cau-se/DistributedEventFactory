"""Stage interfaces and parameter ownership for topology optimization."""

from dataclasses import dataclass, field
from typing import Dict

from distributed_event_factory.topology_pipeline.model import ProcessModel
from distributed_event_factory.topology_pipeline.spec import TopologyPipelineSpec


@dataclass
class StageResult:
    """Model and measured metrics produced by one optimization stage."""

    model: ProcessModel
    metrics: Dict[str, float] = field(default_factory=dict)


class TopologyOptimizationStage:
    """Interface for a stage that owns one independent parameter group."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Define the common execution contract for a stage and return its optimized model and metrics.
        pass


class LayerCountStage(TopologyOptimizationStage):
    """Owns the number and placement of event-producing process layers."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Create the target number of layers, with one event-producing step per layer.
        pass


class ProcessVariantStage(TopologyOptimizationStage):
    """Owns process connections and the set of allowed process variants."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Change transitions to reach the target count of possible process paths.
        pass


class VariantProbabilityStage(TopologyOptimizationStage):
    """Owns transition probabilities while preserving the allowed process paths."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Tune probabilities to reach normalized Shannon entropy over process variants.
        pass


class DurationStage(TopologyOptimizationStage):
    """Owns event durations while preserving process structure and probabilities."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Tune step durations to reach the target average total duration per trace.
        pass


class PayloadStage(TopologyOptimizationStage):
    """Owns payload changes while preserving all earlier stage parameters."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Tune per-step payload deltas to reach the target successful-trace ratio.
        pass


class DatasourceAssignmentStage(TopologyOptimizationStage):
    """Owns data-source assignments without changing process paths."""

    def optimize(self, model: ProcessModel, spec: TopologyPipelineSpec) -> StageResult:
        # TODO: Assign data sources to steps to reach the average distinct sources per case target.
        pass
