"""Ordered orchestration interface for topology optimization stages."""

from dataclasses import dataclass, field
from typing import List

from distributed_event_factory.topology_pipeline.model import ProcessModel
from distributed_event_factory.topology_pipeline.spec import TopologyPipelineSpec
from distributed_event_factory.topology_pipeline.stages import StageResult, TopologyOptimizationStage


@dataclass
class TopologyPipelineResult:
    """Final model and the ordered results of its optimization stages."""

    model: ProcessModel
    stage_results: List[StageResult] = field(default_factory=list)


@dataclass
class TopologyPipeline:
    """Runs stages in priority order, with earlier stage parameters frozen later."""

    stages: List[TopologyOptimizationStage] = field(default_factory=list)

    def run(self, initial_model: ProcessModel, spec: TopologyPipelineSpec) -> TopologyPipelineResult:
        # TODO: Run stages in the supplied priority order and preserve each earlier stage's owned parameters.
        pass
