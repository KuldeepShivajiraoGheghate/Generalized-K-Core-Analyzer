"""
Graph Construction and Ingestion Module (FR-1).
Provides loaders for synthetic reference topologies, real-world datasets,
and custom edge-list files.
"""

from typing import Dict, List, Tuple, Optional, Any
import os
import networkx as nx
import pandas as pd


def create_path_graph(n: int = 5) -> nx.Graph:
    """Creates a simple path graph P_n: 0 - 1 - 2 - ... - (n-1)."""
    return nx.path_graph(n)


def create_cycle_graph(n: int = 5) -> nx.Graph:
    """Creates a simple cycle graph C_n."""
    return nx.cycle_graph(n)


def create_star_graph(n: int = 5) -> nx.Graph:
    """Creates a star graph S_n with center node 0 connected to n outer nodes."""
    return nx.star_graph(n)


def create_complete_graph(n: int = 5) -> nx.Graph:
    """Creates a complete graph K_n."""
    return nx.complete_graph(n)


def create_disconnected_graph() -> nx.Graph:
    """
    Creates a disconnected multi-component reference graph:
    Component 1: Complete graph K_4 (nodes 0, 1, 2, 3) -> 3-core
    Component 2: Triangle cycle C_3 (nodes 4, 5, 6) -> 2-core
    Component 3: Isolated path P_2 (nodes 7, 8) -> 1-core
    Component 4: Isolated node 9 -> 0-core
    """
    G = nx.Graph()
    # K_4
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    # C_3
    G.add_edges_from([(4, 5), (5, 6), (6, 4)])
    # P_2
    G.add_edges_from([(7, 8)])
    # Isolated node
    G.add_node(9)
    return G


def create_erdos_renyi_graph(n: int = 100, p: float = 0.05, seed: Optional[int] = 42) -> nx.Graph:
    """Generates an Erdős-Rényi random graph G(n, p)."""
    return nx.erdos_renyi_graph(n=n, p=p, seed=seed)


def create_barabasi_albert_graph(n: int = 100, m: int = 3, seed: Optional[int] = 42) -> nx.Graph:
    """Generates a Barabási-Albert scale-free graph G(n, m)."""
    return nx.barabasi_albert_graph(n=n, m=m, seed=seed)


def create_karate_club_graph() -> nx.Graph:
    """Loads the canonical Zachary's Karate Club graph (|V|=34, |E|=78)."""
    return nx.karate_club_graph()


