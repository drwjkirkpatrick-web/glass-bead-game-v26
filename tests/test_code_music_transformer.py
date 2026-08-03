"""
Tests for the Code ↔ Music Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_music_transformer import (
    CodeMusicTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_algorithmic_composition_code_as_score(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Algorithmic composition",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="program logic as compositional score",
        )
        assert result.direction == "code→music"
        assert "algorithmic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_midi_encoding_digital_audio(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="MIDI protocol encoding",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="digital message stream as symbolic music representation",
        )
        assert "midi" in result.isomorphisms[0].lower()
        assert "audio" in result.destination_concept.lower() or "waveform" in result.destination_concept.lower()

    def test_recursive_structure_canon_fugue(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Recursive code structure",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="self-referential call with base case termination",
        )
        assert "recursive" in result.isomorphisms[0].lower() or "canon" in result.isomorphisms[0].lower()

    def test_fft_audio_dsp(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="FFT algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="time-domain to frequency-domain transformation",
        )
        assert "fft" in result.isomorphisms[0].lower()
        assert "dsp" in result.destination_concept.lower() or "spectral" in result.destination_concept.lower() or "audio" in result.destination_concept.lower()

    def test_pattern_matching_motivic_development(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Pattern matching algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="identifying and extracting recurring sub-structures",
        )
        assert "pattern" in result.isomorphisms[0].lower()

    def test_state_machine_musical_form(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="State machine",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="finite states with transition rules",
        )
        assert "state" in result.isomorphisms[0].lower()

    def test_seeded_rng_stochastic_composition(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Seeded random number generator",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="deterministic pseudo-random sequence from seed",
        )
        assert "seed" in result.isomorphisms[0].lower() or "stochastic" in result.isomorphisms[0].lower()

    def test_dataflow_signal_flow(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Dataflow programming",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="directed graph of processing nodes with data edges",
        )
        assert "dataflow" in result.isomorphisms[0].lower() or "signal" in result.isomorphisms[0].lower()

    def test_markov_chains_generative_music(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Markov chain",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="stochastic process with transition probability matrix",
        )
        assert "markov" in result.isomorphisms[0].lower()

    def test_abstraction_orchestration(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Code abstraction and encapsulation",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="hiding implementation behind interfaces",
        )
        assert "abstraction" in result.isomorphisms[0].lower() or "orchestr" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test music→code direction."""

    def test_music_to_code_canon(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Canon form",
            origin_domain="musica",
            destination_domain="coda",
            structural_property="recursive self-referential melodic imitation",
        )
        assert result.direction == "music→code"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_music_to_code_digital_audio(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Digital audio waveform",
            origin_domain="musica",
            destination_domain="coda",
            structural_property="discrete sampling of continuous sound",
        )
        assert result.direction == "music→code"
        assert "midi" in result.isomorphisms[0].lower() or "fft" in result.isomorphisms[0].lower()

    def test_music_to_code_generative(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Generative music",
            origin_domain="musica",
            destination_domain="coda",
            structural_property="algorithmic composition with controlled randomness",
        )
        assert result.direction == "music→code"
        assert "markov" in result.isomorphisms[0].lower() or "seed" in result.isomorphisms[0].lower()

    def test_round_trip_fidelity(self):
        """code→music should produce a destination concept with musical terminology."""
        t = CodeMusicTransformer()
        result1 = t.transform(
            origin_concept="Recursive code structure",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="self-referential call with base case",
        )
        assert any(word in result1.destination_concept.lower() for word in
                    ["canon", "fugue", "theme", "voice", "imitation", "score", "sonic", "audio", "musical", "timbre"])


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = CodeMusicTransformer()
        test_tokens = ["[PARSE]", "decompose", "algorithm", "[TAG]", "label", "recursive"]
        result = t.transform(
            origin_concept="Algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="sequential procedure with termination",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = CodeMusicTransformer()
        test_tokens = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18"]
        result = t.transform(
            origin_concept="FFT algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="frequency domain transformation",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="FFT algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="time-domain to frequency-domain transformation",
        )
        assert result.total_confidence >= 0.85


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodeMusicTransformer()
        moves = [
            {"from_concept": "Algorithm", "from_domain": "coda", "to_domain": "musica", "structural_property": "sequential procedure"},
            {"from_concept": "Canon", "from_domain": "musica", "to_domain": "coda", "structural_property": "recursive imitation"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "code→music"
        assert results[1].direction == "music→code"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodeMusicTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "algorithmic_composition__code_as_score" in catalog
        assert "midi_encoding__digital_audio" in catalog
        assert "recursive_structure__canon_fugue" in catalog
        assert "fft__audio_dsp" in catalog
        assert "pattern_matching__motivic_development" in catalog
        assert "state_machine__musical_form" in catalog
        assert "seeded_rng__stochastic_composition" in catalog
        assert "dataflow__signal_flow" in catalog
        assert "markov_chains__generative_music" in catalog
        assert "abstraction__orchestration" in catalog


class TestLanguageThread:
    """Test human language as connecting thread."""

    def test_each_step_has_language_thread(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="Algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="sequential procedure",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="State machine",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="finite states with transitions",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestFallback:
    """Test fallback isomorphism when no good match is found."""

    def test_fallback_isomorphism_used(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="zzzz totally unrelated gibberish qqqq",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="xxxx nothing matching yyyy",
        )
        assert result.total_confidence >= 0.3
        assert len(result.steps) == 6
        assert result.isomorphisms  # Should still have an isomorphism name

    def test_fallback_music_to_code(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="zzzz totally unrelated gibberish qqqq",
            origin_domain="musica",
            destination_domain="coda",
            structural_property="xxxx nothing matching yyyy",
        )
        assert result.direction == "music→code"
        assert result.total_confidence >= 0.3
        assert len(result.steps) == 6


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


class TestToDict:
    """Test serialization to dictionary."""

    def test_to_dict_structure(self):
        t = CodeMusicTransformer()
        result = t.transform(
            origin_concept="FFT algorithm",
            origin_domain="coda",
            destination_domain="musica",
            structural_property="frequency domain transformation",
        )
        d = result.to_dict()
        assert d["direction"] == "code→music"
        assert d["origin_domain"] == "coda"
        assert d["destination_domain"] == "musica"
        assert len(d["steps"]) == 6
        assert "total_confidence" in d
        assert "isomorphisms" in d


if __name__ == "__main__":
    pytest.main([__file__, "-v"])