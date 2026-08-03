"""
Tests for the Code ↔ Medicine Transformer module.
"""
import pytest
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_medicine_transformer import (
    CodeMedicineTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_error_handling_immune_response(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Exception handling",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="error detection recovery cascade sentinel",
        )
        assert result.direction == "code→medicine"
        assert "error" in result.isomorphisms[0].lower() or "immune" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_garbage_collection_apoptosis(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Garbage collection",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="reclaim unreachable memory programmed cell death",
        )
        assert "garbage" in result.isomorphisms[0].lower() or "apoptosis" in result.isomorphisms[0].lower()
        assert "apopt" in result.destination_concept.lower() or "cell" in result.destination_concept.lower()

    def test_type_system_blood_typing(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Type system",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="static type checking compatibility constraints mismatch",
        )
        assert "type" in result.isomorphisms[0].lower() or "blood" in result.isomorphisms[0].lower()

    def test_recursion_viral_replication(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Recursion",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="self-referential base case recursive case exponential cascade",
        )
        assert "recursion" in result.isomorphisms[0].lower() or "viral" in result.isomorphisms[0].lower()

    def test_compiler_optimization_metabolic_efficiency(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Compiler optimization",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="dead-code elimination loop unrolling allosteric regulation efficiency",
        )
        assert "compiler" in result.isomorphisms[0].lower() or "metabolic" in result.isomorphisms[0].lower()

    def test_version_control_dna_repair(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Version control",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="commits diff rollback mismatch repair checkpoint",
        )
        assert "version" in result.isomorphisms[0].lower() or "dna" in result.isomorphisms[0].lower()

    def test_design_patterns_protein_folding_motifs(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Design patterns",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="reusable architectural solution recurring structural motif",
        )
        assert "design" in result.isomorphisms[0].lower() or "protein" in result.isomorphisms[0].lower()

    def test_concurrency_locking_neural_refractory(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Concurrency locking",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="mutex mutual exclusion temporal exclusion refractory period",
        )
        assert "concurrency" in result.isomorphisms[0].lower() or "refractory" in result.isomorphisms[0].lower()

    def test_caching_memoization_immune_memory(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Caching and memoization",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="store results accelerate future response memory B cells",
        )
        assert "cach" in result.isomorphisms[0].lower() or "immune" in result.isomorphisms[0].lower()

    def test_debugging_tracing_clinical_diagnosis(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Debugging and tracing",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="breakpoints stack traces hypothesis-driven differential diagnosis",
        )
        assert "debug" in result.isomorphisms[0].lower() or "diagnos" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test medicine→code direction."""

    def test_medicine_to_code_immune(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Immune response",
            origin_domain="Medicine",
            destination_domain="Code",
            structural_property="pattern recognition receptor sentinel detection recovery cascade",
        )
        assert result.direction == "medicine→code"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_medicine_to_code_apoptosis(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Apoptosis",
            origin_domain="Medicine",
            destination_domain="Code",
            structural_property="programmed cell death caspase cascade disposal homeostasis",
        )
        assert result.direction == "medicine→code"
        assert "garbage" in result.destination_concept.lower() or "collection" in result.destination_concept.lower()

    def test_medicine_to_code_dna_repair(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="DNA repair",
            origin_domain="Medicine",
            destination_domain="Code",
            structural_property="mismatch repair checkpoint rollback history",
        )
        assert result.direction == "medicine→code"
        assert "version" in result.destination_concept.lower() or "git" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """code→medicine round-trip should produce medicine-flavored destination."""
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Exception handling",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="error detection recovery cascade",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["immune", "response", "receptor", "inflammatory", "defense"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages_in_order(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Garbage collection",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="reclaim memory",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Recursion",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="self-referential cascade",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Caching and memoization",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="store results for faster recall",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20

    def test_each_step_has_confidence(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Debugging",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="systematic fault isolation",
        )
        for step in result.steps:
            assert 0.0 <= step.confidence <= 1.0

    def test_formal_rule_is_nonempty(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Type system",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="compatibility constraints",
        )
        for step in result.steps:
            assert step.formal_rule
            assert len(step.formal_rule) > 5


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Caching and memoization",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="store results accelerate future response memory",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        for name, data in CodeMedicineTransformer.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict / from_dict round-trip."""

    def test_to_dict_from_dict_roundtrip(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Version control",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="commits diff rollback",
        )
        d = result.to_dict()
        assert d["direction"] == "code→medicine"
        restored = TransformerResult.from_dict(d)
        assert restored.direction == result.direction
        assert restored.origin_concept == result.origin_concept
        assert restored.destination_concept == result.destination_concept
        assert len(restored.steps) == 6
        assert restored.steps[0].stage == "PARSE"

    def test_to_dict_keys_complete(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Design patterns",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="reusable solution",
        )
        d = result.to_dict()
        expected_keys = {
            "direction", "origin_domain", "origin_concept",
            "destination_domain", "destination_concept",
            "steps", "structural_property", "resonance_sentence",
            "tokens_seen", "tokens_per_step", "total_confidence", "isomorphisms",
        }
        assert set(d.keys()) == expected_keys

    def test_steps_serialize_correctly(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Concurrency locking",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="mutual exclusion",
        )
        d = result.to_dict()
        for step_dict in d["steps"]:
            assert "stage" in step_dict
            assert "input_repr" in step_dict
            assert "output_repr" in step_dict
            assert "formal_rule" in step_dict
            assert "confidence" in step_dict
            assert "language_thread" in step_dict


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = CodeMedicineTransformer()
        test_tokens = ["[PARSE]", "decompose", "module", "[TAG]", "label", "signal"]
        result = t.transform(
            origin_concept="Garbage collection",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="reclaim memory",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = CodeMedicineTransformer()
        test_tokens = [f"t{i}" for i in range(18)]
        result = t.transform(
            origin_concept="Exception handling",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="error detection",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step

    def test_default_tokens_without_explicit(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="Recursion",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="self-referential",
        )
        assert len(result.tokens_seen) == 6
        assert "[PARSE]" in result.tokens_seen
        assert "[VERIFY]" in result.tokens_seen


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodeMedicineTransformer()
        moves = [
            {"from_concept": "Exception handling", "from_domain": "Code", "to_domain": "Medicine", "structural_property": "error detection"},
            {"from_concept": "Immune response", "from_domain": "Medicine", "to_domain": "Code", "structural_property": "sentinel detection"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "code→medicine"
        assert results[1].direction == "medicine→code"

    def test_batch_transform_empty(self):
        t = CodeMedicineTransformer()
        results = t.batch_transform([])
        assert results == []


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodeMedicineTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "error_handling__immune_response" in catalog
        assert "debugging_tracing__clinical_diagnosis" in catalog

    def test_catalog_excludes_rule(self):
        t = CodeMedicineTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data

    def test_catalog_has_code_and_medicine_keys(self):
        t = CodeMedicineTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "code" in data
            assert "medicine" in data
            assert "confidence" in data


class TestFallback:
    """Test fallback behavior for unknown concepts."""

    def test_fallback_isomorphism_for_obscure_concept(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="zzz unknown xyz concept",
            origin_domain="Code",
            destination_domain="Medicine",
            structural_property="vagueness",
        )
        assert result.isomorphisms[0] == "generic_homomorphism__code_medicine"
        assert result.total_confidence >= 0.3

    def test_fallback_still_produces_six_steps(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="zzz unknown xyz concept",
            origin_domain="Medicine",
            destination_domain="Code",
            structural_property="vagueness",
        )
        assert len(result.steps) == 6
        assert result.direction == "medicine→code"


class TestDirectionInference:
    """Test direction inference from concept content when domain is ambiguous."""

    def test_infer_code_from_concept(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="recursion",
            origin_domain="Unknown",
            destination_domain="Medicine",
            structural_property="self-referential",
        )
        assert result.direction == "code→medicine"

    def test_infer_medicine_from_concept(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="apoptosis",
            origin_domain="Unknown",
            destination_domain="Code",
            structural_property="programmed cell death",
        )
        assert result.direction == "medicine→code"

    def test_software_keyword_in_domain(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="something",
            origin_domain="Software",
            destination_domain="Medicine",
            structural_property="structural",
        )
        assert result.direction == "code→medicine"

    def test_biology_keyword_in_domain(self):
        t = CodeMedicineTransformer()
        result = t.transform(
            origin_concept="something",
            origin_domain="Biology",
            destination_domain="Code",
            structural_property="structural",
        )
        assert result.direction == "medicine→code"


class TestDecomposeAndTag:
    """Test the _decompose and _tag_primitives helpers."""

    def test_decompose_known_code_concept(self):
        t = CodeMedicineTransformer()
        result = t._decompose("Exception handling")
        assert "exception" in result

    def test_decompose_known_medicine_concept(self):
        t = CodeMedicineTransformer()
        result = t._decompose("Apoptosis")
        assert "caspase" in result

    def test_decompose_unknown_concept(self):
        t = CodeMedicineTransformer()
        result = t._decompose("zzz unknown xyz")
        assert "elements" in result

    def test_tag_known_code_concept(self):
        t = CodeMedicineTransformer()
        result = t._tag_primitives("Concurrency locking")
        assert "exclusive" in result

    def test_tag_known_medicine_concept(self):
        t = CodeMedicineTransformer()
        result = t._tag_primitives("Neural pathways")
        assert "refractory" in result or "channel" in result

    def test_tag_unknown_concept(self):
        t = CodeMedicineTransformer()
        result = t._tag_primitives("zzz unknown xyz")
        assert "entity" in result


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2

    def test_singleton_is_correct_type(self):
        t = get_transformer()
        assert isinstance(t, CodeMedicineTransformer)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])