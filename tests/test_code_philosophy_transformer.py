"""
Tests for the Code ↔ Philosophy Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_philosophy_transformer import (
    CodePhilosophyTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library (code→philosophy)."""

    def test_formal_logic_boolean_code(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Boolean code",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="conditional logic and if-then branching",
        )
        assert result.direction == "code→philosophy"
        assert "formal_logic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_ontology_data_model(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Data model",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="schema and entity-relationship structure",
        )
        assert "ontology" in result.isomorphisms[0].lower()
        assert "ontolog" in result.destination_concept.lower()

    def test_epistemology_machine_learning(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Machine learning",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="learning knowledge from data and generalization",
        )
        assert "epistemolog" in result.isomorphisms[0].lower() or "machine" in result.isomorphisms[0].lower()

    def test_ethics_code_of_conduct(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Code of conduct",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="AI ethics and responsible engineering principles",
        )
        assert "ethic" in result.isomorphisms[0].lower()

    def test_dialectic_refactoring(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Refactoring",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="thesis antithesis synthesis in code evolution",
        )
        assert "dialect" in result.isomorphisms[0].lower() or "refactor" in result.isomorphisms[0].lower()

    def test_phenomenology_ux_design(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="UX design",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="lived experience and affordances of interface",
        )
        assert "phenomen" in result.isomorphisms[0].lower() or "ux" in result.isomorphisms[0].lower()

    def test_determinism_algorithmic_predictability(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Algorithmic determinism",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="same inputs yield same outputs predictability",
        )
        assert "determin" in result.isomorphisms[0].lower()

    def test_teleology_design_patterns(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Design patterns",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="intent and purpose encoded in reusable structure",
        )
        assert "teleolog" in result.isomorphisms[0].lower() or "pattern" in result.isomorphisms[0].lower()

    def test_axiology_code_quality(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Code quality",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="value metrics complexity cohesion coupling",
        )
        assert "axiolog" in result.isomorphisms[0].lower() or "quality" in result.isomorphisms[0].lower()

    def test_metaphysics_virtual_worlds(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Virtual worlds",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="simulation reality and simulated existence",
        )
        assert "metaphys" in result.isomorphisms[0].lower() or "virtual" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test philosophy→code direction."""

    def test_philosophy_to_code_dialectic(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Dialectical synthesis",
            origin_domain="philosophia",
            destination_domain="coda",
            structural_property="thesis antithesis resolved into higher unity through refactoring",
        )
        assert result.direction == "philosophy→code"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_philosophy_to_code_epistemology(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Epistemology of knowledge",
            origin_domain="philosophia",
            destination_domain="coda",
            structural_property="how we know and learn from data",
        )
        assert result.direction == "philosophy→code"
        assert "epistemolog" in result.isomorphisms[0].lower() or "machine" in result.isomorphisms[0].lower()

    def test_philosophy_to_code_ethics(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Ethics of AI",
            origin_domain="philosophia",
            destination_domain="coda",
            structural_property="right action and responsible conduct in engineering",
        )
        assert result.direction == "philosophy→code"
        assert "ethic" in result.isomorphisms[0].lower()

    def test_round_trip_fidelity(self):
        """code→philosophy destination should contain philosophical terminology."""
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Boolean code",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="conditional logic and deductive inference",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["logic", "syllogism", "deductive", "inference", "premise"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Data model",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="schema entity relation",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Refactoring",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="dialectical evolution of code",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Virtual worlds",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="simulation of reality",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Boolean code",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="conditional logic and syllogistic inference",
        )
        assert result.total_confidence >= 0.85

    def test_isomorphism_confidences_in_range(self):
        """Every isomorphism in the library has confidence in [0.85, 0.99]."""
        t = CodePhilosophyTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test JSON serialization round-trip."""

    def test_to_dict_has_all_fields(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Data model",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="schema entity relation",
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
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Data model",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="schema entity relation",
        )
        step_dict = result.to_dict()["steps"][0]
        required = {"stage", "input_repr", "output_repr", "formal_rule", "confidence", "language_thread"}
        assert required.issubset(step_dict.keys())

    def test_serialization_round_trip(self):
        """Result to_dict -> JSON -> dict preserves key data."""
        import json
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Design patterns",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="intent and reusable structure",
        )
        d = result.to_dict()
        js = json.dumps(d)
        d2 = json.loads(js)
        assert d2["direction"] == d["direction"]
        assert d2["origin_concept"] == d["origin_concept"]
        assert d2["total_confidence"] == d["total_confidence"]
        assert len(d2["steps"]) == 6

    def test_from_dict_round_trip(self):
        """TransformerResult.from_dict reconstructs from a dict."""
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Code quality",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="value metrics",
        )
        d = result.to_dict()
        reconstructed = TransformerResult.from_dict(d)
        assert reconstructed.direction == result.direction
        assert reconstructed.origin_concept == result.origin_concept
        assert reconstructed.total_confidence == result.total_confidence
        assert len(reconstructed.steps) == 6
        assert reconstructed.steps[0].stage == "PARSE"


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodePhilosophyTransformer()
        moves = [
            {"from_concept": "Data model", "from_domain": "coda", "to_domain": "philosophia", "structural_property": "schema entity"},
            {"from_concept": "Dialectic", "from_domain": "philosophia", "to_domain": "coda", "structural_property": "thesis antithesis synthesis refactoring"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "code→philosophy"
        assert results[1].direction == "philosophy→code"

    def test_batch_transform_preserves_order(self):
        t = CodePhilosophyTransformer()
        moves = [
            {"from_concept": "Boolean code", "from_domain": "coda", "to_domain": "philosophia", "structural_property": "conditional logic"},
            {"from_concept": "Ethics", "from_domain": "philosophia", "to_domain": "coda", "structural_property": "conduct responsibility"},
            {"from_concept": "Virtual worlds", "from_domain": "coda", "to_domain": "philosophia", "structural_property": "simulation reality"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 3
        assert "formal_logic" in results[0].isomorphisms[0].lower()
        assert results[1].direction == "philosophy→code"


class TestFallbackIsomorphism:
    """Test fallback when no isomorphism matches."""

    def test_fallback_for_obscure_concept(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="zzz obscure nonsense xyz",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="zzz vague xyz",
        )
        assert result.isomorphisms  # should have a fallback name
        assert "generic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3

    def test_fallback_direction_inference(self):
        """When domain is ambiguous, direction is inferred from concept content."""
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="function",
            origin_domain="Unknown",
            destination_domain="philosophia",
            structural_property="computation",
        )
        assert result.direction in ("code→philosophy", "philosophy→code")


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodePhilosophyTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "formal_logic__boolean_code" in catalog
        assert "metaphysics__virtual_worlds" in catalog

    def test_catalog_excludes_rule(self):
        t = CodePhilosophyTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data
            assert "code" in data
            assert "philosophy" in data
            assert "confidence" in data


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = CodePhilosophyTransformer()
        test_tokens = ["[PARSE]", "decompose", "schema", "[TAG]", "label", "entity"]
        result = t.transform(
            origin_concept="Data model",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="schema entity relation",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = CodePhilosophyTransformer()
        test_tokens = [f"t{i}" for i in range(1, 19)]
        result = t.transform(
            origin_concept="Boolean code",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="conditional logic",
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


class TestDirectionInference:
    """Test direction inference from domain strings."""

    def test_coda_domain_is_code_to_philosophy(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Algorithm",
            origin_domain="coda",
            destination_domain="philosophia",
            structural_property="determinism",
        )
        assert result.direction == "code→philosophy"

    def test_code_domain_is_code_to_philosophy(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Algorithm",
            origin_domain="code",
            destination_domain="philosophia",
            structural_property="determinism",
        )
        assert result.direction == "code→philosophy"

    def test_philosophia_domain_is_philosophy_to_code(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Ontology",
            origin_domain="philosophia",
            destination_domain="coda",
            structural_property="being and existence",
        )
        assert result.direction == "philosophy→code"

    def test_philosophy_domain_is_philosophy_to_code(self):
        t = CodePhilosophyTransformer()
        result = t.transform(
            origin_concept="Ontology",
            origin_domain="philosophy",
            destination_domain="coda",
            structural_property="being and existence",
        )
        assert result.direction == "philosophy→code"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])