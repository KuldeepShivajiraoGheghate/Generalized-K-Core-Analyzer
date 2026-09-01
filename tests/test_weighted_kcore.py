"""
Unit tests for Weighted K-Core Decomposition (FR-8).
"""

import networkx as nx
import pytest
from src.weighted_kcore import (
    compute_node_strengths,
    compute_weighted_kcore_subgraph,
    compute_weighted_core_numbers,
    compare_unweighted_vs_weighted_cores
)
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik


def test_node_strengths():
    G = nx.Graph()
    G.add_edge(0, 1, weight=3.5)
    G.add_edge(0, 2, weight=1.5)
    G.add_edge(1, 2, weight=2.0)

    strengths = compute_node_strengths(G)
    assert strengths[0] == 5.0
    assert strengths[1] == 5.5
    assert strengths[2] == 3.5


def test_weighted_peeling():
    # Triangle with weights: (0,1)=5.0, (1,2)=5.0, (0,2)=1.0
    # Strengths: 0 -> 6.0, 1 -> 10.0, 2 -> 6.0
    G = nx.Graph()
    G.add_edge(0, 1, weight=5.0)
    G.add_edge(1, 2, weight=5.0)
    G.add_edge(0, 2, weight=1.0)

    # Threshold 5.0: all have strength >= 5.0 -> all 3 survive
    sub5, removed5 = compute_weighted_kcore_subgraph(G, 5.0)
    assert sub5.number_of_nodes() == 3

    # Threshold 7.0: nodes 0 and 2 have strength 6.0 < 7.0, queued for removal.
    # Removing 0 and 2 reduces strength of node 1 to 0.0 < 7.0, which also gets removed.
    sub7, removed7 = compute_weighted_kcore_subgraph(G, 7.0)
    assert sub7.number_of_nodes() == 0
    assert len(removed7) == 3


def test_weighted_core_shift():
    # Construct graph where unweighted degree is uniform (cycle C_4, degree=2 for all),
    # but weights make edge (0,1) heavy (weight=10.0) while others are weight=1.0
    G = nx.cycle_graph(4)
    G[0][1]["weight"] = 10.0
    G[1][2]["weight"] = 1.0
    G[2][3]["weight"] = 1.0
    G[3][0]["weight"] = 1.0

    unw_cores = compute_core_numbers_batagelj_zaversnik(G)
    w_cores = compute_weighted_core_numbers(G, step_size=1.0)

    comparison = compare_unweighted_vs_weighted_cores(G, unw_cores, w_cores)
    assert len(comparison) == 4
    # Nodes 0 and 1 have higher weighted core than nodes 2 and 3
    assert w_cores[0] > w_cores[2]
    assert w_cores[1] > w_cores[3]
