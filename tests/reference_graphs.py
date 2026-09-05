"""
Reference Graphs for Unit Testing and Ground-Truth Validation (Phase 2).

Provides hand-crafted, mathematically verified reference graphs across
various standard topologies:
1. Path Graph (P5)
2. Cycle Graph (C5)
3. Star Graph (S5)
4. Complete Graph (K4)
5. Complete Graph (K5)
6. Disconnected Multi-Component Graph (Triangle K3 + Path P3)
7. Tree Graph (Binary Tree)
8. Multi-Core Hierarchy Graph (Custom Graph with core numbers 1, 2, and 3)
"""

from typing import Dict, List, Set, Tuple, Any

REFERENCE_GRAPHS: Dict[str, Dict[str, Any]] = {
    "path_5": {
        "description": "Linear Path Graph P5: 0-1-2-3-4",
        "nodes": [0, 1, 2, 3, 4],
        "edges": [(0, 1), (1, 2), (2, 3), (3, 4)],
        "node_count": 5,
        "edge_count": 4,
        "min_degree": 1,
        "max_degree": 2,
        "avg_degree": 1.6,
        "connected_components": 1,
        "degrees": {0: 1, 1: 2, 2: 2, 3: 2, 4: 1},
        # Theoretical k-cores:
        # k=1: All nodes (deg >= 1)
        # k=2: Empty (leaf nodes 0, 4 pruned -> degree of 1, 3 becomes 1 -> pruned -> all pruned)
        "k_cores": {
            1: [0, 1, 2, 3, 4],
            2: [],
            3: []
        },
        "core_numbers": {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
        "degeneracy": 1
    },
    "cycle_5": {
        "description": "Simple Cycle Graph C5: 0-1-2-3-4-0",
        "nodes": [0, 1, 2, 3, 4],
        "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)],
        "node_count": 5,
        "edge_count": 5,
        "min_degree": 2,
        "max_degree": 2,
        "avg_degree": 2.0,
        "connected_components": 1,
        "degrees": {0: 2, 1: 2, 2: 2, 3: 2, 4: 2},
        # k=1: All nodes
        # k=2: All nodes (all degree 2)
        # k=3: Empty
        "k_cores": {
            1: [0, 1, 2, 3, 4],
            2: [0, 1, 2, 3, 4],
            3: []
        },
        "core_numbers": {0: 2, 1: 2, 2: 2, 3: 2, 4: 2},
        "degeneracy": 2
    },
    "star_5": {
        "description": "Star Graph S5: Center 0 connected to leaves 1, 2, 3, 4",
        "nodes": [0, 1, 2, 3, 4],
        "edges": [(0, 1), (0, 2), (0, 3), (0, 4)],
        "node_count": 5,
        "edge_count": 4,
        "min_degree": 1,
        "max_degree": 4,
        "avg_degree": 1.6,
        "connected_components": 1,
        "degrees": {0: 4, 1: 1, 2: 1, 3: 1, 4: 1},
        # k=1: All nodes
        # k=2: Empty (leaves pruned -> center degree becomes 0 -> pruned)
        "k_cores": {
            1: [0, 1, 2, 3, 4],
            2: [],
            3: []
        },
        "core_numbers": {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
        "degeneracy": 1
    },
    "complete_4": {
        "description": "Complete Graph K4 (4 nodes, 6 edges)",
        "nodes": [0, 1, 2, 3],
        "edges": [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
        "node_count": 4,
        "edge_count": 6,
        "min_degree": 3,
        "max_degree": 3,
        "avg_degree": 3.0,
        "connected_components": 1,
        "degrees": {0: 3, 1: 3, 2: 3, 3: 3},
        # k=1, 2, 3: All nodes
        # k=4: Empty
        "k_cores": {
            1: [0, 1, 2, 3],
            2: [0, 1, 2, 3],
            3: [0, 1, 2, 3],
            4: []
        },
        "core_numbers": {0: 3, 1: 3, 2: 3, 3: 3},
        "degeneracy": 3
    },
    "complete_5": {
        "description": "Complete Graph K5 (5 nodes, 10 edges)",
        "nodes": [0, 1, 2, 3, 4],
        "edges": [
            (0, 1), (0, 2), (0, 3), (0, 4),
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4),
            (3, 4)
        ],
        "node_count": 5,
        "edge_count": 10,
        "min_degree": 4,
        "max_degree": 4,
        "avg_degree": 4.0,
        "connected_components": 1,
        "degrees": {0: 4, 1: 4, 2: 4, 3: 4, 4: 4},
        "k_cores": {
            1: [0, 1, 2, 3, 4],
            2: [0, 1, 2, 3, 4],
            3: [0, 1, 2, 3, 4],
            4: [0, 1, 2, 3, 4],
            5: []
        },
        "core_numbers": {0: 4, 1: 4, 2: 4, 3: 4, 4: 4},
        "degeneracy": 4
    },
    "disconnected_k3_p3": {
        "description": "Disconnected Graph: Triangle (0, 1, 2) and Path (3, 4, 5)",
        "nodes": [0, 1, 2, 3, 4, 5],
        "edges": [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5)],
        "node_count": 6,
        "edge_count": 4 + 1,  # 3 in K3, 2 in P3 = 5
        "min_degree": 1,
        "max_degree": 2,
        "avg_degree": 1.6666666666666667,
        "connected_components": 2,
        "degrees": {0: 2, 1: 2, 2: 2, 3: 1, 4: 2, 5: 1},
        # k=1: All nodes [0, 1, 2, 3, 4, 5]
        # k=2: Triangle [0, 1, 2]
        # k=3: Empty
        "k_cores": {
            1: [0, 1, 2, 3, 4, 5],
            2: [0, 1, 2],
            3: []
        },
        "core_numbers": {0: 2, 1: 2, 2: 2, 3: 1, 4: 1, 5: 1},
        "degeneracy": 2
    },
    "hierarchy_graph": {
        "description": "Multi-shell hierarchy: K4 core (0,1,2,3) attached to triangle (4,5) attached to antenna (6)",
        # 0,1,2,3 form K4 with each other.
        # 4 is connected to 0, 1, 5. 5 is connected to 0, 4. (triangle 0, 4, 5)
        # 6 is connected to 5. (antenna)
        "nodes": [0, 1, 2, 3, 4, 5, 6],
        "edges": [
            (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), # K4 among 0,1,2,3
            (0, 4), (1, 4), (4, 5), (0, 5),                 # 4 attached to 0,1,5; 5 attached to 0,4
            (5, 6)                                          # leaf 6 attached to 5
        ],
        "node_count": 7,
        "edge_count": 11,
        "min_degree": 1,
        "max_degree": 5, # node 0: 1, 2, 3, 4, 5 -> deg 5
        "avg_degree": 3.142857142857143,
        "connected_components": 1,
        "degrees": {0: 5, 1: 4, 2: 3, 3: 3, 4: 3, 5: 3, 6: 1},
        # k=1: [0, 1, 2, 3, 4, 5, 6]
        # k=2: [0, 1, 2, 3, 4, 5] (6 removed)
        # k=3: [0, 1, 2, 3] (after 6 removed, 5 has deg 2 -> removed -> 4 has deg 2 -> removed -> {0,1,2,3} remain, all deg 3)
        # k=4: [] (0 has deg 3 in {0,1,2,3}, none have deg 4)
        "k_cores": {
            1: [0, 1, 2, 3, 4, 5, 6],
            2: [0, 1, 2, 3, 4, 5],
            3: [0, 1, 2, 3],
            4: []
        },
        "core_numbers": {0: 3, 1: 3, 2: 3, 3: 3, 4: 2, 5: 2, 6: 1},
        "degeneracy": 3
    }
}


def build_adj_list(nodes: List[Any], edges: List[Tuple[Any, Any]]) -> Dict[Any, Set[Any]]:
    """Builds an undirected adjacency list from nodes and edge list."""
    adj: Dict[Any, Set[Any]] = {u: set() for u in nodes}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def get_reference_graph(name: str) -> Dict[str, Any]:
    """Returns the dictionary for a specific reference graph."""
    if name not in REFERENCE_GRAPHS:
        raise KeyError(f"Unknown reference graph: {name}. Available: {list(REFERENCE_GRAPHS.keys())}")
    return REFERENCE_GRAPHS[name]
