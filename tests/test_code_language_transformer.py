"""
Tests for the Code ↔ Language Transformer.
Covers both transformation directions, the isomorphism catalog,
batch transforms, and the fallback path for unmatched concepts.
"""
import sys
import os

import pytest

# Ensure src/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from code_language_transformer import (
    CodeLanguageTransformer,
    Direction,
    TransformationStep,
    TransformerResult,
    get_transformer,
)


# ─── Fixtures ──────────────────────────────────────────────

@pytest.fixture
def transformer():
    """Fresh transformer per test (avoids token-log bleed between tests)."""
    return CodeLanguageTransformer()


@pytest.fixture
def singleton_transformer():
    """The module-level singleton (reset before each test)."""
    import code_language_transformer as clt
    clt._default_transformer = None
    return clt.get_transformer()


# ─── Direction inference ───────────────────────────────────

class TestDirectionInference:
    def test_code_to_language_via_coda(self, transformer):
        result = transformer.transform(
            origin_concept="recursive descent parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar production rules",
        )
        assert result.direction == "code→language"

    def test_code_to_language_via_code(self, transformer):
        result = transformer.transform(
            origin_concept="AST node",
            origin_domain="code",
            destination_domain="lingua",
            structural_property="tree structure",
        )
        assert result.direction == "code→language"

    def test_language_to_code_via_lingua(self, transformer):
        result = transformer.transform(
            origin_concept="formal grammar",
            origin_domain="lingua",
            destination_domain="coda",
            structural_property="production rules",
        )
        assert result.direction == "language→code"

    def test_language_to_code_via_language(self, transformer):
        result = transformer.transform(
            origin_concept="phonology",
            origin_domain="language",
            destination_domain="coda",
            structural_property="sound system",
        )
        assert result.direction == "language→code"

    def test_direction_inference_from_concept(self, transformer):
        """When domain is ambiguous, concept content decides."""
        result = transformer.transform(
            origin_concept="parser implementation",
            origin_domain="",
            destination_domain="",
            structural_property="parsing",
        )
        assert result.direction == "code→language"


# ─── CODE_TO_LANGUAGE transforms ───────────────────────────

class TestCodeToLanguage:
    def test_parser_to_grammar(self, transformer):
        result = transformer.transform(
            origin_concept="parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar production rules",
        )
        assert result.direction == "code→language"
        assert result.origin_domain == "coda"
        assert result.destination_domain == "lingua"
        assert len(result.steps) == 6
        # The destination concept should be the 'language' side of the matched isomorphism
        assert "grammar" in result.destination_concept.lower()

    def test_type_system_to_semantics(self, transformer):
        result = transformer.transform(
            origin_concept="type system contracts",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="compositional typing",
        )
        assert result.direction == "code→language"
        assert "semantic" in result.destination_concept.lower() or "truth" in result.destination_concept.lower()

    def test_compilation_to_translation(self, transformer):
        result = transformer.transform(
            origin_concept="compiler and compilation",
            origin_domain="code",
            destination_domain="lingua",
            structural_property="source-to-target transformation",
        )
        assert result.direction == "code→language"
        assert "translation" in result.destination_concept.lower()


# ─── LANGUAGE_TO_CODE transforms ───────────────────────────

class TestLanguageToCode:
    def test_grammar_to_parser(self, transformer):
        result = transformer.transform(
            origin_concept="formal grammar production rules",
            origin_domain="lingua",
            destination_domain="coda",
            structural_property="parser",
        )
        assert result.direction == "language→code"
        assert result.origin_domain == "lingua"
        assert result.destination_domain == "coda"
        assert len(result.steps) == 6
        assert "parser" in result.destination_concept.lower()

    def test_phonology_to_encoding(self, transformer):
        result = transformer.transform(
            origin_concept="phonology sound system",
            origin_domain="lingua",
            destination_domain="coda",
            structural_property="character encoding",
        )
        assert result.direction == "language→code"
        assert "encoding" in result.destination_concept.lower() or "unicode" in result.destination_concept.lower()

    def test_dialect_to_paradigm(self, transformer):
        result = transformer.transform(
            origin_concept="linguistic dialect",
            origin_domain="language",
            destination_domain="coda",
            structural_property="programming paradigm OOP FP",
        )
        assert result.direction == "language→code"
        assert "paradigm" in result.destination_concept.lower()


# ─── Pipeline structure ────────────────────────────────────

class TestPipelineStructure:
    def test_six_stages(self, transformer):
        result = transformer.transform(
            origin_concept="parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar",
        )
        stage_names = [s.stage for s in result.steps]
        assert stage_names == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self, transformer):
        result = transformer.transform(
            origin_concept="type system",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="semantics",
        )
        for step in result.steps:
            assert isinstance(step.language_thread, str)
            assert len(step.language_thread) > 10

    def test_confidence_bounds(self, transformer):
        result = transformer.transform(
            origin_concept="parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar",
        )
        assert 0.3 <= result.total_confidence <= 0.99
        for step in result.steps:
            assert 0.0 <= step.confidence <= 1.0

    def test_tokens_per_step(self, transformer):
        custom_tokens = [f"t{i}" for i in range(18)]  # 3 per stage × 6 stages
        result = transformer.transform(
            origin_concept="parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar",
            tokens=custom_tokens,
        )
        assert len(result.tokens_per_step) == 6
        for stage_tokens in result.tokens_per_step.values():
            assert len(stage_tokens) == 3

    def test_to_dict_serializable(self, transformer):
        result = transformer.transform(
            origin_concept="parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar",
        )
        d = result.to_dict()
        assert d["direction"] == "code→language"
        assert len(d["steps"]) == 6
        assert isinstance(d["steps"][0], dict)
        assert "language_thread" in d["steps"][0]


