"""
Glass Bead Game v26 — Graph Pathfinder
Finds paths through the knowledge graph using BFS and A* search.
"""
import heapq
from typing import Dict, List, Any, Optional, Tuple
from collections import deque


class GraphPathfinder:
    """Find shortest paths in the Glass Bead Game knowledge graph."""

    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, Dict[str, Any]] = {}
        self._adj: Dict[str, List[Tuple[str, float, str]]] = {}  # node_id -> [(neighbor, weight, edge_id)]

    def add_node(self, node: Dict[str, Any]) -> str:
        """Add a node to the graph."""
        node_id = node.get('id')
        if not node_id:
            raise ValueError("Node must have an 'id' field")
        self.nodes[node_id] = node
        if node_id not in self._adj:
            self._adj[node_id] = []
        return node_id

    def add_edge(self, edge: Dict[str, Any]) -> str:
        """Add an edge to the graph. Weight = 1 / confidence."""
        edge_id = edge.get('id')
        if not edge_id:
            raise ValueError("Edge must have an 'id' field")
        source = edge.get('source')
        target = edge.get('target')
        if source not in self.nodes or target not in self.nodes:
            raise ValueError("Edge source and target must be existing nodes")

        confidence = edge.get('strength', 0.5)
        if confidence <= 0:
            confidence = 0.001
        weight = 1.0 / confidence

        self.edges[edge_id] = edge
        self._adj.setdefault(source, []).append((target, weight, edge_id))
        self._adj.setdefault(target, []).append((source, weight, edge_id))
        return edge_id

    def bfs_shortest_path(self, start_id: str, goal_id: str) -> Optional[Dict[str, Any]]:
        """
        BFS shortest path (unweighted) between two node IDs.
        Returns path_nodes, path_edges, total_confidence, narrative.
        """
        if start_id not in self.nodes or goal_id not in self.nodes:
            return None
        if start_id == goal_id:
            return self._build_result([start_id], [], 0.0)

        visited = {start_id}
        queue = deque([(start_id, [start_id], [])])

        while queue:
            current, path_nodes, path_edges = queue.popleft()

            for neighbor, _weight, edge_id in self._adj.get(current, []):
                if neighbor in visited:
                    continue
                new_nodes = path_nodes + [neighbor]
                new_edges = path_edges + [edge_id]
                if neighbor == goal_id:
                    return self._build_result(new_nodes, new_edges, self._sum_confidence(new_edges))
                visited.add(neighbor)
                queue.append((neighbor, new_nodes, new_edges))

        return None

    def astar_shortest_path(self, start_id: str, goal_id: str) -> Optional[Dict[str, Any]]:
        """
        A* shortest path with edge weight = 1 / confidence.
        Uses zero heuristic (equivalent to Dijkstra).
        Returns path_nodes, path_edges, total_confidence, narrative.
        """
        if start_id not in self.nodes or goal_id not in self.nodes:
            return None
        if start_id == goal_id:
            return self._build_result([start_id], [], 0.0)

        # Dijkstra / A* with h=0
        dist = {node_id: float('inf') for node_id in self.nodes}
        dist[start_id] = 0.0
        prev = {}  # node_id -> (prev_node, edge_id)
        heap = [(0.0, start_id)]
        visited_set = set()

        while heap:
            cost, current = heapq.heappop(heap)
            if current in visited_set:
                continue
            visited_set.add(current)
            if current == goal_id:
                break
            for neighbor, weight, edge_id in self._adj.get(current, []):
                if neighbor in visited_set:
                    continue
                new_cost = cost + weight
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = (current, edge_id)
                    heapq.heappush(heap, (new_cost, neighbor))

        if goal_id not in prev and start_id != goal_id:
            return None

        # Reconstruct path
        path_nodes = []
        path_edges = []
        cur = goal_id
        while cur != start_id:
            path_nodes.append(cur)
            prev_node, edge_id = prev[cur]
            path_edges.append(edge_id)
            cur = prev_node
        path_nodes.append(start_id)
        path_nodes.reverse()
        path_edges.reverse()

        return self._build_result(path_nodes, path_edges, self._sum_confidence(path_edges))

    def _sum_confidence(self, edge_ids: List[str]) -> float:
        """Sum confidence values for a list of edge IDs."""
        total = 0.0
        for eid in edge_ids:
            edge = self.edges.get(eid, {})
            total += edge.get('strength', 0.5)
        return round(total, 3)

    def _build_result(self, path_nodes: List[str], path_edges: List[str], total_confidence: float) -> Dict[str, Any]:
        """Build the standard result dict including narrative."""
        narrative = self._build_narrative(path_nodes, path_edges)
        return {
            'path_nodes': path_nodes,
            'path_edges': path_edges,
            'total_confidence': total_confidence,
            'narrative': narrative,
        }

    def _build_narrative(self, path_nodes: List[str], path_edges: List[str]) -> str:
        """Build a narrative string joining language threads across the path."""
        if not path_nodes:
            return "No path found."
        if len(path_nodes) == 1:
            node = self.nodes[path_nodes[0]]
            return f"Resting in {node.get('domain', 'unknown')}."

        parts = []
        for i, node_id in enumerate(path_nodes):
            node = self.nodes[node_id]
            domain = node.get('domain', 'unknown')
            if i == 0:
                parts.append(f"From {domain}")
            elif i == len(path_nodes) - 1:
                parts.append(f"to {domain}")
            else:
                edge_id = path_edges[i - 1] if i - 1 < len(path_edges) else None
                edge_label = ""
                if edge_id and edge_id in self.edges:
                    edge_label = self.edges[edge_id].get('label', '')
                if edge_label:
                    parts.append(f"through {domain} via '{edge_label}'")
                else:
                    parts.append(f"through {domain}")

        return " → ".join(parts)

    def find_path(self, start_id: str, goal_id: str) -> Dict[str, Any]:
        """Find a path and return in the standard API format."""
        result = self.bfs_shortest_path(start_id, goal_id)
        if result is None:
            return {"path": [], "confidence": 0.0, "narrative": "No path found."}
        # Map to the JS panel format
        path_labels = []
        for node_id in result["path_nodes"]:
            node = self.nodes.get(node_id, {})
            path_labels.append(node.get("label", node_id))
        return {
            "path": path_labels,
            "confidence": result["total_confidence"],
            "narrative": result["narrative"],
        }

    @classmethod
    def from_seed(cls) -> 'GraphPathfinder':
        """Seed the pathfinder with the demo 8 nodes from app.py."""
        pf = cls()
        domains = [
            'musica', 'mathematica', 'historia', 'natura',
            'lingua', 'philosophia', 'technologia', 'medicina',
            'coda'
        ]
        bead_names = {
            'musica': 'Magister Musicae',
            'mathematica': 'Magister Mathematicae',
            'historia': 'Magister Historiae',
            'natura': 'Magister Naturae',
            'lingua': 'Magister Linguae',
            'philosophia': 'Magister Philosophiae',
            'technologia': 'Magister Technologiae',
            'medicina': 'Magister Medicinae',
            'coda': 'Magister Codae',
        }
        colors = {
            'musica': '#00e5ff',
            'mathematica': '#ff00ff',
            'historia': '#ffd700',
            'natura': '#00ff7f',
            'lingua': '#ff6b6b',
            'philosophia': '#9370db',
            'technologia': '#ffa500',
            'medicina': '#ff69b4',
            'coda': '#39ff14',
        }

        for i, domain in enumerate(domains):
            node = {
                'id': f'node_{i}',
                'domain': domain,
                'label': bead_names[domain],
                'color': colors[domain],
                'size': 0.8,
            }
            pf.add_node(node)

        for i in range(len(domains)):
            j = (i + 1) % len(domains)
            edge = {
                'id': f'edge_{i}_{j}',
                'source': f'node_{i}',
                'target': f'node_{j}',
                'strength': 0.5,
                'label': f'{domains[i]} → {domains[j]}',
            }
            pf.add_edge(edge)

        return pf
