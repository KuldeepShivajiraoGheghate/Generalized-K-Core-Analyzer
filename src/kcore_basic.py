"""
Static K-Core Decomposition - Basic / Naive Algorithm (FR-2).
Implements the iterative node-removal (peeling) algorithm from scratch
using adjacency list representations.
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import networkx as nx


def compute_kcore_subgraph_naive(
    graph: nx.Graph,
    k: int
) -> Tuple[nx.Graph, List[Any]]:
    """
    Computes the k-core subgraph for a specific integer k using iterative removal.

    Algorithm:
    1. Initialize degree map for all active nodes in graph.
    2. Queue all vertices with degree < k.
    3. While queue is not empty:
       - Dequeue vertex v.
       - Remove v from active graph.
       - Decrement degrees of all active neighbors of v.
       - If any neighbor's degree drops below k, add it to the removal queue.
    4. Return the induced subgraph on remaining active nodes and the removal sequence.

    Parameters:
        graph: Input networkx.Graph.
        k: Integer core threshold.

    Returns:
        (kcore_subgraph, removal_order): Induced k-core subgraph and list of removed nodes in order.
    """
    if k <= 0:
        return graph.copy(), []

    # Build adjacency dictionary from input graph
    adj: Dict[Any, Set[Any]] = {node: set(graph.neighbors(node)) for node in graph.nodes()}
    degrees: Dict[Any, int] = {node: len(adj[node]) for node in adj}
    
    removal_order: List[Any] = []
    removed_set: Set[Any] = set()

    # Find initial nodes with degree < k
    queue: List[Any] = [node for node, deg in degrees.items() if deg < k]
    queued_set: Set[Any] = set(queue)

    while queue:
        u = queue.pop(0)
        removal_order.append(u)
        removed_set.add(u)

        # Update neighbors of u
        for neighbor in adj[u]:
            if neighbor not in removed_set:
                degrees[neighbor] -= 1
                if degrees[neighbor] < k and neighbor not in queued_set:
                    queue.append(neighbor)
                    queued_set.add(neighbor)

    # Construct the resulting k-core subgraph from remaining nodes
    remaining_nodes = [node for node in graph.nodes() if node not in removed_set]
    kcore_subgraph = graph.subgraph(remaining_nodes).copy()
    
    return kcore_subgraph, removal_order


def compute_core_numbers_naive(graph: nx.Graph) -> Dict[Any, int]:
    """
    Computes exact core numbers for all nodes using iterative naive decomposition.
    Iterates k from 1 up to maximum possible degree, identifying nodes surviving at each stage.

    Parameters:
        graph: Input networkx.Graph.

    Returns:
        Dict mapping node -> core number c(v).
    """
    if graph.number_of_nodes() == 0:
        return {}

    # Initialize all node core numbers to 0
    core_numbers: Dict[Any, int] = {node: 0 for node in graph.nodes()}
    max_deg = max((d for _, d in graph.degree()), default=0)

    current_subgraph = graph.copy()

    for k in range(1, max_deg + 2):
        if current_subgraph.number_of_nodes() == 0:
            break
        
        # Naive peel current subgraph at threshold k
        kcore_sub, removed = compute_kcore_subgraph_naive(current_subgraph, k)
        
        # Nodes surviving in kcore_subgraph belong to at least k-core
        for node in kcore_sub.nodes():
            core_numbers[node] = k

        current_subgraph = kcore_sub

    return core_numbers
