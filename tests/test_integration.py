"""
Integration and End-to-End Workflow Tests (SRS Section 11.2).
"""

import os
import networkx as nx
import pytest
from src.graph_loader import create_karate_club_graph, save_edge_list_file, load_edge_list_file
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik, validate_against_networkx
from src.dynamic_kcore import apply_dynamic_mutation_and_maintain
from src.metrics import summarize_kcore_stats


def test_full_pipeline_integration(tmp_path):
    # 1. Ingestion / Loading
    G = create_karate_club_graph()
    temp_file = str(tmp_path / "karate.csv")
    save_edge_list_file(G, temp_file)
    loaded_G = load_edge_list_file(temp_file)

    assert loaded_G.number_of_nodes() == 34
    assert loaded_G.number_of_edges() == 78

    # 2. Static Decomposition
    cores = compute_core_numbers_batagelj_zaversnik(loaded_G)
    is_valid, report = validate_against_networkx(loaded_G, cores)
    assert is_valid

    # 3. Summary Metrics
    stats = summarize_kcore_stats(loaded_G, cores)
    assert stats["num_nodes"] == 34
    assert stats["degeneracy"] == 4

    # 4. Dynamic Update & Maintenance
    res_add = apply_dynamic_mutation_and_maintain(
        loaded_G, cores, mutation_type="add", u=0, v=33
    )
    assert res_add["is_consistent"]

    res_remove = apply_dynamic_mutation_and_maintain(
        loaded_G, res_add["updated_cores"], mutation_type="remove", u=0, v=33
    )
    assert res_remove["is_consistent"]
