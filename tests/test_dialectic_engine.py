"""Tests for the Thesis-Antithesis-Synthesis dialectic engine."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

from src.dialectic_engine import (
    Thesis, Antithesis, Synthesis,
    DialecticGame, DialecticScorer,
)


def test_thesis_antithesis_synthesis_dataclasses():
    t = Thesis(title="Law", domain="philosophia", core_idea="Order binds chaos.", keywords=["order", "structure", "rules"])
    a = Antithesis(title="Freedom", domain="historia", core_idea="The will unbound.", opposition_axes=["individual", "unpredictability"])
    s = Synthesis(title="Ordered Liberty", emergent_concept="Autonomy within a lattice of mutual respect.")

    assert t.title == "Law"
    assert a.domain == "historia"
    assert "emergent_concept" in s.to_dict()
    print("✓ Dataclasses instantiate and serialize")


def test_equality_scorer():
    t = Thesis("Law", "philosophia", "...", keywords=["a", "b", "c"])
    a = Antithesis("Freedom", "historia", "...", opposition_axes=["x", "y", "z"])

    # perfectly balanced
    s_balanced = Synthesis("S", "...", preserved_from_thesis=["a", "b"], preserved_from_antithesis=["x", "y"])
    assert DialecticScorer.equality(t, a, s_balanced) == 1.0

    # imbalanced
    s_imbalanced = Synthesis("S", "...", preserved_from_thesis=["a", "b", "c"], preserved_from_antithesis=["x"])
    eq = DialecticScorer.equality(t, a, s_imbalanced)
    assert eq < 1.0
    assert eq > 0.0
    print("✓ Equality scoring works")


def test_tension_scorer():
    t = Thesis("Law", "philosophia", "...", keywords=["order", "structure"])
    a = Antithesis("Freedom", "historia", "...", opposition_axes=["individual", "unpredictability"])

    s = Synthesis(
        "S", "...",
        preserved_from_thesis=["order", "structure"],
        preserved_from_antithesis=["individual"],
        language_thread="Law → Freedom → Ordered Liberty",
    )
    te = DialecticScorer.tension(t, a, s)
    assert 0.0 <= te <= 1.0
    assert te > 0.5  # high coverage + bridge bonus
    print("✓ Tension scoring works")


def test_purity_scorer():
    t = Thesis("Law", "philosophia", "Order binds chaos.")
    a = Antithesis("Freedom", "historia", "The will unbound.")

    # novel emergent concept — should score well
    s_pure = Synthesis("Ordered Liberty", "Autonomy within a lattice of mutual respect.", language_thread="Law → Freedom → Ordered Liberty")
    pu_pure = DialecticScorer.purity(t, a, s_pure)
    assert pu_pure > 0.5

    # compromise title penalized
    s_comp = Synthesis("Law and Freedom", "A mix of law and freedom.")
    pu_comp = DialecticScorer.purity(t, a, s_comp)
    assert pu_comp < pu_pure
    print("✓ Purity scoring works")


def test_dialectic_game_builder():
    t = Thesis("Law", "philosophia", "Order binds chaos.", keywords=["order", "structure", "rules"])
    a = Antithesis("Freedom", "historia", "The will unbound.", opposition_axes=["individual", "spontaneity"])

    game = DialecticGame(t, a)
    try:
        game.score()
        assert False, "should raise before synthesis is built"
    except ValueError:
        pass

    synth = game.build_synthesis(
        title="Ordered Liberty",
        emergent_concept="Autonomy within a lattice of mutual respect.",
        language_thread="Law → Freedom → Ordered Liberty",
    )
    assert synth.title == "Ordered Liberty"

    scores = game.score()
    assert "equality" in scores
    assert "tension" in scores
    assert "purity" in scores
    assert "overall" in scores
    assert 0.0 <= scores["overall"] <= 1.0
    print("✓ DialecticGame builder works")


def test_from_moves_factory():
    m1 = {"from_domain": "musica", "via": "Recursive fugue structure.", "keywords": ["recursion", "voice"]}
    m2 = {"from_domain": "mathematica", "via": "Self-referential proof.", "opposition_axes": ["rigor", "abstraction"]}

    game = DialecticGame.from_moves(m1, m2, thesis_title="Fugue", antithesis_title="Proof")
    assert game.thesis.title == "Fugue"
    assert game.antithesis.title == "Proof"
    assert game.thesis.domain == "musica"

    synth = game.build_synthesis(title="Recursive Harmony", emergent_concept="Beauty born of logical self-reference.")
    scores = game.score()
    assert scores["overall"] >= 0.0
    print("✓ from_moves factory works")


def test_full_serialization():
    t = Thesis("Law", "philosophia", "Order binds chaos.", keywords=["order"])
    a = Antithesis("Freedom", "historia", "The will unbound.", opposition_axes=["individual"])
    game = DialecticGame(t, a)
    game.build_synthesis("Ordered Liberty", "Autonomy within mutual respect.", language_thread="Law → Freedom → Ordered Liberty")
    game.score()

    d = game.to_dict()
    assert d["thesis"]["title"] == "Law"
    assert d["antithesis"]["title"] == "Freedom"
    assert d["synthesis"]["title"] == "Ordered Liberty"
    assert "scores" in d["synthesis"]
    print("✓ Full serialization works")


if __name__ == '__main__':
    test_thesis_antithesis_synthesis_dataclasses()
    test_equality_scorer()
    test_tension_scorer()
    test_purity_scorer()
    test_dialectic_game_builder()
    test_from_moves_factory()
    test_full_serialization()
    print("\nAll dialectic tests passed.")
