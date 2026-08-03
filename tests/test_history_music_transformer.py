"""
Tests for the History ↔ Music Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from history_music_transformer import (
    HistoryMusicTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_baroque_fugue(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Baroque era absolutism",
            origin_domain="History",
            destination_domain="Music",
            structural_property="layered hierarchy under sovereign order",
        )
        assert result.direction == "history→music"
        assert "baroque" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_renaissance_polyphonic_motet(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Renaissance humanism",
            origin_domain="History",
            destination_domain="Music",
            structural_property="plurality of independent voices",
        )
        assert "renaissance" in result.isomorphisms[0].lower()
        assert "motet" in result.destination_concept.lower() or "polyphon" in result.destination_concept.lower()

    def test_enlightenment_sonata_form(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Enlightenment rationalism",
            origin_domain="History",
            destination_domain="Music",
            structural_property="rational argument and balanced exposition",
        )
        assert "enlightenment" in result.isomorphisms[0].lower()
        assert "sonata" in result.destination_concept.lower()

    def test_romantic_program_music(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Romantic era individualism",
            origin_domain="History",
            destination_domain="Music",
            structural_property="narrative self-expression",
        )
        assert "romantic" in result.isomorphisms[0].lower()
        assert "program" in result.destination_concept.lower()

    def test_wwi_atonality(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="First World War crisis",
            origin_domain="History",
            destination_domain="Music",
            structural_property="collapse of old order and tonal center",
        )
        assert "wwi" in result.isomorphisms[0].lower() or "crisis" in result.isomorphisms[0].lower()
        assert "atonal" in result.destination_concept.lower() or "viennese" in result.destination_concept.lower()

    def test_civil_rights_spirituals(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Civil Rights movement",
            origin_domain="History",
            destination_domain="Music",
            structural_property="communal solidarity and call-and-response",
        )
        assert "civil" in result.isomorphisms[0].lower() or "rights" in result.isomorphisms[0].lower()
        assert "spiritual" in result.destination_concept.lower() or "gospel" in result.destination_concept.lower()

    def test_french_revolution_beethoven(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="French Revolution",
            origin_domain="History",
            destination_domain="Music",
            structural_property="heroic individualism and overthrow of order",
        )
        assert "french" in result.isomorphisms[0].lower() or "revolution" in result.isomorphisms[0].lower()
        assert "beethoven" in result.destination_concept.lower() or "heroic" in result.destination_concept.lower()

    def test_industrial_revolution_ostinato(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Industrial Revolution",
            origin_domain="History",
            destination_domain="Music",
            structural_property="mechanized repetitive labor",
        )
        assert "industrial" in result.isomorphisms[0].lower()
        assert "ostinato" in result.destination_concept.lower() or "mechanical" in result.destination_concept.lower()

    def test_cold_war_serialism(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Cold War",
            origin_domain="History",
            destination_domain="Music",
            structural_property="total systemic control and deterrence",
        )
        assert "cold" in result.isomorphisms[0].lower()
        assert "serial" in result.destination_concept.lower()

    def test_greek_modes_gregorian(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Ancient Greek modal theory",
            origin_domain="History",
            destination_domain="Music",
            structural_property="transmission of modal system through antiquity",
        )
        assert "greek" in result.isomorphisms[0].lower()
        assert "gregorian" in result.destination_concept.lower() or "chant" in result.destination_concept.lower()


class TestBidirectionalTransformations:
    """Test music→history direction."""

    def test_music_to_history_fugue(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Fugue contrapuntal form",
            origin_domain="Music",
            destination_domain="History",
            structural_property="layered voices under single subject",
        )
        assert result.direction == "music→history"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_music_to_history_sonata(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Sonata form exposition development recapitulation",
            origin_domain="Music",
            destination_domain="History",
            structural_property="rational argument through thematic transformation",
        )
        assert result.direction == "music→history"
        assert "enlightenment" in result.destination_concept.lower() or "sonata" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """history→music round-trip should produce musical terminology."""
        t = HistoryMusicTransformer()
        result1 = t.transform(
            origin_concept="French Revolution",
            origin_domain="History",
            destination_domain="Music",
            structural_property="heroic individualism",
        )
        assert any(word in result1.destination_concept.lower() for word in
                    ["beethoven", "heroic", "symphony", "scale", "triumph", "struggle"])


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = HistoryMusicTransformer()
        test_tokens = ["[PARSE]", "era", "revolution", "[TAG]", "label", "historical"]
        result = t.transform(
            origin_concept="Baroque era",
            origin_domain="History",
            destination_domain="Music",
            structural_property="layered hierarchy",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = HistoryMusicTransformer()
        test_tokens = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9",
                       "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18"]
        result = t.transform(
            origin_concept="Enlightenment",
            origin_domain="History",
            destination_domain="Music",
            structural_property="rational argument",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="History",
            destination_domain="Music",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="French Revolution",
            origin_domain="History",
            destination_domain="Music",
            structural_property="heroic individualism and overthrow of order",
        )
        assert result.total_confidence >= 0.85


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = HistoryMusicTransformer()
        moves = [
            {"from_concept": "Baroque era", "from_domain": "History", "to_domain": "Music", "structural_property": "layered hierarchy"},
            {"from_concept": "Fugue", "from_domain": "Music", "to_domain": "History", "structural_property": "contrapuntal layering"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "history→music"
        assert results[1].direction == "music→history"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = HistoryMusicTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "baroque_absolutism__fugue" in catalog
        assert "wwi_crisis__atonality" in catalog


class TestLanguageThread:
    """Test human language as connecting thread."""

    def test_each_step_has_language_thread(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Renaissance",
            origin_domain="History",
            destination_domain="Music",
            structural_property="plurality of voices",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Romantic era",
            origin_domain="History",
            destination_domain="Music",
            structural_property="narrative self-expression",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestSerialization:
    """Test to_dict / from_dict JSON serialization."""

    def test_to_dict_roundtrip(self):
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Enlightenment",
            origin_domain="History",
            destination_domain="Music",
            structural_property="rational argument",
        )
        d = result.to_dict()
        assert d["direction"] == "history→music"
        assert d["origin_domain"] == "History"
        assert d["destination_domain"] == "Music"
        assert len(d["steps"]) == 6
        assert isinstance(d["steps"][0], dict)
        assert "language_thread" in d["steps"][0]

    def test_to_dict_is_json_serializable(self):
        import json
        t = HistoryMusicTransformer()
        result = t.transform(
            origin_concept="Baroque era",
            origin_domain="History",
            destination_domain="Music",
            structural_property="layered hierarchy",
        )
        d = result.to_dict()
        s = json.dumps(d, ensure_ascii=False)
        assert "history→music" in s


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])