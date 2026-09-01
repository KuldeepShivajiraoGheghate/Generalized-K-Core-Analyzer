"""
Static Visualization Module (FR-11).
Generates publication-quality Matplotlib charts and network diagrams
for core distributions, dynamic benchmarks, and multi-relational comparisons.
"""

from typing import Dict, List, Any, Optional
import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless figure generation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from src.metrics import compute_core_distribution, compute_degeneracy


# Aesthetic styling defaults
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
ACCENT_COLOR = "#2ca02c"


def plot_kcore_network(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    title: str = "K-Core Network Decomposition",
    save_path: Optional[str] = None,
    figsize: tuple = (9, 7)
) -> plt.Figure:
    """
    Renders a node-link graph diagram with node colors corresponding to core numbers.
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    
    if graph.number_of_nodes() == 0:
        ax.text(0.5, 0.5, "Empty Graph", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return fig

    # Compute spring layout
    pos = nx.spring_layout(graph, seed=42)
    
    nodes = list(graph.nodes())
    cores = [core_numbers.get(n, 0) for n in nodes]
    degrees = [graph.degree(n) for n in nodes]
    node_sizes = [max(150, 40 * d + 80) for d in degrees]

    # Draw edges
    nx.draw_networkx_edges(
        graph, pos, ax=ax, alpha=0.35, edge_color="#7f8c8d", width=1.2
    )

    # Draw nodes
    cmap = plt.cm.viridis
    scatter = nx.draw_networkx_nodes(
        graph, pos, nodelist=nodes, node_color=cores, cmap=cmap,
        node_size=node_sizes, edgecolors="#2c3e50", linewidths=1.2, ax=ax
    )

    # Draw labels if graph is reasonably small
    if graph.number_of_nodes() <= 70:
        nx.draw_networkx_labels(
            graph, pos, font_size=8, font_family="sans-serif",
            font_color="#ffffff", font_weight="bold", ax=ax
        )

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label("Core Number $c(v)$", fontsize=11, fontweight="bold")

    degeneracy = compute_degeneracy(core_numbers)
    ax.set_title(f"{title}\n($|V|={graph.number_of_nodes()}$, $|E|={graph.number_of_edges()}$, Degeneracy $k_{{\\max}}={degeneracy}$)", fontsize=13, fontweight="bold", pad=12)
    ax.axis("off")
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    return fig


def plot_core_distribution(
    core_numbers: Dict[Any, int],
    title: str = "K-Shell Frequency Distribution",
    save_path: Optional[str] = None,
    figsize: tuple = (8, 5)
) -> plt.Figure:
    """
    Renders a bar chart showing the count and percentage of vertices in each k-shell.
    """
    dist = compute_core_distribution(core_numbers)
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    if not dist:
        ax.text(0.5, 0.5, "No Core Data", ha="center", va="center")
        return fig

    k_vals = list(dist.keys())
    counts = list(dist.values())
    total_nodes = sum(counts)

    bars = ax.bar(
        [str(k) for k in k_vals],
        counts,
        color="#2b5c8f",
        edgecolor="#1b3a5b",
        width=0.6,
        alpha=0.9
    )

    # Annotate percentage above bars
    for bar, count in zip(bars, counts):
        pct = (count / total_nodes) * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max(counts) * 0.02),
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    ax.set_xlabel("Core Number ($k$)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Node Count $|V_k|$", fontsize=11, fontweight="bold")
    ax.set_title(f"{title} (Total $|V|={total_nodes}$)", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylim(0, max(counts) * 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    return fig


def plot_static_runtime_scaling(
    df_results: Any,
    save_path: Optional[str] = None,
    figsize: tuple = (8, 5)
) -> plt.Figure:
    """
    Plots runtime scaling comparison between Naive O(V*E) and Batagelj-Zaversnik O(V+E).
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    # Group by graph size / nodes
    df_naive = df_results[df_results["algorithm"] == "Naive (FR-2)"]
    df_eff = df_results[df_results["algorithm"] == "Batagelj-Zaversnik (FR-3)"]

    ax.plot(
        df_naive["num_nodes"],
        df_naive["runtime_ms"],
        marker="o",
        linewidth=2,
        color="#e74c3c",
        label="Naive Peeling $O(V \\cdot E)$"
    )
    ax.plot(
        df_eff["num_nodes"],
        df_eff["runtime_ms"],
        marker="s",
        linewidth=2,
        color="#27ae60",
        label="Batagelj-Zaversnik $O(V + E)$"
    )

    ax.set_xlabel("Graph Size ($|V|$ Nodes)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Execution Time (milliseconds)", fontsize=11, fontweight="bold")
    ax.set_title("Static K-Core Runtime Scaling: Naive vs. Batagelj-Zaversnik", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    return fig


def plot_dynamic_runtime_comparison(
    df_dynamic: Any,
    save_path: Optional[str] = None,
    figsize: tuple = (9, 5)
) -> plt.Figure:
    """
    Plots dynamic mutation execution times: Full Recomputation vs Incremental Maintenance.
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    x = range(1, len(df_dynamic) + 1)
    ax.plot(
        x,
        df_dynamic["full_recompute_ms"],
        marker="o",
        linestyle="--",
        color="#e67e22",
        linewidth=1.8,
        label="Full Recomputation Baseline (FR-6)"
    )
    ax.plot(
        x,
        df_dynamic["incremental_ms"],
        marker="^",
        linestyle="-",
        color="#2980b9",
        linewidth=2.0,
        label="Incremental Maintenance (FR-7)"
    )

    avg_speedup = df_dynamic["speedup"].mean()
    ax.set_xlabel("Dynamic Mutation Step Sequence", fontsize=11, fontweight="bold")
    ax.set_ylabel("Execution Time (milliseconds)", fontsize=11, fontweight="bold")
    ax.set_title(f"Dynamic Maintenance vs. Full Recomputation (Avg Speedup: {avg_speedup:.2f}x)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    return fig


def plot_weighted_core_shift(
    df_weighted: Any,
    save_path: Optional[str] = None,
    figsize: tuple = (8, 5)
) -> plt.Figure:
    """
    Plots unweighted vs weighted core ranks showing hierarchy shifts.
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    scatter = ax.scatter(
        df_weighted["unweighted_core"],
        df_weighted["weighted_core"],
        c=df_weighted["strength"],
        cmap="plasma",
        s=80,
        alpha=0.8,
        edgecolors="#2c3e50"
    )

    # Reference diagonal line
    max_val = max(df_weighted["unweighted_core"].max(), df_weighted["weighted_core"].max())
    ax.plot([0, max_val], [0, max_val], "k--", alpha=0.5, label="Identity Line ($c_w = c_{unw}$)")

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Node Strength $s(u)$", fontsize=10, fontweight="bold")

    ax.set_xlabel("Unweighted Core Number $c(u)$", fontsize=11, fontweight="bold")
    ax.set_ylabel("Weighted Strength Core $c_w(u)$", fontsize=11, fontweight="bold")
    ax.set_title("Core Hierarchy Shift: Unweighted vs. Weighted Strength Decomposition", fontsize=12, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    return fig


def plot_multilayer_core_distribution(
    layer_cores: Dict[str, Dict[Any, int]],
    save_path: Optional[str] = None,
    figsize: tuple = (8, 5)
) -> plt.Figure:
    """
    Plots comparative core number distributions across distinct relationship layers.
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    layers = list(layer_cores.keys())
    all_k = sorted(list({k for lc in layer_cores.values() for k in lc.values()}))

    x = np.arange(len(all_k))
    width = 0.8 / len(layers) if layers else 0.4
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6"]

    for idx, layer in enumerate(layers):
        dist = compute_core_distribution(layer_cores[layer])
        counts = [dist.get(k, 0) for k in all_k]
        ax.bar(
            x + (idx * width) - (0.4 - width / 2),
            counts,
            width=width,
            label=f"Layer: {layer}",
            color=colors[idx % len(colors)],
            alpha=0.85
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"k={k}" for k in all_k])
    ax.set_xlabel("Core Number Level ($k$)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Node Count", fontsize=11, fontweight="bold")
    ax.set_title("Multi-Relational Layer-wise Core Distribution Comparison", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=True, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight")

    return fig
