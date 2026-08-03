"""
Tests for the Technology ↔ Math Transformer module.
"""
import pytest
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from technology_math_transformer import (
    TechnologyMathTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_boolean_algebra_digital_circuits(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Boolean algebra",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="two-valued lattice with AND OR NOT",
        )
        assert result.direction == "math→technology"
        assert "boolean" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_finite_state_machine_cpu(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Finite state machine",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="states transitions and accept conditions",
        )
        assert "finite" in result.isomorphisms[0].lower() or "state" in result.isomorphisms[0].lower()
        assert "cpu" in result.destination_concept.lower() or "control" in result.destination_concept.lower()

    def test_graph_algorithms_network_routing(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Graph shortest path",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="weighted nodes edges minimum cost path",
        )
        assert "graph" in result.isomorphisms[0].lower()

    def test_information_theory_compression(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Shannon entropy",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="source coding entropy bound",
        )
        assert "information" in result.isomorphisms[0].lower() or "entropy" in result.isomorphisms[0].lower()

    def test_linear_algebra_3d_graphics(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Linear algebra matrix",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="affine projective transformation",
        )
        assert "linear" in result.isomorphisms[0].lower()

    def test_probability_machine_learning(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Probability theory",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="expected loss minimization",
        )
        assert "probability" in result.isomorphisms[0].lower()

    def test_automata_compilers(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Automata theory formal language",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="regular context-free grammar parser",
        )
        assert "automata" in result.isomorphisms[0].lower() or "parser" in result.isomorphisms[0].lower()

    def test_error_correcting_codes(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Algebraic coding theory",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="minimum distance parity check matrix",
        )
        assert "error" in result.isomorphisms[0].lower() or "code" in result.isomorphisms[0].lower()

    def test_cryptography_number_theory(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Number theory modular arithmetic",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="factoring discrete logarithm hardness",
        )
        assert "crypt" in result.isomorphisms[0].lower()

    def test_signal_processing_fourier(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Fourier analysis DFT",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="discrete frequency decomposition convolution",
        )
        assert "signal" in result.isomorphisms[0].lower() or "fourier" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test technology→math direction."""

    def test_technology_to_math_circuit(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Digital circuit",
            origin_domain="Technology",
            destination_domain="Mathematics",
            structural_property="logic gates implementing boolean operations",
        )
        assert result.direction == "technology→math"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_technology_to_math_cpu(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="CPU control unit",
            origin_domain="Technology",
            destination_domain="Mathematics",
            structural_property="clocked state transitions fetch decode",
        )
        assert result.direction == "technology→math"
        assert "state" in result.destination_concept.lower() or "finite" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """math→technology round-trip should produce tech-flavored destination."""
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Boolean algebra",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="two-valued lattice with AND OR NOT",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["circuit", "gate", "logic", "bit", "boolean", "digital"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages_in_order(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Group",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="closure",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Graph",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="minimal distance between nodes",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Fourier",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="frequency decomposition",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Boolean algebra",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="two-valued lattice with AND OR NOT",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        for name, data in TechnologyMathTransformer.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict / from_dict round-trip."""

    def test_to_dict_from_dict_roundtrip(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="Fourier transform",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="decomposition into frequency components",
        )
        d = result.to_dict()
        assert d["direction"] == "math→technology"
        restored = TransformerResult.from_dict(d)
        assert restored.direction == result.direction
        assert restored.origin_concept == result.origin_concept
        assert restored.destination_concept == result.destination_concept
        assert len(restored.steps) == 6
        assert restored.steps[0].stage == "PARSE"


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = TechnologyMathTransformer()
        test_tokens = ["[PARSE]", "decompose", "gate", "[TAG]", "label", "boolean"]
        result = t.transform(
            origin_concept="Boolean algebra",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="logic gates",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = TechnologyMathTransformer()
        test_tokens = [f"t{i}" for i in range(18)]
        result = t.transform(
            origin_concept="Finite state machine",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="states transitions",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = TechnologyMathTransformer()
        moves = [
            {"from_concept": "Group", "from_domain": "Mathematics", "to_domain": "Technology", "structural_property": "closure"},
            {"from_concept": "Circuit", "from_domain": "Technology", "to_domain": "Mathematics", "structural_property": "logic gates"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "math→technology"
        assert results[1].direction == "technology→math"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = TechnologyMathTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "boolean_algebra__digital_circuits" in catalog
        assert "cryptography__number_theory" in catalog

    def test_catalog_excludes_rule(self):
        t = TechnologyMathTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data


class TestFallback:
    """Test fallback behavior for unknown concepts."""

    def test_fallback_isomorphism_for_obscure_concept(self):
        t = TechnologyMathTransformer()
        result = t.transform(
            origin_concept="zzz unknown xyz concept",
            origin_domain="Mathematics",
            destination_domain="Technology",
            structural_property="vagueness",
        )
        assert result.isomorphisms[0] == "generic_homomorphism__technological_form"
        assert result.total_confidence >= 0.3


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])