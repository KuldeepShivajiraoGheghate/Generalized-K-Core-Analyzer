"""
Multi-Relational (Multiplex) K-Core Decomposition Module (FR-9).
Implements layer filtering, single-layer core decomposition, and joint/composite
multiplex k-core peeling across heterogeneous edge relationship layers.
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import networkx as nx
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik


class MultiplexGraph:
    """
    Multiplex Graph representation where edges are partitioned into distinct relationship layers.
    Vertices are shared across layers, while edge sets are layer-specific.
    """

    def __init__(self, layer_attr: str = "relationship_type"):
        self.layer_attr = layer_attr
        self.nodes: Set[Any] = set()
        self.layers: Dict[str, nx.Graph] = {}

    def add_node(self, node: Any) -> None:
        self.nodes.add(node)
        for g in self.layers.values():
            g.add_node(node)

    def add_edge(self, u: Any, v: Any, layer: str = "default", **attrs) -> None:
        self.nodes.add(u)
        self.nodes.add(v)
        if layer not in self.layers:
            self.layers[layer] = nx.Graph()
            for n in self.nodes:
                self.layers[layer].add_node(n)

        self.layers[layer].add_edge(u, v, **attrs)

    def get_layers(self) -> List[str]:
        return sorted(list(self.layers.keys()))

    def get_layer_subgraph(self, layer: str) -> nx.Graph:
        """Returns the graph for a specific layer."""
        if layer not in self.layers:
            g = nx.Graph()
            for n in self.nodes:
                g.add_node(n)
            return g
        return self.layers[layer].copy()

    def get_aggregate_graph(self, selected_layers: Optional[List[str]] = None) -> nx.Graph:
        """
        Builds the flattened aggregate graph combining edges from selected layers.
        If selected_layers is None, combines all layers.
        """
        agg = nx.Graph()
        for n in self.nodes:
            agg.add_node(n)

        target_layers = selected_layers if selected_layers is not None else list(self.layers.keys())
        for layer_name in target_layers:
            if layer_name in self.layers:
                for u, v, data in self.layers[layer_name].edges(data=True):
                    agg.add_edge(u, v, **data)
        return agg

    @classmethod
    def from_nx_graph(cls, graph: nx.Graph, layer_attr: str = "relationship_type") -> "MultiplexGraph":
        """Builds a MultiplexGraph from a standard NetworkX Graph with edge layer attributes."""
        m_graph = cls(layer_attr=layer_attr)
        for n in graph.nodes():
            m_graph.add_node(n)

        for u, v, data in graph.edges(data=True):
            layer = data.get(layer_attr, "default")
            m_graph.add_edge(u, v, layer=layer, **data)

        return m_graph


def compute_layerwise_core_numbers(
    multiplex_graph: MultiplexGraph
) -> Dict[str, Dict[Any, int]]:
    """
    Computes static core numbers independently for every layer in the multiplex network.

    Returns:
        Dict mapping layer_name -> {node: core_number}.
    """
    layer_cores: Dict[str, Dict[Any, int]] = {}
    for layer in multiplex_graph.get_layers():
        g_l = multiplex_graph.get_layer_subgraph(layer)
        layer_cores[layer] = compute_core_numbers_batagelj_zaversnik(g_l)
    return layer_cores


def compute_composite_multiplex_kcore(
    multiplex_graph: MultiplexGraph,
    k_vector: Dict[str, int]
) -> Tuple[nx.Graph, List[Any]]:
    """
    Computes the joint composite multiplex k-core subgraph.
    A vertex v survives in the composite (k_1, k_2, ..., k_m)-core if and only if
    v has degree deg_l(v) >= k_l in each active layer l simultaneously.

    Algorithm:
    1. Initialize degree tables for each layer.
    2. Queue any vertex v that has deg_l(v) < k_l for ANY layer l.
    3. While queue is not empty:
       - Dequeue v.
       - Remove v from all active layer degree tables.
       - Decrement degrees of all neighbors of v across their respective layers.
       - If any neighbor drops below the threshold in any layer, enqueue it.
    4. Return surviving aggregate subgraph and removal order.

    Parameters:
        multiplex_graph: MultiplexGraph instance.
        k_vector: Dict mapping layer_name -> minimum required degree in that layer.

    Returns:
        (composite_subgraph, removal_order)
    """
    # Active nodes
    all_nodes = set(multiplex_graph.nodes)
    if not all_nodes:
        return nx.Graph(), []

    # Map per-layer adjacencies
    layer_adjs: Dict[str, Dict[Any, Set[Any]]] = {}
    layer_degs: Dict[str, Dict[Any, int]] = {}
    
    for layer, k_thresh in k_vector.items():
        g_l = multiplex_graph.get_layer_subgraph(layer)
        layer_adjs[layer] = {n: set(g_l.neighbors(n)) for n in all_nodes}
        layer_degs[layer] = {n: len(layer_adjs[layer][n]) for n in all_nodes}

    removed_set: Set[Any] = set()
    removal_order: List[Any] = []

    # Find initial violations across any layer
    queue: List[Any] = []
    queued_set: Set[Any] = set()

    for n in all_nodes:
        for layer, k_thresh in k_vector.items():
            if layer_degs[layer][n] < k_thresh:
                queue.append(n)
                queued_set.add(n)
                break

    while queue:
        u = queue.pop(0)
        removal_order.append(u)
        removed_set.add(u)

        # Update neighbors in every layer
        for layer, k_thresh in k_vector.items():
            for nbr in layer_adjs[layer][u]:
                if nbr not in removed_set:
                    layer_degs[layer][nbr] -= 1
                    if layer_degs[layer][nbr] < k_thresh and nbr not in queued_set:
                        queue.append(nbr)
                        queued_set.add(nbr)

    surviving_nodes = [n for n in all_nodes if n not in removed_set]
    aggregate = multiplex_graph.get_aggregate_graph(selected_layers=list(k_vector.keys()))
    composite_subgraph = aggregate.subgraph(surviving_nodes).copy()
    
    return composite_subgraph, removal_order
