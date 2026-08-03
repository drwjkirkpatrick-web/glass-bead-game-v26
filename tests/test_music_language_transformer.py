"""
Tests for the Music ↔ Language Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from music_language_transformer import (
    MusicLanguageTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_phonology_pitch_intervals(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Phoneme and distinctive features",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="minimal contrastive units with relational identity",
        )
        assert result.direction == "language→music"
        assert "phonolog" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_syntax_tree_voice_leading(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Syntax tree phrase structure",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="hierarchical structure with heads and complements",
        )
        assert "syntax" in result.isomorphisms[0].lower()

    def test_prosody_musical_phrasing(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Prosody and intonation",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="grouping of events into phrases via prominence contour",
        )
        assert "prosod" in result.isomorphisms[0].lower()

    def test_semantics_tonal_function(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Semantics and semantic roles",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="meaning determined by relational role in a system",
        )
        assert "semant" in result.isomorphisms[0].lower()

    def test_morphology_motivic_transformation(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Morphology and morphemes",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="structural operations applied to a base form",
        )
        assert "morpholog" in result.isomorphisms[0].lower()

    def test_pragmatics_performance_practice(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Pragmatics and speech acts",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="contextual interpretation determines actual meaning",
        )
        assert "pragmat" in result.isomorphisms[0].lower()

    def test_poetic_meter_rhythmic_meter(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Poetic meter and stress pattern",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="recurring accentual pattern grouping events",
        )
        assert "meter" in result.isomorphisms[0].lower() or "poetic" in result.isomorphisms[0].lower()

    def test_semiotics_musical_semiotics(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Semiotics and signs",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="signifier signified conventional code",
        )
        assert "semiot" in result.isomorphisms[0].lower()

    def test_rhetoric_figures_musical_figures(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Rhetorical figures and ornaments",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="structural ornaments of argument transposed into music",
        )
        assert "rhetor" in result.isomorphisms[0].lower()

    def test_distinctive_features_interval_vectors(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Distinctive features binary phonology",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="compact relational signature of internal contrasts",
        )
        assert "distinctive" in result.isomorphisms[0].lower() or "interval" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test music→language direction."""

    def test_music_to_language_phonology(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Pitch intervals as contrastive units",
            origin_domain="Music",
            destination_domain="Language",
            structural_property="minimal contrastive units with relational identity",
        )
        assert result.direction == "music→language"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_music_to_language_prosody(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Musical phrasing and cadence",
            origin_domain="Music",
            destination_domain="Language",
            structural_property="grouping events into phrases via prominence contour",
        )
        assert result.direction == "music→language"
        assert "prosod" in result.isomorphisms[0].lower()

    def test_language_to_music_direction_value(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Morphology",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="structural operations applied to a base form",
        )
        assert result.direction == "language→music"

    def test_round_trip_fidelity(self):
        """language→music round-trip should preserve concept identity."""
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Phonology phonemes distinctive features",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="minimal contrastive units with relational identity",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["phoneme", "phonology", "interval", "feature", "contrast", "pitch"])


class TestPipelineStructure:
    """Test the 6-stage pipeline."""

    def test_six_stages(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Syntax tree",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="hierarchical phrase structure",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Prosody",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="intonation and phrasing",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Semantics",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="relational meaning",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Something obscure and totally unrelated",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="vagueness without structure",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Prosody and intonation",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="grouping of events into phrases via prominence contour",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        """Every ISOMORPHISM entry has confidence in [0.85, 0.99]."""
        t = MusicLanguageTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test JSON serialization round-trip."""

    def test_to_dict_round_trip(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="Poetic meter",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="recurring accentual pattern",
        )
        d = result.to_dict()
        assert d["direction"] == result.direction
        assert d["origin_concept"] == result.origin_concept
        assert len(d["steps"]) == 6
        assert isinstance(d["steps"][0]["stage"], str)
        assert isinstance(d["total_confidence"], float)
        # Step data should be plain dict
        assert d["steps"][0]["language_thread"] == result.steps[0].language_thread


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = MusicLanguageTransformer()
        moves = [
            {"from_concept": "Phonology", "from_domain": "Linguistics",
             "to_domain": "Music", "structural_property": "minimal contrastive units"},
            {"from_concept": "Musical phrasing", "from_domain": "Music",
             "to_domain": "Language", "structural_property": "grouping via prominence contour"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "language→music"
        assert results[1].direction == "music→language"


class TestFallbackIsomorphism:
    """Test fallback behavior for unrecognized concepts."""

    def test_fallback_returns_generic(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="zzzqqqxx",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="zzzqqqxx",
        )
        assert result.isomorphisms[0] == "generic_homomorphism__musical_linguistic_form"
        assert result.total_confidence >= 0.3

    def test_fallback_music_to_language(self):
        t = MusicLanguageTransformer()
        result = t.transform(
            origin_concept="zzzqqqxx",
            origin_domain="Music",
            destination_domain="Language",
            structural_property="zzzqqqxx",
        )
        assert result.direction == "music→language"
        assert result.isomorphisms[0] == "generic_homomorphism__musical_linguistic_form"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = MusicLanguageTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "phonology__pitch_intervals" in catalog
        assert "prosody__musical_phrasing" in catalog

    def test_catalog_excludes_rule(self):
        t = MusicLanguageTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data
            assert "music" in data
            assert "language" in data
            assert "confidence" in data


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = MusicLanguageTransformer()
        test_tokens = ["[PARSE]", "decompose", "phoneme", "[TAG]", "label", "contrast"]
        result = t.transform(
            origin_concept="Phoneme",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="minimal contrastive units",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = MusicLanguageTransformer()
        test_tokens = ["t1", "t2", "t3", "t4", "t5", "t6",
                        "t7", "t8", "t9", "t10", "t11", "t12",
                        "t13", "t14", "t15", "t16", "t17", "t18"]
        result = t.transform(
            origin_concept="Morphology",
            origin_domain="Linguistics",
            destination_domain="Music",
            structural_property="structural operations on base form",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


if __name__ == "__main__":
    pytest.main([__file__, "-v"])