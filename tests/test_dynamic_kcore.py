"""
Unit and Equivalence tests for Dynamic Updates and Incremental K-Core Maintenance (FR-5, FR-6, FR-7).
"""

import random
import networkx as nx
import pytest
from src.graph_loader import create_karate_club_graph, create_erdos_renyi_graph, create_path_graph
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik
from src.dynamic_kcore import (
    add_edge_dynamic,
    remove_edge_dynamic,
    maintain_kcore_edge_addition,
    maintain_kcore_edge_deletion,
    full_recompute_core_numbers,
    apply_dynamic_mutation_and_maintain
)


def test_single_edge_addition_equivalence():
    # Start with a path P_4 (0-1-2-3, all cores=1)
    G = create_path_graph(4)
    cores = compute_core_numbers_batagelj_zaversnik(G)

    # Add edge (0, 3) to form a cycle C_4 (all cores should upgrade to 2)
    add_edge_dynamic(G, 0, 3)
    inc_cores, modified, _ = maintain_kcore_edge_addition(G, cores, 0, 3)
    full_cores, _ = full_recompute_core_numbers(G)

    assert inc_cores == full_cores
    assert all(c == 2 for c in inc_cores.values())
    assert len(modified) == 4


def test_single_edge_deletion_equivalence():
    # Start with a cycle C_4 (all cores=2)
    G = nx.cycle_graph(4)
    cores = compute_core_numbers_batagelj_zaversnik(G)

    # Remove edge (0, 3) to form a path P_4 (all cores should downgrade to 1)
    remove_edge_dynamic(G, 0, 3)
    inc_cores, modified, _ = maintain_kcore_edge_deletion(G, cores, 0, 3)
    full_cores, _ = full_recompute_core_numbers(G)

    assert inc_cores == full_cores
    assert all(c == 1 for c in inc_cores.values())
    assert len(modified) == 4


def test_randomized_dynamic_mutation_stream():
    """
    Executes a stream of 25 randomized edge mutations on Karate Club graph,
    asserting 100% agreement between incremental maintenance and full recomputation at every step.
    """
    random.seed(42)
    G = create_karate_club_graph()
    cores = compute_core_numbers_batagelj_zaversnik(G)

    nodes = list(G.nodes())

    for step in range(25):
        if step % 2 == 0:
            # Edge addition
            u, v = random.sample(nodes, 2)
            while G.has_edge(u, v):
                u, v = random.sample(nodes, 2)
            mutation_type = "add"
        else:
            # Edge deletion
            u, v = random.choice(list(G.edges()))
            mutation_type = "remove"

        result = apply_dynamic_mutation_and_maintain(
            G, cores, mutation_type=mutation_type, u=u, v=v
        )

        assert result["is_consistent"], f"Dynamic mismatch at step {step}: {mutation_type} ({u}, {v})"
        cores = result["updated_cores"]
