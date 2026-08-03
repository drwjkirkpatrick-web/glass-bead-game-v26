"""
Tests for the Math ↔ Philosophy Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from math_philosophy_transformer import (
    MathPhilosophyTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library (math→philosophy)."""

    def test_godel_incompleteness(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Gödel incompleteness",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="true but unprovable statements in formal systems",
        )
        assert result.direction == "math→philosophy"
        assert "godel" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_set_theory_ontology(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Set theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="membership relation structuring all objects",
        )
        assert "set" in result.isomorphisms[0].lower()
        assert "ontolog" in result.destination_concept.lower()

    def test_group_symmetry_dialectical(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Group symmetry",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="thesis antithesis synthesis under composition",
        )
        assert "group" in result.isomorphisms[0].lower() or "dialect" in result.isomorphisms[0].lower()

    def test_topology_phenomenology(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Topological space",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="properties preserved under continuous deformation",
        )
        assert "topolog" in result.isomorphisms[0].lower()

    def test_probability_induction(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Probability theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="Bayesian inference updating belief from evidence",
        )
        assert "probab" in result.isomorphisms[0].lower()

    def test_category_theory_metaphysics(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Category theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="objects morphisms functors natural transformations",
        )
        assert "category" in result.isomorphisms[0].lower()

    def test_formal_logic_syllogistic(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Formal logic",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="modus ponens deductive validity",
        )
        assert "logic" in result.isomorphisms[0].lower() or "syllog" in result.isomorphisms[0].lower()

    def test_cantor_infinity(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Cantor infinity",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="transfinite cardinalities hierarchy",
        )
        assert "infinity" in result.isomorphisms[0].lower() or "cantor" in result.isomorphisms[0].lower()

    def test_game_theory_ethics(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Game theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="Nash equilibrium among interdependent rational agents",
        )
        assert "game" in result.isomorphisms[0].lower()

    def test_fractal_hermeneutic(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Fractal geometry",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="self-similarity across scales",
        )
        assert "fractal" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test philosophy→math direction."""

    def test_philosophy_to_math_dialectic(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Dialectical synthesis",
            origin_domain="Philosophy",
            destination_domain="Mathematics",
            structural_property="thesis antithesis resolved into higher unity",
        )
        assert result.direction == "philosophy→math"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_philosophy_to_math_induction(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Induction problem",
            origin_domain="Philosophy",
            destination_domain="Mathematics",
            structural_property="finite observations justifying universal generalization",
        )
        assert result.direction == "philosophy→math"
        assert "probab" in result.isomorphisms[0].lower()

    def test_philosophy_to_math_ethics(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Ethics of cooperation",
            origin_domain="Philosophy",
            destination_domain="Mathematics",
            structural_property="right action among interdependent agents",
        )
        assert result.direction == "philosophy→math"
        assert "game" in result.isomorphisms[0].lower()

    def test_round_trip_fidelity(self):
        """math→philosophy destination should contain philosophical terminology."""
        t = MathPhilosophyTransformer()
        result1 = t.transform(
            origin_concept="Gödel incompleteness",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="true but unprovable statements",
        )
        assert any(word in result1.destination_concept.lower() for word in
                    ["epistemolog", "limit", "knowledge", "framework", "bound"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Set theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="membership relation",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Group symmetry",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="composition of symmetries",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Fractal geometry",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="self-similar across scales",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Gödel incompleteness",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="true but unprovable statements in formal systems",
        )
        assert result.total_confidence >= 0.85

    def test_isomorphism_confidences_in_range(self):
        """Every isomorphism in the library has confidence in [0.85, 0.99]."""
        t = MathPhilosophyTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test JSON serialization round-trip."""

    def test_to_dict_has_all_fields(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Set theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="membership relation",
        )
        d = result.to_dict()
        required = {
            "direction", "origin_domain", "origin_concept",
            "destination_domain", "destination_concept",
            "steps", "structural_property", "resonance_sentence",
            "tokens_seen", "tokens_per_step", "total_confidence", "isomorphisms",
        }
        assert required.issubset(d.keys())
        assert isinstance(d["steps"], list)
        assert len(d["steps"]) == 6
        assert isinstance(d["steps"][0], dict)

    def test_step_dict_has_all_fields(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Set theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="membership relation",
        )
        step = result.steps[0].to_dict() if hasattr(result.steps[0], "to_dict") else result.to_dict()["steps"][0]
        required = {"stage", "input_repr", "output_repr", "formal_rule", "confidence", "language_thread"}
        # steps are dataclasses; check via asdict equivalent in to_dict
        step_dict = result.to_dict()["steps"][0]
        assert required.issubset(step_dict.keys())

    def test_serialization_round_trip(self):
        """Result to_dict -> JSON -> dict preserves key data."""
        import json
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="Game theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="Nash equilibrium",
        )
        d = result.to_dict()
        js = json.dumps(d)
        d2 = json.loads(js)
        assert d2["direction"] == d["direction"]
        assert d2["origin_concept"] == d["origin_concept"]
        assert d2["total_confidence"] == d["total_confidence"]
        assert len(d2["steps"]) == 6


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = MathPhilosophyTransformer()
        moves = [
            {"from_concept": "Set theory", "from_domain": "Mathematics", "to_domain": "Philosophy", "structural_property": "membership"},
            {"from_concept": "Dialectic", "from_domain": "Philosophy", "to_domain": "Mathematics", "structural_property": "thesis antithesis synthesis"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "math→philosophy"
        assert results[1].direction == "philosophy→math"

    def test_batch_transform_preserves_order(self):
        t = MathPhilosophyTransformer()
        moves = [
            {"from_concept": "Gödel", "from_domain": "Mathematics", "to_domain": "Philosophy", "structural_property": "incompleteness"},
            {"from_concept": "Ethics", "from_domain": "Philosophy", "to_domain": "Mathematics", "structural_property": "cooperation"},
            {"from_concept": "Cantor", "from_domain": "Mathematics", "to_domain": "Philosophy", "structural_property": "infinity"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 3
        assert "godel" in results[0].isomorphisms[0].lower()
        assert results[1].direction == "philosophy→math"


class TestFallbackIsomorphism:
    """Test fallback when no isomorphism matches."""

    def test_fallback_for_obscure_concept(self):
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="zzz obscure nonsense xyz",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="zzz vague xyz",
        )
        assert result.isomorphisms  # should have a fallback name
        assert "generic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3

    def test_fallback_direction_inference(self):
        """When domain is ambiguous, direction is inferred from concept content."""
        t = MathPhilosophyTransformer()
        result = t.transform(
            origin_concept="group",
            origin_domain="Unknown",
            destination_domain="Philosophy",
            structural_property="symmetry",
        )
        assert result.direction in ("math→philosophy", "philosophy→math")


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = MathPhilosophyTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "godel_incompleteness__epistemological_limits" in catalog
        assert "game_theory__ethics" in catalog

    def test_catalog_excludes_rule(self):
        t = MathPhilosophyTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data
            assert "math" in data
            assert "philosophy" in data
            assert "confidence" in data


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = MathPhilosophyTransformer()
        test_tokens = ["[PARSE]", "decompose", "set", "[TAG]", "label", "membership"]
        result = t.transform(
            origin_concept="Set theory",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="membership relation",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = MathPhilosophyTransformer()
        test_tokens = [f"t{i}" for i in range(1, 19)]
        result = t.transform(
            origin_concept="Logic",
            origin_domain="Mathematics",
            destination_domain="Philosophy",
            structural_property="modus ponens",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])