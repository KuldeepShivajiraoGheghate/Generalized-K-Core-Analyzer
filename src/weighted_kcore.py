"""
Weighted K-Core Decomposition Module (FR-8).
Implements strength-based core decomposition for graphs with positive real-valued edge weights.
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import networkx as nx
import numpy as np


def compute_node_strengths(graph: nx.Graph, weight_attr: str = "weight") -> Dict[Any, float]:
    """
    Computes node strength s(u) = sum_{v in N(u)} w(u, v).

    Parameters:
        graph: Input networkx.Graph.
        weight_attr: Edge attribute name representing weight (default: 'weight').

    Returns:
        Dict mapping node -> float strength.
    """
    strengths: Dict[Any, float] = {}
    for node in graph.nodes():
        s = sum(data.get(weight_attr, 1.0) for _, _, data in graph.edges(node, data=True))
        strengths[node] = round(float(s), 6)
    return strengths


def compute_weighted_kcore_subgraph(
    graph: nx.Graph,
    threshold_weight: float,
    weight_attr: str = "weight"
) -> Tuple[nx.Graph, List[Any]]:
    """
    Decomposes the graph by iteratively removing vertices with strength s(v) < threshold_weight.

    Algorithm:
    1. Calculate initial vertex strengths s(v).
    2. Queue all vertices with s(v) < threshold_weight.
    3. While queue is not empty:
       - Dequeue vertex v.
       - For each active neighbor u of v, subtract w(u, v) from s(u).
       - If s(u) < threshold_weight and u is not yet queued, enqueue u.
    4. Return induced subgraph on surviving vertices and removal sequence.

    Parameters:
        graph: Input networkx.Graph.
        threshold_weight: Float strength threshold (k_w).
        weight_attr: Edge attribute name for weights.

    Returns:
        (subgraph, removal_order)
    """
    if threshold_weight <= 0:
        return graph.copy(), []

    # Map adjacency with weights
    adj_weights: Dict[Any, Dict[Any, float]] = {}
    for node in graph.nodes():
        adj_weights[node] = {}
        for nbr, data in graph[node].items():
            adj_weights[node][nbr] = float(data.get(weight_attr, 1.0))

    strengths: Dict[Any, float] = {u: sum(adj_weights[u].values()) for u in adj_weights}
    
    removal_order: List[Any] = []
    removed_set: Set[Any] = set()

    queue = [u for u, s in strengths.items() if s < threshold_weight]
    queued_set = set(queue)

    while queue:
        curr = queue.pop(0)
        removal_order.append(curr)
        removed_set.add(curr)

        for nbr, w in adj_weights[curr].items():
            if nbr not in removed_set:
                strengths[nbr] -= w
                if strengths[nbr] < threshold_weight and nbr not in queued_set:
                    queue.append(nbr)
                    queued_set.add(nbr)

    surviving_nodes = [u for u in graph.nodes() if u not in removed_set]
    subgraph = graph.subgraph(surviving_nodes).copy()
    return subgraph, removal_order


def compute_weighted_core_numbers(
    graph: nx.Graph,
    step_size: float = 1.0,
    weight_attr: str = "weight"
) -> Dict[Any, float]:
    """
    Computes generalized weighted core numbers by incrementing threshold_weight
    in discrete steps from 1.0 up to maximum vertex strength.

    Parameters:
        graph: Input networkx.Graph.
        step_size: Granularity of the strength threshold sweep.
        weight_attr: Edge attribute name.

    Returns:
        Dict mapping node -> maximum weighted strength threshold survived.
    """
    if graph.number_of_nodes() == 0:
        return {}

    strengths = compute_node_strengths(graph, weight_attr=weight_attr)
    max_strength = max(strengths.values()) if strengths else 0.0

    weighted_cores: Dict[Any, float] = {node: 0.0 for node in graph.nodes()}
    current_subgraph = graph.copy()

    threshold = step_size
    while threshold <= max_strength + step_size and current_subgraph.number_of_nodes() > 0:
        sub, _ = compute_weighted_kcore_subgraph(current_subgraph, threshold, weight_attr=weight_attr)
        for node in sub.nodes():
            weighted_cores[node] = round(threshold, 2)
        current_subgraph = sub
        threshold += step_size

    return weighted_cores


def compare_unweighted_vs_weighted_cores(
    graph: nx.Graph,
    unweighted_cores: Dict[Any, int],
    weighted_cores: Dict[Any, float]
) -> List[Dict[str, Any]]:
    """
    Compares the unweighted vs weighted core rankings across all nodes,
    measuring rank shifts induced by heterogeneous edge weights.

    Returns:
        List of comparison records per node.
    """
    strengths = compute_node_strengths(graph)
    comparison = []
    
    for node in graph.nodes():
        deg = graph.degree(node)
        s = strengths.get(node, 0.0)
        c_unw = unweighted_cores.get(node, 0)
        c_w = weighted_cores.get(node, 0.0)

        comparison.append({
            "node": node,
            "degree": deg,
            "strength": s,
            "unweighted_core": c_unw,
            "weighted_core": c_w,
            "is_shifted": (c_unw != int(c_w))
        })
        
    return sorted(comparison, key=lambda x: str(x["node"]))
