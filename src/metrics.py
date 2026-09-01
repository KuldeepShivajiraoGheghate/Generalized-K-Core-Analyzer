"""
Graph Analytics and Coreness Metrics Module.
Provides descriptive statistics for topological graph structures and k-core decompositions.
"""

from typing import Dict, Any, List, Set
import networkx as nx
import numpy as np


def compute_graph_metrics(graph: nx.Graph) -> Dict[str, Any]:
    """
    Computes global topological metrics for an undirected graph.

    Parameters:
        graph: networkx.Graph object.

    Returns:
        Dictionary containing node count, edge count, density, degree statistics,
        and connected component count.
    """
    n_nodes = graph.number_of_nodes()
    n_edges = graph.number_of_edges()
    
    if n_nodes == 0:
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "density": 0.0,
            "min_degree": 0,
            "max_degree": 0,
            "avg_degree": 0.0,
            "num_connected_components": 0,
            "degree_sequence": []
        }

    degrees = [d for _, d in graph.degree()]
    density = nx.density(graph) if n_nodes > 1 else 0.0
    num_cc = nx.number_connected_components(graph)

    return {
        "num_nodes": n_nodes,
        "num_edges": n_edges,
        "density": round(float(density), 6),
        "min_degree": int(np.min(degrees)) if degrees else 0,
        "max_degree": int(np.max(degrees)) if degrees else 0,
        "avg_degree": round(float(np.mean(degrees)), 4) if degrees else 0.0,
        "num_connected_components": num_cc,
        "degree_sequence": sorted(degrees, reverse=True)
    }


def compute_core_distribution(core_numbers: Dict[Any, int]) -> Dict[int, int]:
    """
    Computes the frequency distribution of core numbers (k-shells).

    Parameters:
        core_numbers: Dict mapping node -> core number.

    Returns:
        Dict mapping core level k -> number of nodes with c(v) == k.
    """
    distribution: Dict[int, int] = {}
    for node, k in core_numbers.items():
        distribution[k] = distribution.get(k, 0) + 1
    return dict(sorted(distribution.items()))


def compute_degeneracy(core_numbers: Dict[Any, int]) -> int:
    """
    Computes graph degeneracy: k_max = max_{v} c(v).

    Parameters:
        core_numbers: Dict mapping node -> core number.

    Returns:
        Maximum core number (degeneracy) of the graph.
    """
    if not core_numbers:
        return 0
    return max(core_numbers.values())


def summarize_kcore_stats(graph: nx.Graph, core_numbers: Dict[Any, int]) -> Dict[str, Any]:
    """
    Produces a consolidated summary of graph metrics and core decomposition stats.

    Parameters:
        graph: networkx.Graph object.
        core_numbers: Dict mapping node -> core number.

    Returns:
        Dictionary with combined structural and core metrics.
    """
    metrics = compute_graph_metrics(graph)
    degeneracy = compute_degeneracy(core_numbers)
    distribution = compute_core_distribution(core_numbers)
    
    core_vals = list(core_numbers.values())
    avg_core = float(np.mean(core_vals)) if core_vals else 0.0
    
    metrics.update({
        "degeneracy": degeneracy,
        "avg_core_number": round(avg_core, 4),
        "core_distribution": distribution,
    })
    return metrics
