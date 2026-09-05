"""
Unit tests to verify topological invariants and ground-truth values of Phase 2 reference graphs.
"""

import pytest
import networkx as nx
from tests.reference_graphs import REFERENCE_GRAPHS, build_adj_list


def test_handshaking_lemma_and_degrees():
    """Verify sum of degrees = 2 * |E| and degree values match ground truth."""
    for name, data in REFERENCE_GRAPHS.items():
        nodes = data["nodes"]
        edges = data["edges"]
        expected_degrees = data["degrees"]
        expected_node_count = data["node_count"]
        expected_edge_count = data["edge_count"]
        
        assert len(nodes) == expected_node_count, f"Node count mismatch for {name}"
        assert len(edges) == expected_edge_count, f"Edge count mismatch for {name}"
        
        adj = build_adj_list(nodes, edges)
        computed_degrees = {u: len(adj[u]) for u in nodes}
        
        # Check degree sequence
        assert computed_degrees == expected_degrees, f"Degree mismatch for {name}"
        
        # Euler's Handshaking Lemma: sum(deg) = 2 * |E|
        sum_deg = sum(computed_degrees.values())
        assert sum_deg == 2 * len(edges), f"Handshaking lemma violated for {name}"
        
        # Min/Max/Avg Degree
        assert min(computed_degrees.values()) == data["min_degree"]
        assert max(computed_degrees.values()) == data["max_degree"]
        assert pytest.approx(sum_deg / len(nodes)) == data["avg_degree"]


def test_connected_components_and_reference_networkx():
    """Verify connected components and graph topology against NetworkX baseline."""
    for name, data in REFERENCE_GRAPHS.items():
        G = nx.Graph()
        G.add_nodes_from(data["nodes"])
        G.add_edges_from(data["edges"])
        
        # Component count
        num_components = nx.number_connected_components(G)
        assert num_components == data["connected_components"], f"Component count mismatch for {name}"
        
        # NetworkX ground-truth core numbers vs our hand calculations
        nx_core_numbers = nx.core_number(G)
        assert nx_core_numbers == data["core_numbers"], (
            f"Hand-calculated core numbers mismatch with NetworkX oracle for {name}. "
            f"Hand: {data['core_numbers']}, NX: {nx_core_numbers}"
        )
        
        # Degeneracy
        assert max(nx_core_numbers.values() if nx_core_numbers else [0]) == data["degeneracy"]


def test_theoretical_k_core_subgraphs():
    """Verify hand-calculated k-core subgraphs for all k."""
    for name, data in REFERENCE_GRAPHS.items():
        G = nx.Graph()
        G.add_nodes_from(data["nodes"])
        G.add_edges_from(data["edges"])
        
        for k, expected_subgraph_nodes in data["k_cores"].items():
            nx_kcore = nx.k_core(G, k=k)
            actual_subgraph_nodes = sorted(list(nx_kcore.nodes()))
            expected_sorted = sorted(expected_subgraph_nodes)
            assert actual_subgraph_nodes == expected_sorted, (
                f"K-core mismatch for graph '{name}' at k={k}. "
                f"Expected {expected_sorted}, got {actual_subgraph_nodes}"
            )
