"""Tests for Contemplation Engine"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from src.contemplation import (
    ContemplationPhase,
    ContemplationSession,
    PhaseRecord,
    require_contemplation_before_move,
    apply_contemplation_bonus,
)


def test_phase_lifecycle():
    session = ContemplationSession(player_id="knecht")
    assert not session.is_active()

    session.enter_phase(ContemplationPhase.PREPARATION)
    assert session.is_active()
    assert session._current_phase == ContemplationPhase.PREPARATION

    time.sleep(0.1)
    record = session.exit_phase("I seek the unity beneath multiplicity.")
    assert isinstance(record, PhaseRecord)
    assert record.phase == ContemplationPhase.PREPARATION
    assert record.duration_seconds >= 0.1
    assert not session.is_active()
    print("✓ Phase lifecycle works")


def test_all_five_phases():
    session = ContemplationSession(player_id="tester")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(0.05)
        session.exit_phase(f"Reflection during {phase.name} phase.")
    assert session.is_complete()
    assert len(session.phases_completed) == 5
    print("✓ All five phases complete")


def test_depth_scoring():
    session = ContemplationSession(player_id="scorer")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(1.5)
        session.exit_phase(f"Notes for {phase.name}.")
    score = session.depth_score()
    assert score["scaled"] > 0
    assert 1.0 <= score["bonus_multiplier"] <= 2.0
    print("✓ Depth scoring works")


def test_rush_penalty():
    session = ContemplationSession(player_id="rusher")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(0.01)  # Too brief
        session.exit_phase(f"Hasty note for {phase.name}.")
    score = session.depth_score()
    # Should be heavily penalised or zero
    assert score["scaled"] < score["raw"] or score["scaled"] == 0.0
    print("✓ Rush penalty works")


def test_move_requirement():
    assert ContemplationSession.move_requires_contemplation("synthesis")
    assert ContemplationSession.move_requires_contemplation("realization")
    assert not ContemplationSession.move_requires_contemplation("simple_link")

    incomplete = ContemplationSession(player_id="incomplete")
    incomplete.enter_phase(ContemplationPhase.PREPARATION)
    time.sleep(0.01)
    incomplete.exit_phase("Only one phase.")
    req = require_contemplation_before_move("synthesis", incomplete)
    assert req["required"] is True
    assert req["passed"] is False
    print("✓ Move requirement checks work")


def test_bonus_claim():
    session = ContemplationSession(player_id="bonus")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(0.2)
        session.exit_phase(f"Deep reflection in {phase.name}.")
    bonus = session.claim_bonus()
    assert bonus is not None
    assert "bonus_points" in bonus
    assert "phrase" in bonus
    assert session._consumed is True
    # Second claim returns None
    assert session.claim_bonus() is None
    print("✓ Bonus claim works")


def test_apply_contemplation_bonus():
    session = ContemplationSession(player_id="applier")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(1.5)
        session.exit_phase(f"Reflection in {phase.name}.")
    result = apply_contemplation_bonus(base_score=50.0, session=session)
    assert result["bonus_applied"] is True
    assert result["final_score"] > 50.0
    print("✓ Apply bonus works")


def test_language_thread():
    session = ContemplationSession(player_id="lang")
    thread = session.language_thread()
    assert "PREPARATION" in thread
    assert "latin" in thread["PREPARATION"]
    single = session.language_thread(ContemplationPhase.CONCENTRATION)
    assert single["german"] == "Das Sich-Versenken in die Gestalt"
    print("✓ Language thread works")


def test_serialisation():
    session = ContemplationSession(player_id="serial")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(0.05)
        session.exit_phase(f"Note for {phase.name}.")
    data = session.to_dict()
    restored = ContemplationSession.from_dict(data)
    assert restored.player_id == session.player_id
    assert restored.is_complete() == session.is_complete()
    assert len(restored.phases_completed) == len(session.phases_completed)
    print("✓ Serialisation works")


def test_integration_with_game_engine():
    """Simulate engine calling contemplation guard before an advanced move."""
    session = ContemplationSession(player_id="integrator")
    for phase in ContemplationPhase:
        session.enter_phase(phase)
        time.sleep(0.1)
        session.exit_phase(f"Integrated {phase.name}.")
    req = require_contemplation_before_move("theme_development", session)
    assert req["passed"] is True
    assert "depth" in req
    print("✓ Integration with game engine works")


if __name__ == '__main__':
    test_phase_lifecycle()
    test_all_five_phases()
    test_depth_scoring()
    test_rush_penalty()
    test_move_requirement()
    test_bonus_claim()
    test_apply_contemplation_bonus()
    test_language_thread()
    test_serialisation()
    test_integration_with_game_engine()
    print("\nAll contemplation tests passed.")