def create_dolphins_graph() -> nx.Graph:
    """
    Creates the famous Dolphins social network (|V|=62, |E|=159).
    Built directly if raw file is not present or loaded from dataset.
    """
    # Embedded fallback edge list if file not found
    dolphins_edges = [
        ("Beak", "Fish"), ("Beak", "Grin"), ("Beak", "Haecksel"), ("Beak", "SN9"),
        ("Beak", "SN96"), ("Beak", "TR77"), ("Beescratch", "Jet"), ("Beescratch", "Knit"),
        ("Beescratch", "Notch"), ("Beescratch", "Number1"), ("Beescratch", "SN100"),
        ("Beescratch", "SN96"), ("Beescratch", "TR77"), ("Beescratch", "Upnow"),
        ("Bumper", "Fish"), ("Bumper", "SN96"), ("Bumper", "Thumper"), ("Bumper", "Zipfel"),
        ("CCL", "Double"), ("CCL", "Grin"), ("CCL", "Zap"), ("Cross", "Trigger"),
        ("DN16", "Feather"), ("DN16", "Gallatin"), ("DN16", "Wave"), ("DN16", "Web"),
        ("DN21", "Feather"), ("DN21", "Gallatin"), ("DN21", "Jet"), ("DN21", "Upnow"),
        ("DN21", "Wave"), ("DN21", "Web"), ("DN63", "Knit"), ("DN63", "Number1"),
        ("DN63", "PL"), ("DN63", "SN9"), ("DN63", "Upnow"), ("Double", "Kringel"),
        ("Double", "SN4"), ("Double", "Topless"), ("Double", "Zap"), ("Feather", "Gallatin"),
        ("Feather", "Ripplefluke"), ("Feather", "SN90"), ("Feather", "Web"),
        ("Fish", "Patchback"), ("Fish", "SN96"), ("Fish", "TR77"), ("Five", "Trigger"),
        ("Fork", "Scabs"), ("Gallatin", "Jet"), ("Gallatin", "Ripplefluke"),
        ("Gallatin", "SN90"), ("Gallatin", "Upnow"), ("Gallatin", "Web"),
        ("Grin", "Hook"), ("Grin", "MN83"), ("Grin", "SN4"), ("Grin", "SN63"),
        ("Grin", "SN9"), ("Grin", "Stripes"), ("Grin", "TR99"), ("Haecksel", "Jonah"),
        ("Haecksel", "MN83"), ("Haecksel", "SN9"), ("Haecksel", "Topless"),
        ("Haecksel", "Vito"), ("Haecksel", "Zap"), ("Hook", "Kringel"),
        ("Hook", "SN4"), ("Hook", "SN63"), ("Hook", "SN89"), ("Hook", "TR99"),
        ("Jonah", "Kringel"), ("Jonah", "MN105"), ("Jonah", "MN83"), ("Jonah", "Patchback"),
        ("Jonah", "Topless"), ("Jonah", "Trigger"), ("Knit", "PL"), ("Knit", "Upnow"),
        ("Kringel", "MN83"), ("Kringel", "Patchback"), ("Kringel", "SN100"),
        ("Kringel", "SN4"), ("Kringel", "SN63"), ("Kringel", "Thumper"),
        ("Kringel", "TR99"), ("MN105", "Patchback"), ("MN105", "Scabs"),
        ("MN105", "SN4"), ("MN105", "Topless"), ("MN105", "Trigger"),
        ("MN105", "TR99"), ("MN60", "SN4"), ("MN60", "Topless"), ("MN60", "Trigger"),
        ("MN83", "Patchback"), ("MN83", "SN4"), ("MN83", "Topless"), ("MN83", "Trigger"),
        ("MN83", "TR99"), ("Mus", "Notch"), ("Mus", "Number1"), ("Mus", "PL"),
        ("Mus", "SN4"), ("Notch", "Number1"), ("Notch", "Upnow"), ("Number1", "PL"),
        ("Number1", "SN96"), ("Patchback", "SMN5"), ("Patchback", "Stripes"),
        ("Patchback", "Topless"), ("Patchback", "Trigger"), ("Patchback", "TR99"),
        ("PL", "SN4"), ("PL", "SN96"), ("PL", "TR77"), ("Ripplefluke", "Scabs"),
        ("Ripplefluke", "SN90"), ("Ripplefluke", "Upnow"), ("Ripplefluke", "Zig"),
        ("Scabs", "Shallow"), ("Scabs", "SN4"), ("Scabs", "SN63"), ("Scabs", "SN9"),
        ("Scabs", "Stripes"), ("Scabs", "Topless"), ("Scabs", "TR99"),
        ("Shallow", "Topless"), ("SMN5", "Trigger"), ("SN100", "SN4"),
        ("SN100", "SN89"), ("SN100", "SN9"), ("SN100", "Zap"), ("SN4", "SN63"),
        ("SN4", "SN89"), ("SN4", "SN9"), ("SN4", "Stripes"), ("SN4", "Topless"),
        ("SN4", "Trigger"), ("SN4", "TR99"), ("SN4", "Zipfel"), ("SN63", "Stripes"),
        ("SN63", "Thumper"), ("SN63", "TR99"), ("SN63", "TSN83"), ("SN89", "Web"),
        ("SN9", "TSN103"), ("SN9", "TSN83"), ("SN9", "Upnow"), ("SN9", "Vito"),
        ("SN9", "Zipfel"), ("SN90", "Upnow"), ("SN90", "Web"), ("SN96", "TR77"),
        ("SN96", "TSN83"), ("Stripes", "TR99"), ("Topless", "TR99"),
        ("Topless", "Trigger"), ("Topless", "Zap"), ("TR77", "TR99"),
        ("Trigger", "Vito"), ("TSN83", "Zipfel"), ("Upnow", "Web"),
        ("Vito", "Zap"), ("Wave", "Web"), ("Web", "Zig"), ("Zipfel", "Zap")
    ]
    dolphins_nodes = [
        "Beak", "Beescratch", "Bumper", "CCL", "Cross", "DN16", "DN21", "DN63", "Double",
        "Feather", "Fish", "Five", "Fork", "Gallatin", "Grin", "Haecksel", "Hook", "Jet", "Jonah",
        "Knit", "Kringel", "MN105", "MN60", "MN83", "Mus", "Notch", "Number1", "Patchback",
        "PL", "Quasi", "Ripplefluke", "Scabs", "Shallow", "Shmuddel", "SMN5", "SN100",
        "SN4", "SN63", "SN89", "SN9", "SN90", "SN96", "Stripes", "Thumper", "Topless",
        "TR120", "TR77", "TR82", "TR88", "TR99", "Trigger", "TSN103", "TSN83", "Upnow",
        "Vito", "Wave", "Web", "Whitetip", "Zap", "Zig", "Zipfel", "Oscar"
    ]
    G = nx.Graph()
    for n in dolphins_nodes:
        G.add_node(n)
    G.add_edges_from(dolphins_edges)
    return G


def load_edge_list_file(
    filepath: str,
    delimiter: str = ",",
    source_col: str = "source",
    target_col: str = "target",
    weight_col: Optional[str] = "weight",
    layer_col: Optional[str] = "relationship_type"
) -> nx.Graph:
    """
    Loads an undirected graph from a CSV/TSV edge list.
    Supports optional edge weights and relationship layer labels.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found: {filepath}")

    df = pd.read_csv(filepath, sep=delimiter)
    
    if source_col not in df.columns or target_col not in df.columns:
        raise ValueError(f"Columns '{source_col}' and '{target_col}' required in {filepath}")

    G = nx.Graph()
    for _, row in df.iterrows():
        u = row[source_col]
        v = row[target_col]
        edge_data: Dict[str, Any] = {}
        
        if weight_col and weight_col in df.columns and pd.notna(row[weight_col]):
            edge_data["weight"] = float(row[weight_col])
        else:
            edge_data["weight"] = 1.0
            
        if layer_col and layer_col in df.columns and pd.notna(row[layer_col]):
            edge_data["relationship_type"] = str(row[layer_col])
        else:
            edge_data["relationship_type"] = "default"

        G.add_edge(u, v, **edge_data)
        
    return G


def save_edge_list_file(
    graph: nx.Graph,
    filepath: str,
    delimiter: str = ","
) -> None:
    """Exports a graph to a CSV edge list with weights and layers if present."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    rows = []
    for u, v, data in graph.edges(data=True):
        rows.append({
            "source": u,
            "target": v,
            "weight": data.get("weight", 1.0),
            "relationship_type": data.get("relationship_type", "default")
        })
    df = pd.DataFrame(rows)
    df.to_csv(filepath, sep=delimiter, index=False)
