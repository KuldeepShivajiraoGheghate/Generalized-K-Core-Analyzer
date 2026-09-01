"""
Dynamic Graph Mutation and Incremental K-Core Maintenance Module (FR-5, FR-6, FR-7).
Provides single-edge graph mutations, candidate vertex set identification,
full recomputation baseline, and localized incremental core maintenance.
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import time
import networkx as nx
from src.kcore_efficient import compute_core_numbers_batagelj_zaversnik


def add_edge_dynamic(
    graph: nx.Graph,
    u: Any,
    v: Any,
    **edge_attrs
) -> Tuple[nx.Graph, bool]:
    """
    FR-5: Inserts an undirected edge (u, v) into the graph.
    Returns (graph, is_new_edge).
    """
    if u not in graph:
        graph.add_node(u)
    if v not in graph:
        graph.add_node(v)
        
    is_new = not graph.has_edge(u, v)
    graph.add_edge(u, v, **edge_attrs)
    return graph, is_new


def remove_edge_dynamic(
    graph: nx.Graph,
    u: Any,
    v: Any
) -> Tuple[nx.Graph, bool]:
    """
    FR-5: Removes an undirected edge (u, v) from the graph if it exists.
    Returns (graph, edge_existed).
    """
    if graph.has_edge(u, v):
        graph.remove_edge(u, v)
        return graph, True
    return graph, False


def identify_candidate_subgraph_addition(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    u: Any,
    v: Any
) -> Tuple[int, Set[Any]]:
    """
    Identifies the candidate vertex set that could theoretically increase core number
    after adding edge (u, v).

    Theory:
    Let K = min(c(u), c(v)). Only vertices with initial core number equal to K
    that are reachable from u or v within the K-core subgraph can increase their core number to K+1.

    Returns:
        (K, candidate_set): The target core level K and set of candidate vertex IDs.
    """
    cu = core_numbers.get(u, 0)
    cv = core_numbers.get(v, 0)
    K = min(cu, cv)

    start_nodes = []
    if cu == K:
        start_nodes.append(u)
    if cv == K:
        start_nodes.append(v)

    if not start_nodes:
        return K, set()

    # Traverse within vertices having core number >= K to find K-shell connected candidates
    candidates: Set[Any] = set()
    visited: Set[Any] = set()
    queue = list(start_nodes)

    for node in start_nodes:
        visited.add(node)
        if core_numbers.get(node) == K:
            candidates.add(node)

    while queue:
        curr = queue.pop(0)
        for nbr in graph.neighbors(curr):
            nbr_core = core_numbers.get(nbr, 0)
            if nbr_core >= K and nbr not in visited:
                visited.add(nbr)
                if nbr_core == K:
                    candidates.add(nbr)
                    queue.append(nbr)

    return K, candidates


def identify_candidate_subgraph_deletion(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    u: Any,
    v: Any
) -> Tuple[int, Set[Any]]:
    """
    Identifies the candidate vertex set that could theoretically decrease core number
    after removing edge (u, v).

    Theory:
    Let K = min(c(u), c(v)). Only vertices with initial core number equal to K
    that were supported by the deleted connection can decrease their core number to K-1.

    Returns:
        (K, candidate_set): The target core level K and set of candidate vertex IDs.
    """
    cu = core_numbers.get(u, 0)
    cv = core_numbers.get(v, 0)
    K = min(cu, cv)

    start_nodes = []
    if cu == K:
        start_nodes.append(u)
    if cv == K:
        start_nodes.append(v)

    candidates: Set[Any] = set()
    visited: Set[Any] = set()
    queue = list(start_nodes)

    for node in start_nodes:
        visited.add(node)
        if core_numbers.get(node) == K:
            candidates.add(node)

    while queue:
        curr = queue.pop(0)
        for nbr in graph.neighbors(curr):
            nbr_core = core_numbers.get(nbr, 0)
            if nbr_core >= K and nbr not in visited:
                visited.add(nbr)
                if nbr_core == K:
                    candidates.add(nbr)
                    queue.append(nbr)

    return K, candidates


def full_recompute_core_numbers(
    graph: nx.Graph
) -> Tuple[Dict[Any, int], float]:
    """
    FR-6: Full recomputation baseline.
    Executes Batagelj-Zaversnik across the entire graph and measures wall-clock runtime.

    Returns:
        (core_numbers, execution_time_seconds)
    """
    t0 = time.perf_counter()
    cores = compute_core_numbers_batagelj_zaversnik(graph)
    t1 = time.perf_counter()
    return cores, (t1 - t0)


def maintain_kcore_edge_addition(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    u: Any,
    v: Any
) -> Tuple[Dict[Any, int], Set[Any], float]:
    """
    FR-7: Incremental maintenance of core numbers following the insertion of edge (u, v).

    Algorithm:
    1. Identify candidate set V_c of nodes in shell K = min(c(u), c(v)).
    2. Compute local effective degree deg_K(w) for all w in V_c (neighbors with core > K or in V_c).
    3. Prune candidate vertices with deg_K(w) <= K iteratively.
    4. Remaining candidates satisfy deg_K(w) >= K + 1 and upgrade their core number: c(w) <- K + 1.

    Returns:
        (updated_core_numbers, modified_nodes, execution_time_seconds)
    """
    t0 = time.perf_counter()
    cores = dict(core_numbers)
    
    # Ensure u and v exist in cores
    if u not in cores:
        cores[u] = 0
    if v not in cores:
        cores[v] = 0

    cu = cores[u]
    cv = cores[v]
    K = min(cu, cv)

    K, candidate_set = identify_candidate_subgraph_addition(graph, cores, u, v)
    
    if not candidate_set:
        t1 = time.perf_counter()
        return cores, set(), (t1 - t0)

    # Compute effective degree for each candidate node
    # Effective degree = count of neighbors with core > K, plus count of candidate neighbors in V_c
    cand_nodes = set(candidate_set)
    eff_deg: Dict[Any, int] = {}
    for w in cand_nodes:
        d = 0
        for nbr in graph.neighbors(w):
            nbr_c = cores.get(nbr, 0)
            if nbr_c > K or nbr in cand_nodes:
                d += 1
        eff_deg[w] = d

    # Iteratively prune candidate nodes with effective degree <= K (they cannot upgrade to K+1)
    prune_queue = [w for w in cand_nodes if eff_deg[w] <= K]
    pruned_set: Set[Any] = set(prune_queue)

    while prune_queue:
        curr = prune_queue.pop(0)
        for nbr in graph.neighbors(curr):
            if nbr in cand_nodes and nbr not in pruned_set:
                eff_deg[nbr] -= 1
                if eff_deg[nbr] <= K:
                    pruned_set.add(nbr)
                    prune_queue.append(nbr)

    # Surviving candidate nodes have at least K+1 qualifying connections -> upgrade core to K+1
    upgraded_nodes: Set[Any] = set()
    for w in cand_nodes:
        if w not in pruned_set:
            cores[w] = K + 1
            upgraded_nodes.add(w)

    t1 = time.perf_counter()
    return cores, upgraded_nodes, (t1 - t0)


def maintain_kcore_edge_deletion(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    u: Any,
    v: Any
) -> Tuple[Dict[Any, int], Set[Any], float]:
    """
    FR-7: Incremental maintenance of core numbers following the removal of edge (u, v).

    Algorithm:
    1. Identify candidate set V_c of nodes in shell K = min(c(u), c(v)).
    2. Compute support degree sup_K(w) = count of neighbors with core >= K.
    3. If any node w in candidate set has sup_K(w) < K, downgrade w: c(w) <- K - 1.
    4. Propagate support reductions to neighbors and repeat until stable.

    Returns:
        (updated_core_numbers, modified_nodes, execution_time_seconds)
    """
    t0 = time.perf_counter()
    cores = dict(core_numbers)

    cu = cores.get(u, 0)
    cv = cores.get(v, 0)
    K = min(cu, cv)

    K, candidate_set = identify_candidate_subgraph_deletion(graph, cores, u, v)

    if not candidate_set or K == 0:
        t1 = time.perf_counter()
        return cores, set(), (t1 - t0)

    # Compute support degree for candidate nodes: count of neighbors with core >= K
    cand_nodes = set(candidate_set)
    support_deg: Dict[Any, int] = {}
    for w in cand_nodes:
        d = sum(1 for nbr in graph.neighbors(w) if cores.get(nbr, 0) >= K)
        support_deg[w] = d

    downgraded_nodes: Set[Any] = set()
    downgrade_queue = [w for w in cand_nodes if support_deg[w] < K]
    queued_set: Set[Any] = set(downgrade_queue)

    while downgrade_queue:
        curr = downgrade_queue.pop(0)
        cores[curr] = K - 1
        downgraded_nodes.add(curr)

        for nbr in graph.neighbors(curr):
            if nbr in cand_nodes and nbr not in queued_set:
                support_deg[nbr] -= 1
                if support_deg[nbr] < K:
                    queued_set.add(nbr)
                    downgrade_queue.append(nbr)

    t1 = time.perf_counter()
    return cores, downgraded_nodes, (t1 - t0)


def apply_dynamic_mutation_and_maintain(
    graph: nx.Graph,
    core_numbers: Dict[Any, int],
    mutation_type: str,
    u: Any,
    v: Any,
    **edge_attrs
) -> Dict[str, Any]:
    """
    Consolidated dynamic mutation runner: applies mutation, executes both full recompute
    and incremental maintenance, and asserts consistency.

    Parameters:
        graph: nx.Graph (mutated in-place or updated).
        core_numbers: Current core numbers dictionary.
        mutation_type: 'add' or 'remove'.
        u, v: Edge endpoints.

    Returns:
        Dict with updated_cores, modified_nodes, incremental_time, full_recompute_time, is_consistent.
    """
    mutation_type = mutation_type.lower()
    
    if mutation_type in ("add", "insert"):
        add_edge_dynamic(graph, u, v, **edge_attrs)
        inc_cores, modified, inc_time = maintain_kcore_edge_addition(graph, core_numbers, u, v)
    elif mutation_type in ("remove", "delete"):
        remove_edge_dynamic(graph, u, v)
        inc_cores, modified, inc_time = maintain_kcore_edge_deletion(graph, core_numbers, u, v)
    else:
        raise ValueError(f"Unknown mutation_type: {mutation_type}")

    # Full recompute validation
    full_cores, full_time = full_recompute_core_numbers(graph)
    
    # Assert consistency
    is_consistent = (inc_cores == full_cores)

    return {
        "updated_cores": inc_cores,
        "modified_nodes": modified,
        "num_modified_nodes": len(modified),
        "incremental_time_sec": inc_time,
        "full_recompute_time_sec": full_time,
        "speedup": (full_time / inc_time) if inc_time > 0 else 1.0,
        "is_consistent": is_consistent
    }
