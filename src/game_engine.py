"""
glass-bead-game-v26 — Game Engine
Core game logic: graph management, move validation, scoring, rank progression.
"""
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any


class KnowledgeGraph:
    """The Glass Bead Game board — a living knowledge graph."""
    
    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self._node_map: Dict[str, Dict] = {}  # id -> node
        self._domain_index: Dict[str, List[str]] = {}  # domain -> [node_ids]
    
    def add_node(self, node: Dict[str, Any]) -> str:
        """Add a concept node to the graph. Returns node id."""
        if 'id' not in node:
            node['id'] = f"node_{len(self.nodes)}_{int(datetime.utcnow().timestamp())}"
        
        self.nodes.append(node)
        self._node_map[node['id']] = node
        
        domain = node.get('domain', 'unknown')
        if domain not in self._domain_index:
            self._domain_index[domain] = []
        self._domain_index[domain].append(node['id'])
        
        return node['id']
    
    def add_edge(self, edge: Dict[str, Any]) -> str:
        """Add a resonance edge between nodes. Returns edge id."""
        if 'id' not in edge:
            edge['id'] = f"edge_{edge.get('source','x')}_{edge.get('target','y')}"
        
        self.edges.append(edge)
        return edge['id']
    
    def get_node(self, node_id: str) -> Optional[Dict]:
        return self._node_map.get(node_id)
    
    def get_nodes_by_domain(self, domain: str) -> List[Dict]:
        ids = self._domain_index.get(domain, [])
        return [self._node_map[nid] for nid in ids if nid in self._node_map]
    
    def get_neighbors(self, node_id: str) -> List[Dict]:
        """Get all nodes connected to this node."""
        neighbor_ids = set()
        for edge in self.edges:
            if edge['source'] == node_id:
                neighbor_ids.add(edge['target'])
            elif edge['target'] == node_id:
                neighbor_ids.add(edge['source'])
        return [self._node_map[nid] for nid in neighbor_ids if nid in self._node_map]
    
    def get_path(self, from_id: str, to_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """Find shortest path between two nodes (BFS). Returns list of node ids."""
        if from_id == to_id:
            return [from_id]
        
        visited = {from_id}
        queue = [(from_id, [from_id])]
        
        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue
            
            for edge in self.edges:
                neighbor = None
                if edge['source'] == current:
                    neighbor = edge['target']
                elif edge['target'] == current:
                    neighbor = edge['source']
                
                if neighbor and neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == to_id:
                        return new_path
                    visited.add(neighbor)
                    queue.append((neighbor, new_path))
        
        return None
    
    def density(self) -> float:
        """Graph density: 0 (empty) to 1 (complete)."""
        n = len(self.nodes)
        if n < 2:
            return 0.0
        max_edges = n * (n - 1) / 2
        return len(self.edges) / max_edges if max_edges > 0 else 0.0
    
    def to_dict(self) -> Dict:
        return {'nodes': self.nodes, 'edges': self.edges}
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeGraph':
        g = cls()
        for node in data.get('nodes', []):
            g.add_node(node)
        for edge in data.get('edges', []):
            g.add_edge(edge)
        return g


class MoveValidator:
    """Validates Glass Bead Game moves."""
    
    DOMAINS = [
        'musica', 'mathematica', 'historia', 'natura',
        'lingua', 'philosophia', 'technologia', 'medicina'
    ]
    
    def validate(self, move: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a move. Returns:
        {
            'valid': bool,
            'reason': str,
            'elegance_score': int (1-10),
            'fertility_estimate': int,
            'domain_crossings': int,
            'structural_check': bool,
        }
        """
        from_domain = move.get('from_domain', '')
        to_domain = move.get('to_domain', '')
        via = move.get('via', '')
        resonance = move.get('resonance', '')
        
        result = {
            'valid': True,
            'reason': '',
            'elegance_score': 5,
            'fertility_estimate': 0,
            'domain_crossings': 0,
            'structural_check': True,
        }
        
        # Check domains are valid
        if from_domain not in self.DOMAINS:
            result['valid'] = False
            result['reason'] = f"Invalid from_domain: {from_domain}"
            return result
        if to_domain not in self.DOMAINS:
            result['valid'] = False
            result['reason'] = f"Invalid to_domain: {to_domain}"
            return result
        
        # Check domain crossing
        if from_domain == to_domain:
            result['valid'] = False
            result['reason'] = "Move must cross at least one domain boundary"
            result['structural_check'] = False
            return result
        
        result['domain_crossings'] = self._count_domain_crossings(from_domain, to_domain)
        
        # Check via property is substantive
        if len(via.strip()) < 10:
            result['valid'] = False
            result['reason'] = "Structural property ('via') too brief"
            result['structural_check'] = False
            return result
        
        # Check resonance is poetic
        if len(resonance.strip()) < 15:
            result['valid'] = False
            result['reason'] = "Resonance sentence too brief"
            return result
        
        # Calculate elegance: higher for fewer intermediates, greater domain distance
        domain_distance = self._domain_distance(from_domain, to_domain)
        result['elegance_score'] = min(10, max(1, domain_distance + 3))
        
        # Estimate fertility: how many new moves could this unlock
        result['fertility_estimate'] = domain_distance * 2 + random.randint(0, 3)
        
        result['reason'] = "Move structure validated"
        return result
    
    def _count_domain_crossings(self, d1: str, d2: str) -> int:
        """Count how many domain boundaries are crossed."""
        if d1 == d2:
            return 0
        idx1 = self.DOMAINS.index(d1) if d1 in self.DOMAINS else -1
        idx2 = self.DOMAINS.index(d2) if d2 in self.DOMAINS else -1
        if idx1 == -1 or idx2 == -1:
            return 1
        return abs(idx2 - idx1)
    
    def _domain_distance(self, d1: str, d2: str) -> int:
        """Semantic distance between domains."""
        # Music and math are closely related in Castalia
        related_pairs = [
            ('musica', 'mathematica'),
            ('historia', 'philosophia'),
            ('natura', 'technologia'),
            ('lingua', 'philosophia'),
        ]
        if d1 == d2:
            return 0
        if (d1, d2) in related_pairs or (d2, d1) in related_pairs:
            return 1
        return 2 + random.randint(0, 2)


class ScoringEngine:
    """Aesthetic scoring for Glass Bead Game moves."""
    
    WEIGHTS = {
        'elegance': 0.30,
        'fertility': 0.25,
        'surprise': 0.25,
        'recursion': 0.20,
    }
    
    def score(self, move: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a validated move on aesthetic criteria.
        """
        from_domain = move.get('from_domain', '')
        to_domain = move.get('to_domain', '')
        via = move.get('via', '')
        
        elegance = validation.get('elegance_score', 5)
        fertility = validation.get('fertility_estimate', 0)
        
        # Surprise: bonus for crossing >3 domains (rare)
        crossings = validation.get('domain_crossings', 0)
        surprise = min(10, crossings * 2 + 3)
        
        # Recursion: check if move references itself or earlier moves
        recursion = self._check_recursion(move)
        
        total = (
            elegance * self.WEIGHTS['elegance'] +
            fertility * self.WEIGHTS['fertility'] +
            surprise * self.WEIGHTS['surprise'] +
            recursion * self.WEIGHTS['recursion']
        )
        
        return {
            'dimensions': {
                'elegance': elegance,
                'fertility': min(10, fertility),
                'surprise': surprise,
                'recursion': recursion,
            },
            'total': round(total, 2),
            'breakdown': {
                'elegance_contrib': round(elegance * self.WEIGHTS['elegance'], 2),
                'fertility_contrib': round(min(10, fertility) * self.WEIGHTS['fertility'], 2),
                'surprise_contrib': round(surprise * self.WEIGHTS['surprise'], 2),
                'recursion_contrib': round(recursion * self.WEIGHTS['recursion'], 2),
            }
        }
    
    def _check_recursion(self, move: Dict[str, Any]) -> int:
        """Check for self-referential depth in a move."""
        via = move.get('via', '').lower()
        resonance = move.get('resonance', '').lower()
        
        score = 5  # baseline
        
        # Bonus for meta-references
        if any(word in via for word in ['self', 'recursive', 'fractal', 'loop', 'mirror']):
            score += 3
        if any(word in resonance for word in ['itself', 'returns', 'reflects', 'echoes']):
            score += 2
        
        return min(10, score)


class RankManager:
    """Manages Castalian hierarchy progression."""
    
    RANKS = ['Novice', 'Adept', 'Scholar', 'Magister Ludi']
    RANK_THRESHOLD = {
        'Novice': {'min_moves': 0, 'min_avg_score': 0},
        'Adept': {'min_moves': 3, 'min_avg_score': 15},
        'Scholar': {'min_moves': 10, 'min_avg_score': 20},
        'Magister Ludi': {'min_moves': 25, 'min_avg_score': 25},
    }
    
    def evaluate_promotion(self, player: str, move_history: List[Dict]) -> Dict[str, Any]:
        """
        Evaluate if a player qualifies for promotion.
        """
        current_rank = player.get('rank', 'Novice') if isinstance(player, dict) else 'Novice'
        current_idx = self.RANKS.index(current_rank)
        
        if current_idx >= len(self.RANKS) - 1:
            return {
                'promoted': False,
                'justification': 'Already at highest rank',
                'required_improvements': [],
            }
        
        next_rank = self.RANKS[current_idx + 1]
        threshold = self.RANK_THRESHOLD[next_rank]
        
        total_moves = len(move_history)
        if total_moves == 0:
            return {
                'promoted': False,
                'justification': 'No moves recorded',
                'required_improvements': ['Submit at least one move'],
            }
        
        avg_score = sum(m.get('total_score', 0) for m in move_history) / total_moves
        
        issues = []
        if total_moves < threshold['min_moves']:
            issues.append(f"Need {threshold['min_moves'] - total_moves} more moves")
        if avg_score < threshold['min_avg_score']:
            issues.append(f"Average score {avg_score:.1f} below threshold {threshold['min_avg_score']}")
        
        # Check for peer validation
        peer_validated = any(m.get('peer_validated', False) for m in move_history)
        if not peer_validated:
            issues.append('At least one move must be peer-validated')
        
        promoted = len(issues) == 0
        
        return {
            'promoted': promoted,
            'from_rank': current_rank,
            'to_rank': next_rank if promoted else current_rank,
            'justification': f"Eligible for {next_rank}" if promoted else f"Not yet eligible: {', '.join(issues)}",
            'required_improvements': issues,
            'stats': {
                'total_moves': total_moves,
                'avg_score': round(avg_score, 2),
                'peer_validated': peer_validated,
            }
        }


class KnechtProtocol:
    """The Hessean Warning — every game must connect to practical utility."""
    
    def review_session(self, graph: KnowledgeGraph, applications: List[str]) -> Dict[str, Any]:
        """
        Review a completed game session for Castalian sealing.
        """
        density = graph.density()
        app_count = len(applications)
        
        flagged = app_count == 0
        
        suggestion = ""
        if flagged:
            # Generate a practical application suggestion
            suggestions = [
                "Could this musical-mathematical structure inform error-correction in data transmission?",
                "Might this correspondence suggest a novel pedagogical method for teaching both subjects?",
                "Could the structural analogy inspire a new algorithmic approach to pattern recognition?",
                "Might this resonance inform clinical decision-making frameworks?",
                "Could this synthesis suggest a new compositional technique for algorithmic music?",
            ]
            suggestion = random.choice(suggestions)
        
        utility_score = min(10, app_count * 3 + (density * 5))
        
        return {
            'flag': 'Castalian' if flagged else 'Applied',
            'graph_density': round(density, 3),
            'applications_count': app_count,
            'suggestion': suggestion,
            'utility_score': round(utility_score, 2),
            'warning': flagged and "This session is beautiful but sealed. The Game must illuminate the world.",
        }
