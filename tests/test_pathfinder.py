"""Tests for Graph Pathfinder"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from src.pathfinder import GraphPathfinder


def test_add_node_and_edge():
    pf = GraphPathfinder()
    pf.add_node({'id': 'a', 'domain': 'musica'})
    pf.add_node({'id': 'b', 'domain': 'mathematica'})
    pf.add_edge({'id': 'e1', 'source': 'a', 'target': 'b', 'strength': 0.8})
    assert len(pf.nodes) == 2
    assert len(pf.edges) == 1


def test_bfs_same_node():
    pf = GraphPathfinder()
    pf.add_node({'id': 'a', 'domain': 'musica'})
    result = pf.bfs_shortest_path('a', 'a')
    assert result is not None
    assert result['path_nodes'] == ['a']
    assert result['path_edges'] == []


def test_bfs_direct_neighbor():
    pf = GraphPathfinder()
    pf.add_node({'id': 'a', 'domain': 'musica'})
    pf.add_node({'id': 'b', 'domain': 'mathematica'})
    pf.add_edge({'id': 'e1', 'source': 'a', 'target': 'b', 'strength': 0.8})
    result = pf.bfs_shortest_path('a', 'b')
    assert result is not None
    assert result['path_nodes'] == ['a', 'b']
    assert result['path_edges'] == ['e1']
    assert result['total_confidence'] == 0.8


def test_bfs_missing_nodes():
    pf = GraphPathfinder()
    result = pf.bfs_shortest_path('x', 'y')
    assert result is None


def test_astar_same_node():
    pf = GraphPathfinder()
    pf.add_node({'id': 'a', 'domain': 'musica'})
    result = pf.astar_shortest_path('a', 'a')
    assert result is not None
    assert result['path_nodes'] == ['a']


def test_astar_vs_bfs_consistency():
    pf = GraphPathfinder()
    pf.add_node({'id': 'a', 'domain': 'musica'})
    pf.add_node({'id': 'b', 'domain': 'mathematica'})
    pf.add_node({'id': 'c', 'domain': 'historia'})
    pf.add_edge({'id': 'e1', 'source': 'a', 'target': 'b', 'strength': 0.5})
    pf.add_edge({'id': 'e2', 'source': 'b', 'target': 'c', 'strength': 0.5})
    bfs = pf.bfs_shortest_path('a', 'c')
    astar = pf.astar_shortest_path('a', 'c')
    assert bfs['path_nodes'] == astar['path_nodes']
    assert bfs['path_edges'] == astar['path_edges']


def test_narrative_building():
    pf = GraphPathfinder()
    pf.add_node({'id': 'a', 'domain': 'musica'})
    pf.add_node({'id': 'b', 'domain': 'mathematica'})
    pf.add_edge({'id': 'e1', 'source': 'a', 'target': 'b', 'strength': 0.8, 'label': 'recursion'})
    result = pf.bfs_shortest_path('a', 'b')
    assert 'From musica' in result['narrative']
    assert 'to mathematica' in result['narrative']


def test_seed_graph():
    pf = GraphPathfinder.from_seed()
    assert len(pf.nodes) == 8
    assert len(pf.edges) == 8  # cyclic chain of 8 nodes


def test_bfs_seed_graph_wraps():
    pf = GraphPathfinder.from_seed()
    # node_7 is medicina, node_0 is musica; edge wraps 7->0
    result = pf.bfs_shortest_path('node_7', 'node_0')
    assert result is not None
    assert result['path_nodes'] == ['node_7', 'node_0']


def test_astar_seed_graph_longer_path():
    pf = GraphPathfinder.from_seed()
    result = pf.astar_shortest_path('node_0', 'node_3')
    assert result is not None
    assert result['path_nodes'] == ['node_0', 'node_1', 'node_2', 'node_3']
    assert len(result['path_edges']) == 3
    assert result['total_confidence'] == 1.5  # 3 * 0.5
