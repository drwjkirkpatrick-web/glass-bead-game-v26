"""Tests for Sonification Engine"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from src.sonification import SonificationEngine


def test_domain_to_pitch_mapping():
    assert SonificationEngine.DOMAIN_TO_PITCH['musica'] == 60
    assert SonificationEngine.DOMAIN_TO_PITCH['mathematica'] == 64
    assert SonificationEngine.DOMAIN_TO_PITCH['historia'] == 67
    assert SonificationEngine.DOMAIN_TO_PITCH['philosophia'] == 79


def test_sonify_move_returns_notes():
    engine = SonificationEngine()
    notes = engine.sonify_move('musica', 'mathematica', confidence=1.0)
    assert isinstance(notes, list)
    assert len(notes) >= 3
    for note in notes:
        assert 'pitch' in note
        assert 'velocity' in note
        assert 'duration' in note


def test_sonify_move_pitches_match_domains():
    engine = SonificationEngine()
    notes = engine.sonify_move('musica', 'mathematica', confidence=0.9)
    assert notes[0]['pitch'] == 60
    assert notes[1]['pitch'] == 64
    assert notes[2]['pitch'] == 62  # average


def test_sonify_move_confidence_affects_velocity():
    engine = SonificationEngine()
    low = engine.sonify_move('musica', 'mathematica', confidence=0.2)
    high = engine.sonify_move('musica', 'mathematica', confidence=1.0)
    assert high[0]['velocity'] > low[0]['velocity']


def test_sonify_move_high_confidence_adds_resolution():
    engine = SonificationEngine()
    notes = engine.sonify_move('musica', 'mathematica', confidence=0.85)
    assert len(notes) == 4
    assert notes[-1]['pitch'] == 76  # to_pitch + 12


def test_sonify_move_low_confidence_no_resolution():
    engine = SonificationEngine()
    notes = engine.sonify_move('musica', 'mathematica', confidence=0.5)
    assert len(notes) == 3


def test_sonify_state_empty():
    engine = SonificationEngine()
    result = engine.sonify_state({'nodes': []})
    assert result['drone_pitch'] == 60
    assert result['bpm'] == 60
    assert result['active_domains'] == []


def test_sonify_state_with_nodes():
    engine = SonificationEngine()
    game_state = {
        'nodes': [
            {'id': 'n1', 'domain': 'musica'},
            {'id': 'n2', 'domain': 'mathematica'},
            {'id': 'n3', 'domain': 'historia'},
        ]
    }
    result = engine.sonify_state(game_state)
    assert set(result['active_domains']) == {'musica', 'mathematica', 'historia'}
    assert result['drone_pitch'] == (60 + 64 + 67) // 3
    assert result['bpm'] == 60 + 3 * 3


def test_get_bpm_for_move():
    engine = SonificationEngine()
    bpm = engine.get_bpm_for_move('musica', 'mathematica')
    interval = abs(64 - 60)
    assert bpm == 60 + interval * 2


def test_sonify_move_unknown_domain_defaults():
    engine = SonificationEngine()
    notes = engine.sonify_move('unknown_domain', 'also_unknown')
    assert notes[0]['pitch'] == 60
    assert notes[1]['pitch'] == 60
