"""
Weighted K-Core Experimentation and Benchmarking (FR-10 Weighted Slice).
Compares topological unweighted core decomposition vs. node-strength weighted decomposition.
"""

import os
import sys
import random

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import networkx as nx
from src.graph_loader import create_karate_club_graph, create_erdos_renyi_graph
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik
from src.weighted_kcore import compute_weighted_core_numbers, compare_unweighted_vs_weighted_cores
from src.visualize import plot_weighted_core_shift


def run_weighted_benchmarks(
    num_nodes: int = 150,
    p_edge: float = 0.08,
    seed: int = 42,
    output_table_path: str = "results/tables/weighted_benchmark.csv",
    output_graph_path: str = "results/graphs/weighted_core_shift.png"
) -> pd.DataFrame:
    """
    Assigns heterogeneous weights to a network, computes both unweighted and weighted cores,
    and analyzes the percentage of nodes experiencing rank/core shifts.
    """
    random.seed(seed)
    print(f"\n--- Starting Weighted K-Core Benchmark (|V|={num_nodes}) ---")

    G = create_erdos_renyi_graph(n=num_nodes, p=p_edge, seed=seed)

    # Assign heterogeneous real-valued weights: core edges get higher weights, peripheral lower
    for u, v in G.edges():
        weight = round(random.uniform(0.5, 5.0), 2)
        G[u][v]["weight"] = weight

    # 1. Unweighted core numbers
    unw_cores = compute_core_numbers_batagelj_zaversnik(G)

    # 2. Weighted core numbers
    w_cores = compute_weighted_core_numbers(G, step_size=1.0, weight_attr="weight")

    # 3. Comparison
    comparison = compare_unweighted_vs_weighted_cores(G, unw_cores, w_cores)
    df = pd.DataFrame(comparison)

    num_shifted = df["is_shifted"].sum()
    pct_shifted = (num_shifted / len(df)) * 100

    print(f"Total Nodes: {len(df)} | Shifted Nodes: {num_shifted} ({pct_shifted:.1f}%)")

    # Save outputs
    os.makedirs(os.path.dirname(os.path.abspath(output_table_path)), exist_ok=True)
    df.to_csv(output_table_path, index=False)
    print(f"[SAVED] Table written to: {output_table_path}")

    plot_weighted_core_shift(df, save_path=output_graph_path)
    print(f"[SAVED] Chart written to: {output_graph_path}")

    return df


if __name__ == "__main__":
    run_weighted_benchmarks()
