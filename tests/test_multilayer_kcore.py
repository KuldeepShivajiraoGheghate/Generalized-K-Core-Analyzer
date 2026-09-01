"""
Unit tests for Multi-Relational / Multiplex K-Core Decomposition (FR-9).
"""

import networkx as nx
import pytest
from src.multilayer_kcore import (
    MultiplexGraph,
    compute_layerwise_core_numbers,
    compute_composite_multiplex_kcore
)


def test_multiplex_graph_construction():
    mg = MultiplexGraph()
    mg.add_edge("A", "B", layer="work")
    mg.add_edge("B", "C", layer="work")
    mg.add_edge("A", "B", layer="social")
    mg.add_edge("A", "C", layer="social")

    assert set(mg.get_layers()) == {"social", "work"}
    assert "A" in mg.nodes
    assert "B" in mg.nodes
    assert "C" in mg.nodes

    g_work = mg.get_layer_subgraph("work")
    assert g_work.number_of_edges() == 2

    g_social = mg.get_layer_subgraph("social")
    assert g_social.number_of_edges() == 2


def test_composite_multiplex_kcore():
    # Construct a 2-layer graph on 4 nodes {0, 1, 2, 3}
    # Layer 1 (collab): complete graph K_4 on all 4 nodes (degree=3 each)
    # Layer 2 (friend): path 0-1-2-3 (degrees: 0->1, 1->2, 2->2, 3->1)
    mg = MultiplexGraph()
    # Layer 1: K4
    for u in range(4):
        for v in range(u + 1, 4):
            mg.add_edge(u, v, layer="collab")
    # Layer 2: Path
    mg.add_edge(0, 1, layer="friend")
    mg.add_edge(1, 2, layer="friend")
    mg.add_edge(2, 3, layer="friend")

    # Joint requirement: deg_collab >= 2 AND deg_friend >= 2
    # In collab, all have degree 3 >= 2.
    # In friend, nodes 0 and 3 have degree 1 < 2, so they are peeled.
    # Removing 0 and 3 leaves nodes 1 and 2 with friend degree 1 < 2, which also cascade and get peeled.
    # Composite (2, 2)-core should be empty.
    sub_empty, removed = compute_composite_multiplex_kcore(mg, {"collab": 2, "friend": 2})
    assert sub_empty.number_of_nodes() == 0
    assert len(removed) == 4

    # Joint requirement: deg_collab >= 2 AND deg_friend >= 1
    # Nodes 0, 1, 2, 3 all have deg_collab=3 >= 2 and deg_friend >= 1.
    # Composite (2, 1)-core should contain all 4 nodes.
    sub_full, _ = compute_composite_multiplex_kcore(mg, {"collab": 2, "friend": 1})
    assert sub_full.number_of_nodes() == 4
