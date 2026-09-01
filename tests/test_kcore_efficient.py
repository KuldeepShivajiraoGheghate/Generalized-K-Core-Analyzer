"""
Unit tests for Efficient Batagelj-Zaversnik O(V+E) K-Core Decomposition (FR-3 & FR-4).
Asserts exact node-by-node equivalence against NetworkX reference oracle.
"""

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
    create_dolphins_graph
)
from src.kcore_efficient import (
    compute_core_numbers_batagelj_zaversnik,
    validate_against_networkx,
    extract_kcore_subgraph
)


def test_empty_and_isolated_efficient():
    G_empty = nx.Graph()
    assert compute_core_numbers_batagelj_zaversnik(G_empty) == {}

    G_single = nx.Graph()
    G_single.add_node(0)
    assert compute_core_numbers_batagelj_zaversnik(G_single) == {0: 0}


def test_validation_on_all_reference_topologies():
    graphs = [
        ("Path_5", create_path_graph(5)),
        ("Cycle_6", create_cycle_graph(6)),
        ("Star_7", create_star_graph(7)),
        ("Complete_5", create_complete_graph(5)),
        ("Disconnected", create_disconnected_graph())
    ]

    for name, G in graphs:
        is_valid, report = validate_against_networkx(G)
        assert is_valid, f"Validation failure on {name}: {report}"


def test_validation_on_synthetic_networks():
    # Erdős-Rényi
    G_er = create_erdos_renyi_graph(n=100, p=0.08, seed=42)
    is_valid, report = validate_against_networkx(G_er)
    assert is_valid, f"Validation failure on Erdős-Rényi: {report}"

    # Barabási-Albert
    G_ba = create_barabasi_albert_graph(n=150, m=3, seed=42)
    is_valid, report = validate_against_networkx(G_ba)
    assert is_valid, f"Validation failure on Barabási-Albert: {report}"


def test_validation_on_realworld_networks():
    # Zachary Karate Club
    G_karate = create_karate_club_graph()
    is_valid, report = validate_against_networkx(G_karate)
    assert is_valid, f"Validation failure on Karate Club: {report}"

    # Dolphins Social Network
    G_dolphins = create_dolphins_graph()
    is_valid, report = validate_against_networkx(G_dolphins)
    assert is_valid, f"Validation failure on Dolphins: {report}"


def test_extract_kcore_subgraph():
    G = create_complete_graph(5)
    cores = compute_core_numbers_batagelj_zaversnik(G)
    sub = extract_kcore_subgraph(G, cores, k=4)
    assert sub.number_of_nodes() == 5
    assert sub.number_of_edges() == 10

    sub_empty = extract_kcore_subgraph(G, cores, k=5)
    assert sub_empty.number_of_nodes() == 0
