"""
Unit tests for Graph Construction and Loading Module (FR-1).
"""

import os
import networkx as nx
import pytest
from src.graph_loader import (
    create_path_graph,
    create_cycle_graph,
    create_star_graph,
    create_complete_graph,
    create_disconnected_graph,
    create_erdos_renyi_graph,
    create_barabasi_albert_graph,
    create_karate_club_graph,
    create_dolphins_graph,
    load_edge_list_file,
    save_edge_list_file
)
from src.metrics import compute_graph_metrics


def test_reference_graphs():
    # Path P_5: 5 nodes, 4 edges
    p5 = create_path_graph(5)
    assert p5.number_of_nodes() == 5
    assert p5.number_of_edges() == 4

    # Cycle C_6: 6 nodes, 6 edges, 2-regular
    c6 = create_cycle_graph(6)
    assert c6.number_of_nodes() == 6
    assert c6.number_of_edges() == 6
    assert all(d == 2 for _, d in c6.degree())

    # Star S_5: 6 nodes (1 center + 5 outer), 5 edges
    s5 = create_star_graph(5)
    assert s5.number_of_nodes() == 6
    assert s5.number_of_edges() == 5
    assert s5.degree(0) == 5

    # Complete K_4: 4 nodes, 6 edges, 3-regular
    k4 = create_complete_graph(4)
    assert k4.number_of_nodes() == 4
    assert k4.number_of_edges() == 6
    assert all(d == 3 for _, d in k4.degree())


def test_disconnected_graph():
    G = create_disconnected_graph()
    metrics = compute_graph_metrics(G)
    assert metrics["num_nodes"] == 10
    assert metrics["num_edges"] == 10  # 6 (K4) + 3 (C3) + 1 (P2) + 0 (isolated)
    assert metrics["num_connected_components"] == 4


def test_synthetic_and_realworld():
    er = create_erdos_renyi_graph(50, 0.1, seed=42)
    assert er.number_of_nodes() == 50

    ba = create_barabasi_albert_graph(50, 3, seed=42)
    assert ba.number_of_nodes() == 50
    assert ba.number_of_edges() > 0

    karate = create_karate_club_graph()
    assert karate.number_of_nodes() == 34
    assert karate.number_of_edges() == 78

    dolphins = create_dolphins_graph()
    assert dolphins.number_of_nodes() == 62
    assert dolphins.number_of_edges() == 169


def test_save_and_load_edge_list(tmp_path):
    G = nx.Graph()
    G.add_edge("A", "B", weight=2.5, relationship_type="friend")
    G.add_edge("B", "C", weight=1.0, relationship_type="colleague")

    filepath = str(tmp_path / "test_edges.csv")
    save_edge_list_file(G, filepath)
    assert os.path.exists(filepath)

    loaded_G = load_edge_list_file(filepath)
    assert loaded_G.number_of_nodes() == 3
    assert loaded_G.number_of_edges() == 2
    assert loaded_G["A"]["B"]["weight"] == 2.5
    assert loaded_G["A"]["B"]["relationship_type"] == "friend"
