"""
Tests for the History ↔ Philosophy Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from history_philosophy_transformer import (
    HistoryPhilosophyTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_hegelian_dialectic(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Dialectical historical process",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="thesis antithesis synthesis sublation",
        )
        assert result.direction == "history→philosophy"
        assert "hegelian" in result.isomorphisms[0].lower() or "dialectic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_vico_corsi_ricorsi(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Vico's corsi e ricorsi",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="cyclical return of civilizations through divine heroic human ages",
        )
        assert "vico" in result.isomorphisms[0].lower() or "cyclical" in result.isomorphisms[0].lower()

    def test_spengler_morphology(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Spengler's morphology of cultures",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="organic lifecycle of civilizations birth growth decline",
        )
        assert "spengler" in result.isomorphisms[0].lower() or "morphology" in result.isomorphisms[0].lower()

    def test_renaissance_anamnesis(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Renaissance rebirth of classical antiquity",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="rediscovery and revival of forgotten knowledge",
        )
        assert "renaissance" in result.isomorphisms[0].lower() or "anamnesis" in result.isomorphisms[0].lower()

    def test_enlightenment_teleology(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Enlightenment progress",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="directional advancement toward reason and perfectibility",
        )
        assert "enlightenment" in result.isomorphisms[0].lower() or "teleolog" in result.isomorphisms[0].lower()

    def test_existentialism_crisis(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Post-WWI historical crisis",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="collapse of meaning and shattered European order",
        )
        assert "existentialism" in result.isomorphisms[0].lower() or "crisis" in result.isomorphisms[0].lower()

    def test_hermeneutics_interpretation(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Hermeneutic interpretation of the past",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="fusion of horizons between interpreter and text",
        )
        assert "hermeneutic" in result.isomorphisms[0].lower()

    def test_foucault_genealogy(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Foucault's genealogy of institutions and power",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="tracing descent of practices and epistemic strata",
        )
        assert "foucault" in result.isomorphisms[0].lower() or "genealogy" in result.isomorphisms[0].lower()

    def test_marx_materialism(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Marx's historical materialism",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="modes of production and class struggle drive history",
        )
        assert "marx" in result.isomorphisms[0].lower() or "materialism" in result.isomorphisms[0].lower()

    def test_collingwood_reenactment(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Collingwood's re-enactment of past thought",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="historian re-thinks the thought of historical agents",
        )
        assert "collingwood" in result.isomorphisms[0].lower() or "reenactment" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test philosophy→history direction."""

    def test_philosophy_to_history_hegel(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Hegelian dialectic of Spirit",
            origin_domain="Philosophy",
            destination_domain="History",
            structural_property="thesis antithesis synthesis aufhebung",
        )
        assert result.direction == "philosophy→history"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_philosophy_to_history_hermeneutics(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Hermeneutic circle and fusion of horizons",
            origin_domain="Philosophy",
            destination_domain="History",
            structural_property="interpretation understanding text context horizon",
        )
        assert result.direction == "philosophy→history"
        assert "hermeneutic" in result.isomorphisms[0].lower()

    def test_round_trip_fidelity(self):
        """history→philosophy should preserve concept identity."""
        t = HistoryPhilosophyTransformer()
        result1 = t.transform(
            origin_concept="Dialectical historical process",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="thesis antithesis synthesis",
        )
        # The destination concept should contain philosophical terminology
        assert any(word in result1.destination_concept.lower() for word in
                    ["dialectic", "hegel", "thesis", "spirit", "sublation", "aufhebung"])


class TestPipelineStructure:
    """Test the 6-stage pipeline."""

    def test_six_stages_present(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Dialectical historical process",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="thesis antithesis synthesis",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Renaissance rebirth",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="rediscovery of antiquity",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Enlightenment progress",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="directional advancement",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Hegelian dialectic",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="thesis antithesis synthesis sublation",
        )
        assert result.total_confidence >= 0.85


class TestSerialisation:
    """Test JSON serialization round-trip."""

    def test_serialisation_round_trip(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="Hermeneutic interpretation",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="fusion of horizons",
        )
        d = result.to_dict()
        assert d["direction"] == result.direction
        assert d["origin_concept"] == result.origin_concept
        assert len(d["steps"]) == 6
        assert all("stage" in s and "language_thread" in s for s in d["steps"])
        # Re-instantiate from dict fields
        steps_back = [TransformationStep(**s) for s in d["steps"]]
        assert steps_back[0].stage == "PARSE"
        assert steps_back[-1].stage == "VERIFY"


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = HistoryPhilosophyTransformer()
        moves = [
            {"from_concept": "Dialectical historical process", "from_domain": "History",
             "to_domain": "Philosophy", "structural_property": "thesis antithesis synthesis"},
            {"from_concept": "Hegelian dialectic of Spirit", "from_domain": "Philosophy",
             "to_domain": "History", "structural_property": "aufhebung sublation"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "history→philosophy"
        assert results[1].direction == "philosophy→history"


class TestFallbackIsomorphism:
    """Test fallback when no isomorphism matches."""

    def test_fallback_isomorphism(self):
        t = HistoryPhilosophyTransformer()
        result = t.transform(
            origin_concept="xyzzy obscure unrelated thing",
            origin_domain="History",
            destination_domain="Philosophy",
            structural_property="zzz",
        )
        assert "generic_correspondence" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = HistoryPhilosophyTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "hegelian_dialectic__dialectical_history" in catalog
        assert "hermeneutics__historical_interpretation" in catalog
        # rule should be excluded from catalog
        assert "rule" not in catalog["hegelian_dialectic__dialectical_history"]


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])