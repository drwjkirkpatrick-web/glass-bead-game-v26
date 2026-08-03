"""
Tests for the Nature ↔ Music Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nature_music_transformer import (
    NatureMusicTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_birdsong_melodic_ornamentation(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Birdsong",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="learned vocal motifs with intervallic leaps",
        )
        assert result.direction == "nature→music"
        assert "bird" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_cricket_stridulation_ostinato(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Cricket stridulation",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="species-specific periodic pulse rate",
        )
        assert "cricket" in result.isomorphisms[0].lower()
        assert "ostinato" in result.destination_concept.lower()

    def test_whale_song_long_form_phrasing(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Humpback whale song",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="hierarchical phrases assembled into themes",
        )
        assert "whale" in result.isomorphisms[0].lower()
        assert "phrase" in result.destination_concept.lower() or "form" in result.destination_concept.lower()

    def test_wind_aleatoric_music(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Wind through trees",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="stochastic modulation under turbulent flow",
        )
        assert "wind" in result.isomorphisms[0].lower()
        assert "aleatoric" in result.destination_concept.lower()

    def test_water_flow_legato(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Water flow laminar streamlines",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="smooth continuous motion around obstacles",
        )
        assert "water" in result.isomorphisms[0].lower() or "flow" in result.isomorphisms[0].lower()

    def test_thunder_percussion_dynamics(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Thunder",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="impulsive broadband sound with exponential decay",
        )
        assert "thunder" in result.isomorphisms[0].lower()
        assert "percussion" in result.destination_concept.lower() or "dynamics" in result.destination_concept.lower()

    def test_seasonal_cycle_sonata_form(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Seasonal cycle",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="annual oscillation renewal and senescence",
        )
        assert "season" in result.isomorphisms[0].lower()
        assert "sonata" in result.destination_concept.lower() or "form" in result.destination_concept.lower()

    def test_cardiac_rhythm_pulse_beat(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Cardiac rhythm",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="autorhythmic pulse with accent and entrainment",
        )
        assert "cardiac" in result.isomorphisms[0].lower() or "pulse" in result.isomorphisms[0].lower()
        assert "pulse" in result.destination_concept.lower() or "beat" in result.destination_concept.lower()

    def test_fibonacci_petals_golden_proportion(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Fibonacci petals phyllotaxis",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="golden angle spiral packing approaching phi",
        )
        assert "fibonacci" in result.isomorphisms[0].lower() or "golden" in result.isomorphisms[0].lower()

    def test_tectonic_plates_harmonic_progression(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Tectonic plate motion",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="stress accumulation and stick-slip release",
        )
        assert "tectonic" in result.isomorphisms[0].lower()
        assert "harmonic" in result.destination_concept.lower() or "progression" in result.destination_concept.lower()


class TestBidirectionalTransformations:
    """Test music→nature direction."""

    def test_music_to_nature_ostinato(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Ostinato",
            origin_domain="Music",
            destination_domain="Nature",
            structural_property="persistent repeated rhythmic pattern",
        )
        assert result.direction == "music→nature"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_music_to_nature_pulse(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Pulse beat",
            origin_domain="Music",
            destination_domain="Nature",
            structural_property="regular metrical grid with accented downbeats",
        )
        assert result.direction == "music→nature"
        assert "cardiac" in result.isomorphisms[0].lower() or "pulse" in result.isomorphisms[0].lower()


class TestPipelineStructure:
    """Test the 6-stage pipeline."""

    def test_six_stages_present(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Birdsong",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="learned vocal motifs",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Whale song",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="hierarchical phrases",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Thunder",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="impulsive broadband sound",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Cardiac rhythm",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="autorhythmic pulse with entrainment",
        )
        assert result.total_confidence >= 0.85


class TestSerialisation:
    """Test to_dict round-trip."""

    def test_serialisation_round_trip(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="Birdsong",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="learned vocal motifs",
        )
        d = result.to_dict()
        assert d["direction"] == result.direction
        assert d["origin_concept"] == result.origin_concept
        assert d["destination_concept"] == result.destination_concept
        assert len(d["steps"]) == 6
        assert all("stage" in s and "language_thread" in s for s in d["steps"])
        # Round-trip key fields
        assert d["isomorphisms"] == result.isomorphisms
        assert d["total_confidence"] == result.total_confidence


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = NatureMusicTransformer()
        moves = [
            {"from_concept": "Birdsong", "from_domain": "Nature", "to_domain": "Music", "structural_property": "learned motifs"},
            {"from_concept": "Ostinato", "from_domain": "Music", "to_domain": "Nature", "structural_property": "repeated pattern"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "nature→music"
        assert results[1].direction == "music→nature"


class TestFallbackIsomorphism:
    """Test fallback when no isomorphism matches."""

    def test_fallback_isomorphism(self):
        t = NatureMusicTransformer()
        result = t.transform(
            origin_concept="zzzzz unrecognized thingamajig xyzzy",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="zzzzz meaningless xyzzy",
        )
        assert result.total_confidence >= 0.3
        assert len(result.steps) == 6
        assert result.isomorphisms  # has a fallback name


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = NatureMusicTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "birdsong__melodic_ornamentation" in catalog
        assert "tectonic_plates__harmonic_progression" in catalog

    def test_catalog_excludes_rule(self):
        t = NatureMusicTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, entry in catalog.items():
            assert "rule" not in entry
            assert "nature" in entry
            assert "music" in entry
            assert "confidence" in entry


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


class TestTokens:
    """Test token logging support."""

    def test_tokens_are_logged(self):
        t = NatureMusicTransformer()
        test_tokens = ["[PARSE]", "decompose", "bird", "[TAG]", "label", "syllable"]
        result = t.transform(
            origin_concept="Birdsong",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="learned motifs",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = NatureMusicTransformer()
        test_tokens = [f"t{i}" for i in range(1, 19)]
        result = t.transform(
            origin_concept="Whale song",
            origin_domain="Nature",
            destination_domain="Music",
            structural_property="hierarchical phrases",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


if __name__ == "__main__":
    pytest.main([__file__, "-v"])