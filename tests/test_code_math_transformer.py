"""
Tests for the Code ↔ Math Transformer module.
"""
import pytest
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_math_transformer import (
    CodeMathTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_turing_machine_algorithm(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Turing machine",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="tape head states transition function",
        )
        assert result.direction == "math→code"
        assert "turing" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_lambda_calculus_functional_programming(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Lambda calculus",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="function abstraction application beta reduction",
        )
        assert "lambda" in result.isomorphisms[0].lower()
        assert "functional" in result.destination_concept.lower() or "function" in result.destination_concept.lower()

    def test_type_theory_static_typing(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Type theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="type checking curry howard propositions types proofs programs",
        )
        assert "type" in result.isomorphisms[0].lower()

    def test_recursive_function_recursion(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Recursive function theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="primitive recursion minimization base case",
        )
        assert "recursive" in result.isomorphisms[0].lower()

    def test_automata_regex_engine(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Automata theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="finite automaton regular expression pattern matching",
        )
        assert "automata" in result.isomorphisms[0].lower() or "regex" in result.isomorphisms[0].lower()

    def test_category_theory_monads(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Category theory monad",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="endofunctor unit multiplication monad laws",
        )
        assert "category" in result.isomorphisms[0].lower() or "monad" in result.isomorphisms[0].lower()

    def test_graph_theory_data_structures(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Graph theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="vertices edges tree list adjacency",
        )
        assert "graph" in result.isomorphisms[0].lower()

    def test_boolean_logic_control_flow(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Boolean algebra",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="AND OR NOT if else branching logic",
        )
        assert "boolean" in result.isomorphisms[0].lower()

    def test_complexity_theory_big_o(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Computational complexity theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="asymptotic bound time space complexity NP",
        )
        assert "complexity" in result.isomorphisms[0].lower() or "big" in result.isomorphisms[0].lower()

    def test_set_theory_collections(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Set theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="union intersection membership set dict collection",
        )
        assert "set" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test both directions of transformation."""

    def test_code_to_math_algorithm(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Algorithm",
            origin_domain="Coda",
            destination_domain="Mathematics",
            structural_property="finite sequence of computational steps",
        )
        assert result.direction == "code→math"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_code_to_math_recursion(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Recursive function",
            origin_domain="Coda",
            destination_domain="Mathematics",
            structural_property="base case recursive call call stack",
        )
        assert result.direction == "code→math"
        assert "recursive" in result.destination_concept.lower() or "function" in result.destination_concept.lower()

    def test_code_to_math_with_code_domain(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Regex pattern matching",
            origin_domain="code",
            destination_domain="mathematica",
            structural_property="regular expression finite automaton",
        )
        assert result.direction == "code→math"

    def test_math_to_code_turing(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Turing machine",
            origin_domain="mathematica",
            destination_domain="Coda",
            structural_property="tape head states transition function",
        )
        assert result.direction == "math→code"
        assert "turing" in result.isomorphisms[0].lower()

    def test_round_trip_fidelity(self):
        """math→code round-trip should produce code-flavored destination."""
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Lambda calculus",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="function abstraction application beta reduction",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["function", "functional", "lambda", "haskell", "lisp", "closure"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages_in_order(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Algorithm",
            origin_domain="Coda",
            destination_domain="Mathematics",
            structural_property="steps termination correctness",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Monad",
            origin_domain="Coda",
            destination_domain="Mathematics",
            structural_property="unit bind monad laws",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Type theory",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="curry howard propositions types",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Coda",
            destination_domain="Mathematics",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Turing machine",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="tape head states transition function",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        for name, data in CodeMathTransformer.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict / from_dict round-trip."""

    def test_to_dict_from_dict_roundtrip(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="Lambda calculus",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="function abstraction and application",
        )
        d = result.to_dict()
        assert d["direction"] == "math→code"
        restored = TransformerResult.from_dict(d)
        assert restored.direction == result.direction
        assert restored.origin_concept == result.origin_concept
        assert restored.destination_concept == result.destination_concept
        assert len(restored.steps) == 6
        assert restored.steps[0].stage == "PARSE"


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = CodeMathTransformer()
        test_tokens = ["[PARSE]", "decompose", "tape", "[TAG]", "label", "state"]
        result = t.transform(
            origin_concept="Turing machine",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="tape head states",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = CodeMathTransformer()
        test_tokens = [f"t{i}" for i in range(18)]
        result = t.transform(
            origin_concept="Recursive function",
            origin_domain="Mathematics",
            destination_domain="Coda",
            structural_property="base case induction",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodeMathTransformer()
        moves = [
            {"from_concept": "Turing machine", "from_domain": "Mathematics", "to_domain": "Coda", "structural_property": "tape head states"},
            {"from_concept": "Algorithm", "from_domain": "Coda", "to_domain": "Mathematics", "structural_property": "steps termination correctness"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "math→code"
        assert results[1].direction == "code→math"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodeMathTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "turing_machine__algorithm" in catalog
        assert "set_theory__collections" in catalog

    def test_catalog_excludes_rule(self):
        t = CodeMathTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data


class TestFallback:
    """Test fallback behavior for unknown concepts."""

    def test_fallback_isomorphism_for_obscure_concept(self):
        t = CodeMathTransformer()
        result = t.transform(
            origin_concept="zzz unknown xyz concept",
            origin_domain="Coda",
            destination_domain="Mathematics",
            structural_property="vagueness",
        )
        assert result.isomorphisms[0] == "generic_homomorphism__code_form"
        assert result.total_confidence >= 0.3


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])