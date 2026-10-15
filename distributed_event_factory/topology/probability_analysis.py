"""Probability and entropy calculations shared by topology optimizers."""

from math import log

from distributed_event_factory.topology.model.topology_graph import TopologyGraph


def final_payload_distribution(graph: TopologyGraph) -> dict:
    states = {}
    for node in graph.successors("<start>"):
        for index in range(1, graph.transition_count("<start>", node) + 1):
            probability = graph.transition_probability("<start>", node, index)
            states[(node, 0)] = states.get((node, 0), 0.0) + probability

    final_distribution = {}
    nodes = sorted(
        (node for node in graph.nodes if node not in {"<start>", "<end>"}),
        key=lambda node: graph.nodes[node].level,
    )
    for node in nodes:
        node_states = [
            (payload, probability)
            for (state_node, payload), probability in states.items()
            if state_node == node
        ]
        for dst in graph.successors(node):
            for index in range(1, graph.transition_count(node, dst) + 1):
                transition_probability = graph.transition_probability(node, dst, index)
                delta = graph.payload_delta(node, dst, index)
                for payload, probability in node_states:
                    final_payload = min(100, payload + delta)
                    path_probability = probability * transition_probability
                    if dst == "<end>":
                        final_distribution[final_payload] = (
                            final_distribution.get(final_payload, 0.0) + path_probability
                        )
                    else:
                        state = (dst, final_payload)
                        states[state] = states.get(state, 0.0) + path_probability
    return final_distribution


def expected_payload_contributions(graph: TopologyGraph) -> dict:
    states = {}
    contributions = {}
    for node in graph.successors("<start>"):
        for index in range(1, graph.transition_count("<start>", node) + 1):
            states[(node, 0)] = states.get((node, 0), 0.0) + graph.transition_probability(
                "<start>", node, index
            )

    nodes = sorted(
        (node for node in graph.nodes if node not in {"<start>", "<end>"}),
        key=lambda node: graph.nodes[node].level,
    )
    for node in nodes:
        node_states = [
            (payload, probability)
            for (state_node, payload), probability in states.items()
            if state_node == node
        ]
        for dst in graph.successors(node):
            for index in range(1, graph.transition_count(node, dst) + 1):
                transition_probability = graph.transition_probability(node, dst, index)
                delta = graph.payload_delta(node, dst, index)
                key = (node, dst, index)
                for payload, probability in node_states:
                    path_probability = probability * transition_probability
                    effective_delta = min(delta, 100 - payload)
                    contributions[key] = contributions.get(key, 0.0) + path_probability * effective_delta
                    if dst != "<end>":
                        state = (dst, min(100, payload + delta))
                        states[state] = states.get(state, 0.0) + path_probability
    return contributions


def normalized_payload_entropy(graph: TopologyGraph) -> float:
    contributions_by_step = {}
    for (src, _, _), contribution in expected_payload_contributions(graph).items():
        contributions_by_step[src] = contributions_by_step.get(src, 0.0) + contribution
    values = [value for value in contributions_by_step.values() if value > 0]
    return normalized_entropy(values)


def normalized_entropy(values) -> float:
    total = sum(values)
    if total <= 0 or len(values) <= 1:
        return 0.0
    probabilities = [value / total for value in values]
    entropy = -sum(probability * log(probability) for probability in probabilities)
    return entropy / log(len(probabilities))


def normalized_trace_entropy(graph: TopologyGraph) -> float:
    nodes = sorted(graph.nodes.values(), key=lambda node: (node.level, node.name))
    reach_probability = {"<start>": 1.0}
    path_counts = {"<end>": 1}

    for node in reversed(nodes):
        if node.name == "<end>":
            continue
        path_counts[node.name] = sum(
            graph.transition_count(node.name, dst) * path_counts.get(dst, 0)
            for dst in graph.successors(node.name)
        )

    entropy = 0.0
    for node in nodes:
        if node.name == "<end>":
            continue
        probabilities = [
            graph.transition_probability(node.name, dst, index)
            for dst in graph.successors(node.name)
            for index in range(1, graph.transition_count(node.name, dst) + 1)
        ]
        entropy -= reach_probability.get(node.name, 0.0) * sum(
            probability * log(probability)
            for probability in probabilities
            if probability > 0
        )
        for dst in graph.successors(node.name):
            edge_probability = sum(
                graph.transition_probability(node.name, dst, index)
                for index in range(1, graph.transition_count(node.name, dst) + 1)
            )
            reach_probability[dst] = (
                reach_probability.get(dst, 0.0)
                + reach_probability.get(node.name, 0.0) * edge_probability
            )

    variant_count = path_counts.get("<start>", 0)
    max_entropy = log(variant_count) if variant_count > 1 else 0.0
    return entropy / max_entropy if max_entropy > 0 else 0.0


def most_likely_trace_probability(graph: TopologyGraph) -> float:
    probabilities = {"<start>": 1.0}
    nodes = sorted(graph.nodes.values(), key=lambda node: (node.level, node.name))
    for node in nodes:
        if node.name not in probabilities:
            continue
        for dst in graph.successors(node.name):
            for index in range(1, graph.transition_count(node.name, dst) + 1):
                path_probability = probabilities[node.name] * graph.transition_probability(node.name, dst, index)
                probabilities[dst] = max(probabilities.get(dst, 0.0), path_probability)
    return probabilities.get("<end>", 0.0)
