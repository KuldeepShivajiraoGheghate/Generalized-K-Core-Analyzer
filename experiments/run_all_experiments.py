"""
Master Experiment Runner (FR-10).
Executes the complete 4-axis experimentation suite and real-world network evaluations,
generating all benchmark CSV tables and Matplotlib visualization figures.
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import networkx as nx
from src.graph_loader import (
    create_karate_club_graph,
    create_dolphins_graph,
    save_edge_list_file
)
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik
from src.metrics import summarize_kcore_stats
from src.visualize import plot_kcore_network, plot_core_distribution
from experiments.static_experiment import run_static_benchmarks
from experiments.dynamic_experiment import run_dynamic_benchmarks
from experiments.weighted_experiment import run_weighted_benchmarks
from experiments.multilayer_experiment import run_multilayer_benchmarks


def run_realworld_evaluations() -> pd.DataFrame:
    """
    Evaluates static k-core decomposition on canonical real-world networks:
    Zachary Karate Club and Dolphins Social Network.
    """
    print("\n--- Starting Real-World Network Analysis (Phase 6) ---")
    datasets = {
        "Zachary_Karate_Club": create_karate_club_graph(),
        "Dolphins_Social_Network": create_dolphins_graph()
    }

    records = []
    for name, G in datasets.items():
        # Save raw dataset edge list
        raw_path = f"data/raw/{name.lower()}_edgelist.csv"
        proc_path = f"data/processed/{name.lower()}_cleaned.csv"
        save_edge_list_file(G, raw_path)
        save_edge_list_file(G, proc_path)

        cores = compute_core_numbers_batagelj_zaversnik(G)
        stats = summarize_kcore_stats(G, cores)

        # Plot network and distribution figures
        net_fig_path = f"results/graphs/{name.lower()}_kcore_network.png"
        dist_fig_path = f"results/graphs/{name.lower()}_core_distribution.png"
        plot_kcore_network(G, cores, title=f"{name.replace('_', ' ')} K-Core Decomposition", save_path=net_fig_path)
        plot_core_distribution(cores, title=f"{name.replace('_', ' ')} Core Distribution", save_path=dist_fig_path)

        records.append({
            "dataset": name,
            "num_nodes": stats["num_nodes"],
            "num_edges": stats["num_edges"],
            "density": stats["density"],
            "avg_degree": stats["avg_degree"],
            "degeneracy_kmax": stats["degeneracy"],
            "avg_core_number": stats["avg_core_number"],
            "num_connected_components": stats["num_connected_components"]
        })
        print(f"  {name}: |V|={stats['num_nodes']}, |E|={stats['num_edges']}, Degeneracy k_max={stats['degeneracy']}")

    df = pd.DataFrame(records)
    table_path = "results/tables/realworld_kcore_stats.csv"
    os.makedirs(os.path.dirname(os.path.abspath(table_path)), exist_ok=True)
    df.to_csv(table_path, index=False)
    print(f"[SAVED] Real-world stats table written to: {table_path}")
    return df


def run_all():
    """Runs all 4 experimental axes and real-world evaluations."""
    print("=" * 70)
    print(" GENERALIZED K-CORE ANALYZER (GKCA) - FULL EXPERIMENTATION SUITE")
    print("=" * 70)

    # 1. Real-World Datasets (Phase 6)
    run_realworld_evaluations()

    # 2. Static Scaling Benchmarks (Axis 1 / Phase 5)
    run_static_benchmarks()

    # 3. Dynamic Maintenance Benchmarks (Axis 2 / Phase 8)
    run_dynamic_benchmarks()

    # 4. Weighted Decomposition Benchmarks (Axis 3 / Phase 9)
    run_weighted_benchmarks()

    # 5. Multilayer Multiplex Benchmarks (Axis 4 / Phase 10)
    run_multilayer_benchmarks()

    print("\n" + "=" * 70)
    print(" [ALL EXPERIMENTS COMPLETED SUCCESSFULLY]")
    print(" Result tables saved in: results/tables/")
    print(" Visual charts saved in: results/graphs/")
    print("=" * 70)


if __name__ == "__main__":
    run_all()
