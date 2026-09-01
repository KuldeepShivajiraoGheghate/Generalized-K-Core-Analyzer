"""
Multi-Relational / Multiplex K-Core Experimentation (FR-10 Multi-Relational Slice).
Evaluates core structure shifts across isolated layers versus combined multiplex configurations.
"""

import os
import sys
import random

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import networkx as nx
from src.graph_loader import create_erdos_renyi_graph
from src.multilayer_kcore import MultiplexGraph, compute_layerwise_core_numbers, compute_composite_multiplex_kcore
from src.visualize import plot_multilayer_core_distribution


def run_multilayer_benchmarks(
    num_nodes: int = 120,
    layers: list = ["social_follow", "collaboration", "communication"],
    p_values: list = [0.06, 0.04, 0.05],
    seed: int = 42,
    output_table_path: str = "results/tables/multilayer_benchmark.csv",
    output_graph_path: str = "results/graphs/multilayer_core_distribution.png"
) -> pd.DataFrame:
    """
    Constructs a 3-layer multiplex network and analyzes layer-specific vs composite coreness.
    """
    random.seed(seed)
    print(f"\n--- Starting Multi-Relational / Multiplex Benchmark (|V|={num_nodes}, Layers={len(layers)}) ---")

    m_graph = MultiplexGraph()
    for n in range(num_nodes):
        m_graph.add_node(n)

    for layer_name, p in zip(layers, p_values):
        g_temp = create_erdos_renyi_graph(n=num_nodes, p=p, seed=seed + len(layer_name))
        for u, v in g_temp.edges():
            m_graph.add_edge(u, v, layer=layer_name)

    # 1. Compute layer-wise core numbers
    layer_cores = compute_layerwise_core_numbers(m_graph)

    # 2. Compute composite multiplex core (e.g. k=2 across all layers)
    k_vec = {layer: 2 for layer in layers}
    comp_subgraph, _ = compute_composite_multiplex_kcore(m_graph, k_vec)

    comp_survivors = comp_subgraph.number_of_nodes()

    records = []
    for layer in layers:
        cores = layer_cores[layer]
        records.append({
            "layer": layer,
            "num_nodes": num_nodes,
            "num_edges": m_graph.get_layer_subgraph(layer).number_of_edges(),
            "max_core_degeneracy": max(cores.values()) if cores else 0,
            "avg_core": round(sum(cores.values()) / len(cores), 3) if cores else 0.0,
            "composite_k_threshold": k_vec[layer],
            "composite_surviving_nodes": comp_survivors
        })

    df = pd.DataFrame(records)

    # Save outputs
    os.makedirs(os.path.dirname(os.path.abspath(output_table_path)), exist_ok=True)
    df.to_csv(output_table_path, index=False)
    print(f"[SAVED] Table written to: {output_table_path}")

    plot_multilayer_core_distribution(layer_cores, save_path=output_graph_path)
    print(f"[SAVED] Chart written to: {output_graph_path}")

    print(f"[SUCCESS] Multiplex benchmark completed: {comp_survivors}/{num_nodes} nodes survive in joint composite core.")

    return df


if __name__ == "__main__":
    run_multilayer_benchmarks()
