"""
Static K-Core Experimentation and Benchmarking (FR-10 Static Slice).
Benchmarks Naive Iterative Peeling O(V*E) vs. Batagelj-Zaversnik O(V+E)
across synthetic graphs of increasing scale.
"""

import time
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import networkx as nx
from src.graph_loader import create_erdos_renyi_graph, create_barabasi_albert_graph
from src.kcore_basic import compute_core_numbers_naive
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik, validate_against_networkx
from src.visualize import plot_static_runtime_scaling


def run_static_benchmarks(
    node_sizes: list = [50, 100, 250, 500, 1000, 1500],
    p_edge: float = 0.04,
    repetitions: int = 3,
    output_table_path: str = "results/tables/static_benchmark.csv",
    output_graph_path: str = "results/graphs/static_runtime_comparison.png"
) -> pd.DataFrame:
    """
    Executes controlled runtime scaling experiments comparing Naive vs Batagelj-Zaversnik.
    """
    records = []
    print("\n--- Starting Static K-Core Benchmark Experiment ---")

    for n in node_sizes:
        print(f"Testing graph size |V| = {n} nodes...")
        G = create_erdos_renyi_graph(n=n, p=p_edge, seed=42)
        m = G.number_of_edges()

        # 1. Benchmark Naive Iterative Peeling
        naive_times = []
        for _ in range(repetitions):
            t0 = time.perf_counter()
            _ = compute_core_numbers_naive(G)
            t1 = time.perf_counter()
            naive_times.append((t1 - t0) * 1000.0)  # ms
        avg_naive_ms = sum(naive_times) / len(naive_times)

        # 2. Benchmark Batagelj-Zaversnik
        eff_times = []
        for _ in range(repetitions):
            t0 = time.perf_counter()
            eff_cores = compute_core_numbers_batagelj_zaversnik(G)
            t1 = time.perf_counter()
            eff_times.append((t1 - t0) * 1000.0)  # ms
        avg_eff_ms = sum(eff_times) / len(eff_times)

        # 3. Validate correctness against NetworkX
        is_valid, report = validate_against_networkx(G, eff_cores)
        assert is_valid, f"Validation failure on graph |V|={n}"

        speedup = (avg_naive_ms / avg_eff_ms) if avg_eff_ms > 0 else 1.0

        records.append({
            "num_nodes": n,
            "num_edges": m,
            "density": round(nx.density(G), 5),
            "algorithm": "Naive (FR-2)",
            "runtime_ms": round(avg_naive_ms, 3),
            "degeneracy": max(eff_cores.values()) if eff_cores else 0
        })

        records.append({
            "num_nodes": n,
            "num_edges": m,
            "density": round(nx.density(G), 5),
            "algorithm": "Batagelj-Zaversnik (FR-3)",
            "runtime_ms": round(avg_eff_ms, 3),
            "degeneracy": max(eff_cores.values()) if eff_cores else 0
        })

        print(f"  |V|={n:4d}, |E|={m:5d} -> Naive: {avg_naive_ms:7.2f} ms | BZ: {avg_eff_ms:6.2f} ms | Speedup: {speedup:6.2f}x")

    df = pd.DataFrame(records)

    # Save outputs
    os.makedirs(os.path.dirname(os.path.abspath(output_table_path)), exist_ok=True)
    df.to_csv(output_table_path, index=False)
    print(f"[SAVED] Table written to: {output_table_path}")

    plot_static_runtime_scaling(df, save_path=output_graph_path)
    print(f"[SAVED] Chart written to: {output_graph_path}")

    return df


if __name__ == "__main__":
    run_static_benchmarks()
