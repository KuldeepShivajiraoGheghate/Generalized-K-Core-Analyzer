"""
Unit tests for Naive Static K-Core Decomposition (FR-2).
Validates naive iterative peeling against hand-calculated analytical solutions.
"""

import networkx as nx
import pytest
from src.graph_loader import (
    create_path_graph,
    create_cycle_graph,
    create_star_graph,
    create_complete_graph,
    create_disconnected_graph
)
from src.kcore_basic import compute_kcore_subgraph_naive, compute_core_numbers_naive


def test_empty_and_single_node():
    G_empty = nx.Graph()
    assert compute_core_numbers_naive(G_empty) == {}

    G_single = nx.Graph()
    G_single.add_node(0)
    assert compute_core_numbers_naive(G_single) == {0: 0}


def test_path_graph_naive():
    # In any path P_n (n >= 2), degree of endpoints is 1, internal nodes 2.
    # For k=1: all nodes survive (1-core).
    # For k=2: endpoints peeled, triggering cascade that deletes all nodes. 2-core is empty.
    p5 = create_path_graph(5)
    cores = compute_core_numbers_naive(p5)
    assert all(c == 1 for c in cores.values())

    sub2, removed = compute_kcore_subgraph_naive(p5, 2)
    assert sub2.number_of_nodes() == 0
    assert len(removed) == 5


def test_cycle_graph_naive():
    # In any cycle C_n, every node has degree 2.
    # For k=1 and k=2: all nodes survive.
    # For k=3: empty.
    c5 = create_cycle_graph(5)
    cores = compute_core_numbers_naive(c5)
    assert all(c == 2 for c in cores.values())

    sub2, _ = compute_kcore_subgraph_naive(c5, 2)
    assert sub2.number_of_nodes() == 5

    sub3, _ = compute_kcore_subgraph_naive(c5, 3)
    assert sub3.number_of_nodes() == 0


def test_star_graph_naive():
    # Star S_5: center degree 5, 5 leaves degree 1.
    # For k=1: all survive.
    # For k=2: all 5 leaves removed, leaving isolated center with degree 0, which also gets removed.
    # All nodes have core number 1.
    s5 = create_star_graph(5)
    cores = compute_core_numbers_naive(s5)
    assert all(c == 1 for c in cores.values())


def test_complete_graph_naive():
    # Complete K_5: 5 nodes, every node has degree 4.
    # Core number of every node is 4.
    k5 = create_complete_graph(5)
    cores = compute_core_numbers_naive(k5)
    assert all(c == 4 for c in cores.values())

    sub4, _ = compute_kcore_subgraph_naive(k5, 4)
    assert sub4.number_of_nodes() == 5

    sub5, _ = compute_kcore_subgraph_naive(k5, 5)
    assert sub5.number_of_nodes() == 0


def test_disconnected_graph_naive():
    # Component 1 (K4): nodes 0,1,2,3 -> core 3
    # Component 2 (C3): nodes 4,5,6 -> core 2
    # Component 3 (P2): nodes 7,8 -> core 1
    # Component 4 (isolated): node 9 -> core 0
    G = create_disconnected_graph()
    cores = compute_core_numbers_naive(G)
    for n in [0, 1, 2, 3]:
        assert cores[n] == 3
    for n in [4, 5, 6]:
        assert cores[n] == 2
    for n in [7, 8]:
        assert cores[n] == 1
    assert cores[9] == 0
