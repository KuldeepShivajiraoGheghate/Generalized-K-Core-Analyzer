"""
Interactive Streamlit Dashboard (FR-12).
Provides an interactive exploration interface for graph structures, k-core decomposition,
dynamic edge updates, and execution benchmarking.
"""

import os
import sys
import time
import pandas as pd
import streamlit as st
import networkx as nx

# Add project root to sys.path so imports resolve cleanly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.graph_loader import (
    create_karate_club_graph,
    create_dolphins_graph,
    create_erdos_renyi_graph,
    create_barabasi_albert_graph,
    load_edge_list_file
)
from src.kcore_efficient import (
    compute_core_numbers_batagelj_zaversnik,
    extract_kcore_subgraph
)
from src.dynamic_kcore import apply_dynamic_mutation_and_maintain
from src.metrics import compute_graph_metrics, compute_core_distribution, compute_degeneracy
from src.visualize import plot_kcore_network, plot_core_distribution
from src.multilayer_kcore import MultiplexGraph


# Page configuration
st.set_page_config(
    page_title="Generalized K-Core Analyzer (GKCA)",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for premium look
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "graph" not in st.session_state:
    st.session_state.graph = create_karate_club_graph()
    st.session_state.dataset_name = "Zachary Karate Club"
    st.session_state.core_numbers = compute_core_numbers_batagelj_zaversnik(st.session_state.graph)
    st.session_state.last_mutation_stats = None


def reload_dataset(choice: str, n_nodes: int = 40, p_edge: float = 0.1, uploaded_file=None):
    if choice == "Zachary Karate Club":
        G = create_karate_club_graph()
    elif choice == "Dolphins Social Network":
        G = create_dolphins_graph()
    elif choice == "Synthetic: Erdős-Rényi G(n, p)":
        G = create_erdos_renyi_graph(n=n_nodes, p=p_edge, seed=42)
    elif choice == "Synthetic: Barabási-Albert Scale-Free":
        G = create_barabasi_albert_graph(n=n_nodes, m=3, seed=42)
    elif choice == "Custom CSV Upload" and uploaded_file is not None:
        # Save temp file
        temp_path = "data/raw/temp_upload.csv"
        os.makedirs("data/raw", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        G = load_edge_list_file(temp_path)
    else:
        G = create_karate_club_graph()

    st.session_state.graph = G
    st.session_state.dataset_name = choice
    st.session_state.core_numbers = compute_core_numbers_batagelj_zaversnik(G)
    st.session_state.last_mutation_stats = None


# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/network.png", width=64)
    st.title("GKCA Controls")
    st.caption("A Research-Oriented K-Core Analytics Platform")
    
    st.subheader("1. Select Dataset")
    dataset_option = st.selectbox(
        "Network Dataset",
        [
            "Zachary Karate Club",
            "Dolphins Social Network",
            "Synthetic: Erdős-Rényi G(n, p)",
            "Synthetic: Barabási-Albert Scale-Free",
            "Custom CSV Upload"
        ]
    )

    n_nodes = 40
    p_edge = 0.1
    uploaded_file = None

    if "Synthetic" in dataset_option:
        n_nodes = st.slider("Node Count (|V|)", min_value=10, max_value=200, value=40, step=5)
        if "Erdős-Rényi" in dataset_option:
            p_edge = st.slider("Edge Probability (p)", min_value=0.02, max_value=0.4, value=0.1, step=0.01)

    if dataset_option == "Custom CSV Upload":
        uploaded_file = st.file_uploader("Upload Edge List CSV (source, target)", type=["csv", "txt"])

    if st.button("Load / Reset Dataset", use_container_width=True):
        reload_dataset(dataset_option, n_nodes, p_edge, uploaded_file)
        st.success(f"Loaded: {dataset_option}")

    st.markdown("---")
    st.subheader("2. Filter & Decomposition")
    
    current_cores = st.session_state.core_numbers
    max_k = compute_degeneracy(current_cores)
    
    selected_k = st.slider(
        "K-Core Threshold (k)",
        min_value=0,
        max_value=max(1, max_k),
        value=0,
        help="Filters the visual network to show only nodes with core number c(v) >= k"
    )

    # Check for layer attribute
    layer_types = set()
    for _, _, d in st.session_state.graph.edges(data=True):
        if "relationship_type" in d:
            layer_types.add(d["relationship_type"])
    
    layer_filter = "All"
    if layer_types:
        layer_filter = st.selectbox("Relationship Layer", ["All"] + sorted(list(layer_types)))


# --- MAIN INTERFACE ---
st.markdown('<div class="main-title">Generalized K-Core Analyzer (GKCA)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Linear-time Batagelj-Zaversnik decomposition, localized incremental dynamic maintenance, and multi-relational graph analysis.</div>', unsafe_allow_html=True)

# Top Live Metrics
graph = st.session_state.graph
core_numbers = st.session_state.core_numbers
metrics = compute_graph_metrics(graph)
degeneracy = compute_degeneracy(core_numbers)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Nodes (|V|)", metrics["num_nodes"])
with col2:
    st.metric("Total Edges (|E|)", metrics["num_edges"])
with col3:
    st.metric("Degeneracy (k_max)", degeneracy)
with col4:
    st.metric("Avg Degree", metrics["avg_degree"])
with col5:
    st.metric("Graph Density", f"{metrics['density']:.4f}")

st.markdown("---")

# Main Split: Visualization & Dynamic Operations
left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("🕸️ Network Structure & Coreness")
    
    # Filter by k if requested
    if selected_k > 0:
        display_graph = extract_kcore_subgraph(graph, core_numbers, selected_k)
        chart_title = f"{st.session_state.dataset_name} ({selected_k}-Core Subgraph)"
    else:
        display_graph = graph
        chart_title = f"{st.session_state.dataset_name} (Full Graph)"

    fig_net = plot_kcore_network(
        display_graph,
        core_numbers,
        title=chart_title,
        figsize=(8, 6)
    )
    st.pyplot(fig_net)

with right_col:
    st.subheader("📊 Core Number Distribution")
    fig_dist = plot_core_distribution(
        core_numbers,
        title="Node Distribution per K-Shell",
        figsize=(7, 4.2)
    )
    st.pyplot(fig_dist)

    st.markdown("---")
    st.subheader("⚡ Dynamic Graph Mutation (FR-5 / FR-7)")
    st.caption("Apply edge insertions or deletions and observe real-time incremental maintenance vs. full recomputation.")

    nodes_list = sorted(list(graph.nodes()), key=lambda x: str(x))
    
    if len(nodes_list) >= 2:
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            u_node = st.selectbox("Node u", nodes_list, index=0)
        with m_col2:
            default_v_idx = 1 if len(nodes_list) > 1 else 0
            v_node = st.selectbox("Node v", nodes_list, index=default_v_idx)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("➕ Add Edge (u, v)", use_container_width=True):
                if u_node == v_node:
                    st.warning("Self-loops are not supported. Choose distinct nodes.")
                elif graph.has_edge(u_node, v_node):
                    st.info(f"Edge ({u_node}, {v_node}) already exists.")
                else:
                    stats = apply_dynamic_mutation_and_maintain(
                        graph, core_numbers, mutation_type="add", u=u_node, v=v_node
                    )
                    st.session_state.core_numbers = stats["updated_cores"]
                    st.session_state.last_mutation_stats = stats
                    st.rerun()

        with btn_col2:
            if st.button("➖ Remove Edge (u, v)", use_container_width=True):
                if not graph.has_edge(u_node, v_node):
                    st.warning(f"Edge ({u_node}, {v_node}) does not exist.")
                else:
                    stats = apply_dynamic_mutation_and_maintain(
                        graph, core_numbers, mutation_type="remove", u=u_node, v=v_node
                    )
                    st.session_state.core_numbers = stats["updated_cores"]
                    st.session_state.last_mutation_stats = stats
                    st.rerun()

    # Display Dynamic Timing Panel if a mutation was just executed
    if st.session_state.last_mutation_stats is not None:
        ms = st.session_state.last_mutation_stats
        st.success(f"Mutation completed! Consistent with full recompute: **{ms['is_consistent']}**")
        
        t_col1, t_col2, t_col3 = st.columns(3)
        with t_col1:
            st.metric("Full Recompute", f"{ms['full_recompute_time_sec'] * 1000:.3f} ms")
        with t_col2:
            st.metric("Incremental Time", f"{ms['incremental_time_sec'] * 1000:.3f} ms")
        with t_col3:
            st.metric("Speedup", f"{ms['speedup']:.2f}x")

# --- BENCHMARK RESULTS EXPLORER ---
st.markdown("---")
with st.expander("📈 View 4-Axis Empirical Benchmark Tables", expanded=False):
    tab1, tab2, tab3, tab4 = st.tabs([
        "Static Scaling (Naive vs BZ)",
        "Dynamic Maintenance (Inc vs Full)",
        "Weighted Strength Shifts",
        "Multi-Relational Layers"
    ])

    with tab1:
        if os.path.exists("results/tables/static_benchmark.csv"):
            df_s = pd.read_csv("results/tables/static_benchmark.csv")
            st.dataframe(df_s, width='stretch')
        else:
            st.info("Static benchmark table will appear after running experiments/run_all_experiments.py.")

    with tab2:
        if os.path.exists("results/tables/dynamic_benchmark.csv"):
            df_d = pd.read_csv("results/tables/dynamic_benchmark.csv")
            st.dataframe(df_d, width='stretch')
        else:
            st.info("Dynamic benchmark table will appear after running experiments/run_all_experiments.py.")

    with tab3:
        if os.path.exists("results/tables/weighted_benchmark.csv"):
            df_w = pd.read_csv("results/tables/weighted_benchmark.csv")
            st.dataframe(df_w, width='stretch')
        else:
            st.info("Weighted benchmark table will appear after running experiments/run_all_experiments.py.")

    with tab4:
        if os.path.exists("results/tables/multilayer_benchmark.csv"):
            df_m = pd.read_csv("results/tables/multilayer_benchmark.csv")
            st.dataframe(df_m, width='stretch')
        else:
            st.info("Multilayer benchmark table will appear after running experiments/run_all_experiments.py.")
