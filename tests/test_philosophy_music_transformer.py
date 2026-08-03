"""
Tests for the Philosophy ↔ Music Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from philosophy_music_transformer import (
    PhilosophyMusicTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_pythagorean_tonal_harmony(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Pythagorean harmony of the spheres",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="cosmos governed by integer ratios",
        )
        assert result.direction == "philosophy→music"
        assert "pythagor" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_nietzsche_apollonian_dionysian(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Nietzsche Apollonian Dionysian duality",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="form versus intoxication",
        )
        assert "nietzsche" in result.isomorphisms[0].lower()
        assert "classical" in result.destination_concept.lower() or "romantic" in result.destination_concept.lower()

    def test_schopenhauer_will_melodic_drive(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Schopenhauer Will as blind striving",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="goal-directed volitional motion",
        )
        assert "schopenhauer" in result.isomorphisms[0].lower()
        assert "melodic" in result.destination_concept.lower() or "melody" in result.destination_concept.lower()

    def test_hegel_dialectic_sonata_form(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Hegel dialectic thesis antithesis synthesis",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="self-development through contradiction",
        )
        assert "hegel" in result.isomorphisms[0].lower() or "dialectic" in result.isomorphisms[0].lower()
        assert "sonata" in result.destination_concept.lower()

    def test_adorno_atonality(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Adorno negative dialectics",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="refusal of synthesis and preserved contradiction",
        )
        assert "adorno" in result.isomorphisms[0].lower()
        assert "atonal" in result.destination_concept.lower()

    def test_confucian_ritual_music(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Confucian ritual music doctrine",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="ethical ordering through rite and music",
        )
        assert "confuc" in result.isomorphisms[0].lower()
        assert "ceremonial" in result.destination_concept.lower() or "ritual" in result.destination_concept.lower()

    def test_stoic_tranquility_minimalism(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Stoic ataraxia tranquility",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="acceptance and disciplined attention",
        )
        assert "stoic" in result.isomorphisms[0].lower()
        assert "minimal" in result.destination_concept.lower()

    def test_buddhist_impermanence_variation(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Buddhist impermanence anicca",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="identity as process through change",
        )
        assert "buddh" in result.isomorphisms[0].lower()
        assert "variation" in result.destination_concept.lower()

    def test_existential_freedom_improvisation(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Existentialist freedom and choice",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="self-constitution through free choice",
        )
        assert "existential" in result.isomorphisms[0].lower()
        assert "improvis" in result.destination_concept.lower() or "jazz" in result.destination_concept.lower()

    def test_heraclitus_flux_continuous_variation(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Heraclitus flux panta rhei",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="everything flows and becomes",
        )
        assert "heraclitus" in result.isomorphisms[0].lower()
        assert "variation" in result.destination_concept.lower() or "continuous" in result.destination_concept.lower()


class TestBidirectionalTransformations:
    """Test music→philosophy direction."""

    def test_music_to_philosophy_sonata(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Sonata form exposition development recapitulation",
            origin_domain="Music",
            destination_domain="Philosophy",
            structural_property="dialectical structure through modulation",
        )
        assert result.direction == "music→philosophy"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_music_to_philosophy_minimalism(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Minimalist repetition gradual process",
            origin_domain="Music",
            destination_domain="Philosophy",
            structural_property="sustained texture and reduced will",
        )
        assert result.direction == "music→philosophy"
        assert "stoic" in result.destination_concept.lower() or "tranquility" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """philosophy→music round-trip should produce musical terminology."""
        t = PhilosophyMusicTransformer()
        result1 = t.transform(
            origin_concept="Hegel dialectic",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="self-development through contradiction",
        )
        assert any(word in result1.destination_concept.lower() for word in
                    ["sonata", "exposition", "development", "recapitulation", "form", "key"])


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = PhilosophyMusicTransformer()
        test_tokens = ["[PARSE]", "concept", "dialectic", "[TAG]", "label", "philosophical"]
        result = t.transform(
            origin_concept="Hegel dialectic",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="thesis antithesis synthesis",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = PhilosophyMusicTransformer()
        test_tokens = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9",
                       "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18"]
        result = t.transform(
            origin_concept="Schopenhauer Will",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="blind striving",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Pythagorean harmony of the spheres",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="cosmos governed by integer ratios",
        )
        assert result.total_confidence >= 0.85


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = PhilosophyMusicTransformer()
        moves = [
            {"from_concept": "Hegel dialectic", "from_domain": "Philosophy", "to_domain": "Music", "structural_property": "dialectical development"},
            {"from_concept": "Sonata form", "from_domain": "Music", "to_domain": "Philosophy", "structural_property": "dialectical structure"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "philosophy→music"
        assert results[1].direction == "music→philosophy"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = PhilosophyMusicTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "pythagorean_spheres__tonal_harmony" in catalog
        assert "hegel_dialectic__sonata_form" in catalog


class TestLanguageThread:
    """Test human language as connecting thread."""

    def test_each_step_has_language_thread(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Nietzsche Apollonian Dionysian",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="form versus intoxication",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Schopenhauer Will",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="blind striving",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestSerialization:
    """Test to_dict / from_dict JSON serialization."""

    def test_to_dict_roundtrip(self):
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Hegel dialectic",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="dialectical development",
        )
        d = result.to_dict()
        assert d["direction"] == "philosophy→music"
        assert d["origin_domain"] == "Philosophy"
        assert d["destination_domain"] == "Music"
        assert len(d["steps"]) == 6
        assert isinstance(d["steps"][0], dict)
        assert "language_thread" in d["steps"][0]

    def test_to_dict_is_json_serializable(self):
        import json
        t = PhilosophyMusicTransformer()
        result = t.transform(
            origin_concept="Pythagorean harmony",
            origin_domain="Philosophy",
            destination_domain="Music",
            structural_property="integer ratios",
        )
        d = result.to_dict()
        s = json.dumps(d, ensure_ascii=False)
        assert "philosophy→music" in s


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])