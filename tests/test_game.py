"""Tests for Glass Bead Game v26"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from src.game_engine import KnowledgeGraph, MoveValidator, ScoringEngine, RankManager, KnechtProtocol


def test_knowledge_graph():
    g = KnowledgeGraph()
    n1 = g.add_node({'domain': 'musica', 'label': 'Fugue', 'x': 0, 'y': 0, 'z': 0})
    n2 = g.add_node({'domain': 'mathematica', 'label': 'Recursion', 'x': 1, 'y': 1, 'z': 1})
    g.add_edge({'source': n1, 'target': n2, 'strength': 0.8})
    
    assert len(g.nodes) == 2
    assert len(g.edges) == 1
    assert g.density() > 0
    print("✓ KnowledgeGraph works")


def test_move_validator():
    v = MoveValidator()
    valid_move = {
        'from_domain': 'musica',
        'to_domain': 'mathematica',
        'via': 'Self-similar structure with recursive generation rules',
        'resonance': 'Both contain within themselves the rules for their own transformation.',
    }
    result = v.validate(valid_move)
    assert result['valid'] == True
    assert result['domain_crossings'] > 0
    print("✓ MoveValidator works")


def test_scoring():
    s = ScoringEngine()
    move = {
        'from_domain': 'musica',
        'to_domain': 'mathematica',
        'via': 'recursive self-reference',
        'resonance': 'A mirror reflecting its own reflection.',
    }
    validation = {'elegance_score': 8, 'fertility_estimate': 6, 'domain_crossings': 1}
    score = s.score(move, validation)
    assert 'total' in score
    assert score['total'] > 0
    print("✓ ScoringEngine works")


def test_knecht_protocol():
    k = KnechtProtocol()
    g = KnowledgeGraph()
    result = k.review_session(g, [])
    assert result['flag'] == 'Castalian'
    assert len(result['suggestion']) > 0
    print("✓ KnechtProtocol works")


if __name__ == '__main__':
    test_knowledge_graph()
    test_move_validator()
    test_scoring()
    test_knecht_protocol()
    print("\nAll tests passed.")
