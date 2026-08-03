"""Tests for src/critic.py CriticEngine."""

import pytest
from src.critic import CriticEngine


@pytest.fixture
def engine():
    return CriticEngine()


def _make_move(
    move_type="contemplation",
    iso=0.85,
    thread="This is a sufficiently long language thread that exceeds fifty characters.",
    contemplation=True,
    antithesis=False,
):
    return {
        "type": move_type,
        "domain": "math",
        "isomorphism_confidence": iso,
        "language_thread": thread,
        "has_contemplation_bonus": contemplation,
        "antithesis_present": antithesis,
    }


def test_perfect_move_green(engine):
    move = _make_move(move_type="dialectic", antithesis=True)
    result = engine.analyze_move(move)
    assert result["score"] == 1.0
    assert result["issues"] == []
    assert result["suggestions"] == []
    assert result["traffic_light"] == "green"


def test_low_isomorphism_confidence_red(engine):
    move = _make_move(iso=0.5)
    result = engine.analyze_move(move)
    assert "isomorphism_confidence below 0.7" in result["issues"]
    assert result["score"] == 0.6
    assert result["traffic_light"] == "amber"


def test_short_language_thread_issue(engine):
    move = _make_move(thread="short")
    result = engine.analyze_move(move)
    assert "language_thread too short (<= 50 chars)" in result["issues"]
    assert result["score"] == 0.7
    assert result["traffic_light"] == "amber"


def test_missing_contemplation_bonus(engine):
    move = _make_move(contemplation=False)
    result = engine.analyze_move(move)
    assert "missing contemplation_bonus" in result["issues"]
    assert result["score"] == 0.8
    assert result["traffic_light"] == "amber"


def test_dialectic_missing_antithesis(engine):
    move = _make_move(move_type="dialectic", antithesis=False)
    result = engine.analyze_move(move)
    assert "dialectic move missing antithesis" in result["issues"]
    assert result["score"] == 0.7
    assert result["traffic_light"] == "amber"


def test_multiple_issues_score(engine):
    move = _make_move(
        move_type="dialectic",
        iso=0.5,
        thread="tiny",
        contemplation=False,
        antithesis=False,
    )
    result = engine.analyze_move(move)
    assert result["score"] == 0.0
    assert result["traffic_light"] == "red"
    assert len(result["issues"]) == 4
    assert len(result["suggestions"]) == 4


def test_non_dialectic_no_antithesis_required(engine):
    move = _make_move(move_type="contemplation", antithesis=False)
    result = engine.analyze_move(move)
    assert "dialectic move missing antithesis" not in result["issues"]
    assert result["score"] == 1.0


def test_score_clamped_minimum_zero(engine):
    move = _make_move(
        move_type="dialectic",
        iso=0.0,
        thread="",
        contemplation=False,
        antithesis=False,
    )
    result = engine.analyze_move(move)
    assert result["score"] == 0.0
    assert result["traffic_light"] == "red"
    assert result["score"] == max(0.0, min(1.0, result["score"]))


def test_traffic_light_amber(engine):
    move = _make_move(iso=0.6)
    result = engine.analyze_move(move)
    assert result["traffic_light"] == "amber"


def test_suggestions_populated(engine):
    move = _make_move(iso=0.6, thread="x", contemplation=False)
    result = engine.analyze_move(move)
    assert "Strengthen isomorphism mapping." in result["suggestions"]
    assert "Expand language thread." in result["suggestions"]
    assert "Add contemplative depth." in result["suggestions"]