# ─── Isomorphism catalog ───────────────────────────────────

class TestIsomorphismCatalog:
    def test_catalog_has_ten_entries(self, transformer):
        catalog = transformer.get_isomorphism_catalog()
        assert len(catalog) == 10

    def test_catalog_excludes_rule(self, transformer):
        catalog = transformer.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data
            assert "language" in data
            assert "code" in data
            assert "confidence" in data

    def test_expected_isomorphism_names(self, transformer):
        catalog = transformer.get_isomorphism_catalog()
        expected = {
            "grammar__parser",
            "syntax_tree__parse_tree",
            "semantics__type_system",
            "pragmatics__api_design",
            "translation__compilation",
            "phonology__encoding",
            "morphology__object_model",
            "rhetoric__documentation",
            "corpus__training_data",
            "dialect__programming_paradigm",
        }
        assert set(catalog.keys()) == expected

    def test_isomorphisms_dict_has_ten(self):
        assert len(CodeLanguageTransformer.ISOMORPHISMS) == 10

    def test_all_confidences_in_range(self):
        for name, data in CodeLanguageTransformer.ISOMORPHISMS.items():
            assert 0.0 < data["confidence"] <= 1.0, f"{name} confidence out of range"


# ─── Batch transform ───────────────────────────────────────

class TestBatchTransform:
    def test_batch_multiple_moves(self, transformer):
        moves = [
            {
                "from_concept": "parser implementation",
                "from_domain": "coda",
                "to_domain": "lingua",
                "structural_property": "grammar rules",
            },
            {
                "from_concept": "phonology",
                "from_domain": "lingua",
                "to_domain": "coda",
                "structural_property": "encoding",
            },
            {
                "from_concept": "training data",
                "from_domain": "code",
                "to_domain": "lingua",
                "structural_property": "corpus",
            },
        ]
        results = transformer.batch_transform(moves)
        assert len(results) == 3
        assert results[0].direction == "code→language"
        assert results[1].direction == "language→code"
        assert results[2].direction == "code→language"

    def test_batch_empty(self, transformer):
        results = transformer.batch_transform([])
        assert results == []

    def test_batch_preserves_resonance_sentence(self, transformer):
        moves = [
            {
                "from_concept": "parser",
                "from_domain": "coda",
                "to_domain": "lingua",
                "structural_property": "grammar",
                "resonance_sentence": "Custom resonance for test",
            },
        ]
        results = transformer.batch_transform(moves)
        assert results[0].resonance_sentence == "Custom resonance for test"


# ─── Fallback ──────────────────────────────────────────────

class TestFallback:
    def test_fallback_for_unknown_concept(self, transformer):
        """A concept with no keyword overlap should trigger the generic fallback."""
        result = transformer.transform(
            origin_concept="zzzqxx",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="zzzqxx",
        )
        assert result.direction == "code→language"
        assert len(result.steps) == 6
        # Fallback isomorphism name
        assert "generic_correspondence" in result.isomorphisms[0]
        assert result.total_confidence >= 0.3

    def test_fallback_destination_concept_generic(self, transformer):
        result = transformer.transform(
            origin_concept="zzzqxx",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="zzzqxx",
        )
        assert "zzzqxx" in result.destination_concept.lower()

    def test_fallback_language_to_code(self, transformer):
        result = transformer.transform(
            origin_concept="zzzqxx",
            origin_domain="lingua",
            destination_domain="coda",
            structural_property="zzzqxx",
        )
        assert result.direction == "language→code"
        assert "generic_correspondence" in result.isomorphisms[0]


# ─── Singleton ─────────────────────────────────────────────

class TestSingleton:
    def test_get_transformer_returns_instance(self, singleton_transformer):
        assert isinstance(singleton_transformer, CodeLanguageTransformer)

    def test_singleton_is_reused(self):
        import code_language_transformer as clt
        clt._default_transformer = None
        t1 = clt.get_transformer()
        t2 = clt.get_transformer()
        assert t1 is t2


# ─── Decompose / tag primitives ────────────────────────────

class TestDecomposeAndTag:
    def test_decompose_parser(self, transformer):
        result = transformer._decompose("recursive descent parser")
        assert "tokenizer" in result or "grammar" in result or "parse table" in result

    def test_decompose_grammar(self, transformer):
        result = transformer._decompose("formal grammar")
        assert "production" in result or "non-terminal" in result

    def test_decompose_unknown_returns_generic(self, transformer):
        result = transformer._decompose("zzzqxx unknown")
        assert "constructs" in result

    def test_tag_primitives_parser(self, transformer):
        result = transformer._tag_primitives("parser implementation")
        assert "rule" in result or "action" in result

    def test_tag_primitives_unknown_returns_generic(self, transformer):
        result = transformer._tag_primitives("zzzqxx unknown")
        assert "entity" in result


# ─── Round-trip (both directions with same concept pair) ───

class TestRoundTrip:
    def test_grammar_parser_both_directions(self, transformer):
        c2l = transformer.transform(
            origin_concept="parser",
            origin_domain="coda",
            destination_domain="lingua",
            structural_property="grammar production rules",
        )
        l2c = transformer.transform(
            origin_concept="formal grammar",
            origin_domain="lingua",
            destination_domain="coda",
            structural_property="parser implementation",
        )
        assert c2l.direction == "code→language"
        assert l2c.direction == "language→code"
        # Both should reference the same isomorphism family
        assert "grammar" in c2l.isomorphisms[0].lower()
        assert "grammar" in l2c.isomorphisms[0].lower()