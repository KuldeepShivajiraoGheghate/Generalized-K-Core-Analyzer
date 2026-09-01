"""
Dynamic K-Core Experimentation and Benchmarking (FR-10 Dynamic Slice).
Benchmarks Full Recomputation Baseline (FR-6) vs. Incremental K-Core Maintenance (FR-7)
across a sequence of dynamic edge mutations.
"""

import time
import os
import sys
import random

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import networkx as nx
from src.graph_loader import create_barabasi_albert_graph
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik
from src.dynamic_kcore import apply_dynamic_mutation_and_maintain
from src.visualize import plot_dynamic_runtime_comparison


def run_dynamic_benchmarks(
    num_nodes: int = 1000,
    m_attach: int = 4,
    num_mutations: int = 30,
    seed: int = 42,
    output_table_path: str = "results/tables/dynamic_benchmark.csv",
    output_graph_path: str = "results/graphs/dynamic_runtime_comparison.png"
) -> pd.DataFrame:
    """
    Executes a stream of alternating edge additions and deletions, comparing
    incremental maintenance vs. full recomputation runtime and asserting 100% equivalence.
    """
    random.seed(seed)
    print(f"\n--- Starting Dynamic K-Core Benchmark (|V|={num_nodes}, Mutations={num_mutations}) ---")

    G = create_barabasi_albert_graph(n=num_nodes, m=m_attach, seed=seed)
    cores = compute_core_numbers_batagelj_zaversnik(G)

    records = []
    nodes_list = list(G.nodes())

    for step in range(1, num_mutations + 1):
        # Alternate between insertion and deletion
        if step % 2 == 1:
            mutation_type = "add"
            # Choose a non-existing edge
            u, v = random.sample(nodes_list, 2)
            while G.has_edge(u, v):
                u, v = random.sample(nodes_list, 2)
        else:
            mutation_type = "remove"
            # Choose an existing edge
            if G.number_of_edges() > 0:
                u, v = random.choice(list(G.edges()))
            else:
                continue

        result = apply_dynamic_mutation_and_maintain(
            G, cores, mutation_type=mutation_type, u=u, v=v
        )

        assert result["is_consistent"], f"Dynamic mismatch at step {step}: {mutation_type} ({u}, {v})"
        cores = result["updated_cores"]

        inc_ms = result["incremental_time_sec"] * 1000.0
        full_ms = result["full_recompute_time_sec"] * 1000.0
        speedup = result["speedup"]

        records.append({
            "step": step,
            "mutation_type": mutation_type,
            "edge": f"({u},{v})",
            "modified_nodes_count": result["num_modified_nodes"],
            "incremental_ms": round(inc_ms, 3),
            "full_recompute_ms": round(full_ms, 3),
            "speedup": round(speedup, 2),
            "is_consistent": result["is_consistent"]
        })

        if step % 5 == 0 or step == num_mutations:
            print(f"  Step {step:2d} [{mutation_type.upper():6s}]: Inc={inc_ms:6.2f} ms | Full={full_ms:6.2f} ms | Speedup={speedup:5.1f}x | Affected={result['num_modified_nodes']}")

    df = pd.DataFrame(records)

    # Save outputs
    os.makedirs(os.path.dirname(os.path.abspath(output_table_path)), exist_ok=True)
    df.to_csv(output_table_path, index=False)
    print(f"[SAVED] Table written to: {output_table_path}")

    plot_dynamic_runtime_comparison(df, save_path=output_graph_path)
    print(f"[SAVED] Chart written to: {output_graph_path}")

    avg_speedup = df["speedup"].mean()
    print(f"[SUCCESS] Dynamic benchmark completed with average speedup of {avg_speedup:.2f}x.")

    return df


if __name__ == "__main__":
    run_dynamic_benchmarks()
