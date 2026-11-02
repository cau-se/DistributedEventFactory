from dataclasses import dataclass
from statistics import mean
from typing import Dict, List, Tuple

from distributed_event_factory.topology.model.topology_spec import TopologySpec


@dataclass(frozen=True)
class TopologyMetrics:
    avg_trace_length: float
    min_trace_length: int
    max_trace_length: int
    traces_in_length_interval_ratio: float
    distinct_traces_count: int


@dataclass(frozen=True)
class TopologyScore:
    total: float
    trace_length_penalty: float
    distinct_traces_penalty: float
    is_within_target: bool


class TopologyEvaluator:
    def extract_traces(self, events: List) -> Dict[str, List[str]]:
        traces: Dict[str, List[Tuple[str, str]]] = {}
        for event in events:
            traces.setdefault(event.caseid, []).append((event.timestamp, event.activity))

        ordered_traces: Dict[str, List[str]] = {}
        for case_id, event_pairs in traces.items():
            sorted_pairs = sorted(event_pairs, key=lambda pair: pair[0])
            ordered_traces[case_id] = [activity for _, activity in sorted_pairs]
        return ordered_traces

    def compute_metrics(self, traces: Dict[str, List[str]], spec: TopologySpec) -> TopologyMetrics:
        if len(traces) == 0:
            return TopologyMetrics(
                avg_trace_length=0.0,
                min_trace_length=0,
                max_trace_length=0,
                traces_in_length_interval_ratio=0.0,
                distinct_traces_count=0
            )

        lengths = [len(trace) for trace in traces.values()]
        lower = spec.trace_length.lower()
        upper = spec.trace_length.upper()
        traces_within_bounds = [trace_len for trace_len in lengths if lower <= trace_len <= upper]

        distinct_signatures = set(tuple(trace) for trace in traces.values())

        return TopologyMetrics(
            avg_trace_length=mean(lengths),
            min_trace_length=min(lengths),
            max_trace_length=max(lengths),
            traces_in_length_interval_ratio=len(traces_within_bounds) / len(lengths),
            distinct_traces_count=len(distinct_signatures)
        )

    def score(self, metrics: TopologyMetrics, spec: TopologySpec) -> TopologyScore:
        trace_penalty = self._interval_penalty(
            observed=int(round(metrics.avg_trace_length)),
            target=spec.trace_length.target,
            tolerance=spec.trace_length.tolerance
        )

        if metrics.traces_in_length_interval_ratio < 1.0:
            trace_penalty += (1.0 - metrics.traces_in_length_interval_ratio) * max(1, spec.trace_length.target)

        distinct_penalty = self._interval_penalty(
            observed=metrics.distinct_traces_count,
            target=spec.distinct_traces.target,
            tolerance=spec.distinct_traces.tolerance
        )

        total = 2.0 * trace_penalty + distinct_penalty

        return TopologyScore(
            total=total,
            trace_length_penalty=trace_penalty,
            distinct_traces_penalty=distinct_penalty,
            is_within_target=(trace_penalty == 0 and distinct_penalty == 0)
        )

    @staticmethod
    def _interval_penalty(observed: int, target: int, tolerance: int) -> float:
        lower = target - tolerance
        upper = target + tolerance
        if lower <= observed <= upper:
            return 0.0
        if observed < lower:
            return float(lower - observed)
        return float(observed - upper)
