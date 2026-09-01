"""
Efficient Core-Number Computation Module (FR-3 & FR-4).
Implements the Batagelj-Zaversnik O(V + E) algorithm from scratch using
bucket sort and positional arrays, with validation against NetworkX reference oracle.
"""

from typing import Dict, List, Tuple, Any, Optional
import networkx as nx


def compute_core_numbers_batagelj_zaversnik(graph: nx.Graph) -> Dict[Any, int]:
    """
    Computes exact core numbers for every vertex in O(V + E) time using the
    Batagelj-Zaversnik (2003) algorithm.

    Asymptotic Complexity:
    - Time: O(|V| + |E|) linear in graph size.
    - Space: O(|V| + |E|) for positional arrays and adjacency lists.

    Data Structures:
    - vert: Array storing vertices ordered by ascending degree.
    - pos: Array storing the index position of each vertex in `vert`.
    - deg: Array storing the active effective degree of each vertex.
    - bin: Array storing the starting index in `vert` for each degree bucket.

    Parameters:
        graph: Input networkx.Graph.

    Returns:
        Dict mapping node -> core number c(v).
    """
    nodes = list(graph.nodes())
    n = len(nodes)
    if n == 0:
        return {}

    # Map node labels to continuous integer indices 0..n-1 for array indexing
    node_to_idx: Dict[Any, int] = {node: i for i, node in enumerate(nodes)}
    idx_to_node: List[Any] = nodes

    # Construct integer adjacency lists
    adj: List[List[int]] = [[] for _ in range(n)]
    for u, v in graph.edges():
        ui = node_to_idx[u]
        vi = node_to_idx[v]
        adj[ui].append(vi)
        adj[vi].append(ui)

    # 1. Compute initial degrees and determine maximum degree
    deg: List[int] = [len(adj[i]) for i in range(n)]
    max_deg = max(deg) if n > 0 else 0

    # 2. Count degrees to establish bin boundaries (Counting Sort in O(V))
    bin_counts = [0] * (max_deg + 1)
    for d in deg:
        bin_counts[d] += 1

    # Cumulative sum to determine starting index of each bin in `vert`
    bin_start = [0] * (max_deg + 1)
    start = 0
    for d in range(max_deg + 1):
        bin_start[d] = start
        start += bin_counts[d]

    # 3. Populate `vert` (sorted vertices) and `pos` (positions) in O(V)
    # Temporary array to track current write pointer within each bin
    bin_pos = list(bin_start)
    vert = [0] * n
    pos = [0] * n
    for v in range(n):
        d = deg[v]
        p = bin_pos[d]
        vert[p] = v
        pos[v] = p
        bin_pos[d] += 1

    # 4. Sequentially peel vertices in O(V + E)
    for i in range(n):
        v = vert[i]
        # Core number of v is established as its degree at time of extraction
        for u in adj[v]:
            if deg[u] > deg[v]:
                # Decrement deg[u] with O(1) bin shift
                du = deg[u]
                pu = pos[u]
                pw = bin_start[du]  # Position of first vertex with degree du
                w = vert[pw]

                if u != w:
                    # Swap positions of u and w in vert array
                    vert[pu] = w
                    vert[pw] = u
                    pos[u] = pw
                    pos[w] = pu

                # Advance bin boundary and decrement degree of u
                bin_start[du] += 1
                deg[u] -= 1

    # Map indices back to original node labels
    core_numbers: Dict[Any, int] = {idx_to_node[v]: deg[v] for v in range(n)}
    return core_numbers


def validate_against_networkx(
    graph: nx.Graph,
    computed_cores: Optional[Dict[Any, int]] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    FR-4: Validates custom computed core numbers against NetworkX's reference oracle.

    Parameters:
        graph: Input networkx.Graph.
        computed_cores: Optional pre-computed core dictionary. If None, computes via Batagelj-Zaversnik.

    Returns:
        (is_valid, report): True if all node core numbers match exactly; diagnostic report dictionary.
    """
    if computed_cores is None:
        computed_cores = compute_core_numbers_batagelj_zaversnik(graph)

    reference_cores = nx.core_number(graph)
    
    mismatches: List[Dict[str, Any]] = []
    for node in graph.nodes():
        c_comp = computed_cores.get(node)
        c_ref = reference_cores.get(node)
        if c_comp != c_ref:
            mismatches.append({
                "node": node,
                "computed": c_comp,
                "reference": c_ref
            })

    is_valid = len(mismatches) == 0
    report = {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "is_valid": is_valid,
        "num_mismatches": len(mismatches),
        "mismatches": mismatches
    }
    return is_valid, report


def extract_kcore_subgraph(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    k: int
) -> nx.Graph:
    """
    Extracts the k-core subgraph induced on vertices with core number c(v) >= k.

    Parameters:
        graph: Input networkx.Graph.
        core_numbers: Dict mapping node -> core number.
        k: Integer threshold.

    Returns:
        Induced subgraph networkx.Graph.
    """
    k_nodes = [node for node, c in core_numbers.items() if c >= k]
    return graph.subgraph(k_nodes).copy()
