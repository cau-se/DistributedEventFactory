"""Coordinates the ordered topology optimization phases."""

from dataclasses import dataclass
from typing import Dict

from distributed_event_factory.core.end_datasource import EndDataSource
from distributed_event_factory.topology.generator.topology_datasource_generator import TopologyDatasourceGenerator
from distributed_event_factory.topology.model.topology_graph import TopologyGraph
from distributed_event_factory.topology.model.topology_spec import TopologySpec
from distributed_event_factory.topology.optimizer.entropy_optimizer import (
    EntropyOptimizationResult,
    TraceEntropyOptimizer,
)
from distributed_event_factory.topology.optimizer.payload_optimizer import (
    PayloadOptimizationResult,
    PayloadOptimizer,
)
from distributed_event_factory.topology.optimizer.topology_optimizer import (
    TopologyOptimizationResult,
    TopologyOptimizer,
)


@dataclass(frozen=True)
class TopologyPipelineResult:
    graph: TopologyGraph
    datasources: Dict
    completed_payloads: Dict[str, float]
    transition: TopologyOptimizationResult
    trace_entropy: EntropyOptimizationResult
    payload: PayloadOptimizationResult


class TopologyPipeline:
    def __init__(
        self,
        datasource_generator: TopologyDatasourceGenerator,
        datasource_parser,
        topology_optimizer: TopologyOptimizer,
    ):
        self.datasource_generator = datasource_generator
        self.datasource_parser = datasource_parser
        self.topology_optimizer = topology_optimizer

    def run(self, spec: TopologySpec, simulate_fn) -> TopologyPipelineResult:
        spec.validate()
        transition_result = self.topology_optimizer.optimize(spec, simulate_fn)
        trace_entropy_result = TraceEntropyOptimizer().optimize(transition_result.best_graph, spec)
        payload_result = PayloadOptimizer().optimize(trace_entropy_result.graph, spec)
        graph = payload_result.graph

        events = simulate_fn(graph, spec.sample_size)
        end_activities = self.datasource_generator.build_end_activity_names(graph)
        completed_payloads = {
            event.caseid: event.payload
            for event in events
            if event.activity in end_activities
        }
        datasources = self.datasource_generator.build_datasource_objects(graph, self.datasource_parser)
        datasources["<end>"] = EndDataSource()

        return TopologyPipelineResult(
            graph=graph,
            datasources=datasources,
            completed_payloads=completed_payloads,
            transition=transition_result,
            trace_entropy=trace_entropy_result,
            payload=payload_result,
        )
