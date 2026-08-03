"""
Tests for the Philosophy ↔ Language Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from philosophy_language_transformer import (
    PhilosophyLanguageTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_wittgenstein_games_speech_acts(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Wittgenstein language games",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="meaning as use within a form of life",
        )
        assert result.direction == "philosophy→language"
        assert "wittgenstein" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_saussure_signifier_platonic_forms(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Saussure signifier signified",
            origin_domain="Linguistics",
            destination_domain="Philosophy",
            structural_property="arbitrary sign uniting sound-image and concept",
        )
        assert result.direction == "language→philosophy"
        assert "saussure" in result.isomorphisms[0].lower() or "platonic" in result.isomorphisms[0].lower()

    def test_derrida_difference_semantic_indeterminacy(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Derrida différance",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="deferral of meaning through chains of signifiers",
        )
        assert "derrida" in result.isomorphisms[0].lower() or "diff" in result.isomorphisms[0].lower()

    def test_heidegger_being_ontological_grammar(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Heidegger Being",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="disclosedness structured by care and temporality",
        )
        assert "heidegger" in result.isomorphisms[0].lower()

    def test_quine_indeterminacy_hermeneutic_circle(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Quine indeterminacy of translation",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="no fact of the matter fixes unique meaning",
        )
        assert "quine" in result.isomorphisms[0].lower()

    def test_austin_performatives_pragmatics(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Austin performatives",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="utterances constituting the act they name",
        )
        assert "austin" in result.isomorphisms[0].lower()

    def test_frege_sense_reference_semantics(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Frege sense and reference",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="mode of presentation versus object denoted",
        )
        assert "frege" in result.isomorphisms[0].lower()

    def test_whorf_sapir_epistemic_relativism(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Whorf-Sapir linguistic relativity",
            origin_domain="Linguistics",
            destination_domain="Philosophy",
            structural_property="grammatical categories shape habitual cognition",
        )
        assert "whorf" in result.isomorphisms[0].lower() or "sapir" in result.isomorphisms[0].lower()

    def test_grice_implicature_logical_pragmatics(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Grice implicature",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="conversational meaning beyond literal content",
        )
        assert "grice" in result.isomorphisms[0].lower()

    def test_habermas_discourse_ethics(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Habermas communicative rationality",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="reason grounded in uncoerced discourse",
        )
        assert "habermas" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test the language→philosophy direction."""

    def test_language_to_philosophy_speech_act(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Speech act theory",
            origin_domain="Linguistics",
            destination_domain="Philosophy",
            structural_property="utterances perform illocutionary acts",
        )
        assert result.direction == "language→philosophy"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_language_to_philosophy_semantics(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Formal semantics",
            origin_domain="Linguistics",
            destination_domain="Philosophy",
            structural_property="compositional truth-conditional content",
        )
        assert result.direction == "language→philosophy"
        assert "frege" in result.isomorphisms[0].lower()

    def test_round_trip_identity(self):
        """philosophy→language destination concept should contain linguistic terminology."""
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Austin performatives",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="utterances constituting the act they name",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["speech", "act", "pragmatic", "utterance", "locution", "discourse"])


class TestPipelineStructure:
    """Test the 6-stage pipeline."""

    def test_six_stages_present(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Frege sense reference",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="mode of presentation vs denotation",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Heidegger Being",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="disclosedness",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Grice implicature",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="conversational inference",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Austin performatives",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="utterances constituting the act they name",
        )
        assert result.total_confidence >= 0.85

    def test_isomorphism_confidences_in_range(self):
        """Every isomorphism confidence must be 0.85–0.99."""
        t = PhilosophyLanguageTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} out of range"


class TestSerialisation:
    """Test JSON serialisation round-trip."""

    def test_to_dict_round_trip(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="Wittgenstein language games",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="meaning as use",
        )
        d = result.to_dict()
        assert d["direction"] == "philosophy→language"
        assert len(d["steps"]) == 6
        assert d["steps"][0]["stage"] == "PARSE"
        # Every step dict must have all expected fields
        for step_dict in d["steps"]:
            assert "language_thread" in step_dict
            assert "formal_rule" in step_dict
            assert "confidence" in step_dict


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = PhilosophyLanguageTransformer()
        moves = [
            {"from_concept": "Wittgenstein language games", "from_domain": "Philosophy",
             "to_domain": "Language", "structural_property": "meaning as use"},
            {"from_concept": "Speech act theory", "from_domain": "Linguistics",
             "to_domain": "Philosophy", "structural_property": "illocutionary force"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "philosophy→language"
        assert results[1].direction == "language→philosophy"


class TestFallbackIsomorphism:
    """Test that obscure inputs fall back to a generic correspondence."""

    def test_fallback_used_for_obscure_input(self):
        t = PhilosophyLanguageTransformer()
        result = t.transform(
            origin_concept="zzz qqx wwk",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="zzz qqx wwk",
        )
        assert "generic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = PhilosophyLanguageTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "wittgenstein_games__speech_act_theory" in catalog
        assert "frege_sense_reference__semantics" in catalog

    def test_catalog_excludes_rule_key(self):
        t = PhilosophyLanguageTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data
            assert "philosophy" in data
            assert "language" in data
            assert "confidence" in data


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = PhilosophyLanguageTransformer()
        test_tokens = ["[PARSE]", "decompose", "concept", "[TAG]", "label", "philosophical"]
        result = t.transform(
            origin_concept="Heidegger Being",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="disclosedness of entities",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = PhilosophyLanguageTransformer()
        test_tokens = ["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9",
                        "t10", "t11", "t12", "t13", "t14", "t15", "t16", "t17", "t18"]
        result = t.transform(
            origin_concept="Frege sense reference",
            origin_domain="Philosophy",
            destination_domain="Language",
            structural_property="mode of presentation",
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