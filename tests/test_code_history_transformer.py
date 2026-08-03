"""
Tests for the Code ↔ History Transformer module.
"""
import pytest
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_history_transformer import (
    CodeHistoryTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_version_control_historical_record(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Git version control commits branches merge",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="branching history competing narratives synthesis",
        )
        assert result.direction == "code→history"
        assert "version" in result.isomorphisms[0].lower() or "historical" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_archival_digital_preservation(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Backup archival storage redundancy checksums",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="preservation against entropy redundancy",
        )
        assert "archival" in result.isomorphisms[0].lower() or "preservation" in result.isomorphisms[0].lower()
        assert "archival" in result.destination_concept.lower() or "preservation" in result.destination_concept.lower()

    def test_software_layers_archaeological_strata(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Software stack layers kernel library framework",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="layered structure built atop previous",
        )
        assert "software" in result.isomorphisms[0].lower() or "archaeological" in result.isomorphisms[0].lower() or "strata" in result.isomorphisms[0].lower()
        assert "archaeological" in result.destination_concept.lower() or "strata" in result.destination_concept.lower()

    def test_execution_trace_timeline(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Execution trace function calls variable state",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="chronological sequence of events",
        )
        assert "execution" in result.isomorphisms[0].lower() or "timeline" in result.isomorphisms[0].lower()
        assert "timeline" in result.destination_concept.lower() or "chronological" in result.destination_concept.lower()

    def test_paradigm_shift_scientific_revolution(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Programming paradigm shift procedural object functional",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="paradigm transformation redefining fundamentals",
        )
        assert "paradigm" in result.isomorphisms[0].lower() or "revolution" in result.isomorphisms[0].lower()
        assert "revolution" in result.destination_concept.lower() or "paradigm" in result.destination_concept.lower()

    def test_language_renaissance(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Programming language renaissance new languages emerging",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="rebirth classical synthesis new forms",
        )
        assert "renaissance" in result.isomorphisms[0].lower() or "language" in result.isomorphisms[0].lower()
        assert "renaissance" in result.destination_concept.lower() or "rebirth" in result.destination_concept.lower()

    def test_automation_industrial_revolution(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Automation CI/CD build pipeline deployment",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="machines replacing manual labor mass production",
        )
        assert "automation" in result.isomorphisms[0].lower() or "industrial" in result.isomorphisms[0].lower()
        assert "industrial" in result.destination_concept.lower() or "revolution" in result.destination_concept.lower()

    def test_documentation_oral_tradition(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Documentation README comments API docs tutorials",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="transmitted knowledge of a culture",
        )
        assert "documentation" in result.isomorphisms[0].lower() or "oral" in result.isomorphisms[0].lower() or "tradition" in result.isomorphisms[0].lower()
        assert "oral" in result.destination_concept.lower() or "tradition" in result.destination_concept.lower()

    def test_source_code_manuscript(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Source code file module import authorship",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="primary text authority provenance",
        )
        assert "source" in result.isomorphisms[0].lower() or "manuscript" in result.isomorphisms[0].lower()
        assert "manuscript" in result.destination_concept.lower() or "primary" in result.destination_concept.lower()

    def test_dark_age_technological_gap(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Legacy codebase undocumented internals lost knowledge",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="knowledge discontinuity loss of literacy",
        )
        assert "dark" in result.isomorphisms[0].lower() or "technological" in result.isomorphisms[0].lower() or "gap" in result.isomorphisms[0].lower()
        assert "dark" in result.destination_concept.lower() or "loss" in result.destination_concept.lower()


class TestBidirectionalTransformations:
    """Test history→code direction."""

    def test_history_to_code_version_control(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Historical chronicle annals primary sources",
            origin_domain="History",
            destination_domain="Coda",
            structural_property="dated events with authors commit log",
        )
        assert result.direction == "history→code"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_history_to_code_automation(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Industrial revolution steam engine assembly line",
            origin_domain="History",
            destination_domain="Coda",
            structural_property="machines replacing manual labor",
        )
        assert result.direction == "history→code"
        assert "automation" in result.destination_concept.lower() or "pipeline" in result.destination_concept.lower() or "build" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """code→history round-trip should produce historical terminology."""
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Git version control commits branches",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="branching history competing narratives",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["chronicle", "annals", "historical", "record", "manuscript", "revolution", "renaissance"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages_in_order(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Recursion",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="self-referential unfolding",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Git version control",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="branching history and merge synthesis",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Functional programming",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="purity and immutability",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated zzz",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Git version control commits branches merge",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="branching history competing narratives",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        for name, data in CodeHistoryTransformer.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict / from_dict round-trip."""

    def test_to_dict_from_dict_roundtrip(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Git version control commits branches",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="branching history competing narratives",
        )
        d = result.to_dict()
        assert d["direction"] == "code→history"
        restored = TransformerResult.from_dict(d)
        assert restored.direction == result.direction
        assert restored.origin_concept == result.origin_concept
        assert restored.destination_concept == result.destination_concept
        assert len(restored.steps) == 6
        assert restored.steps[0].stage == "PARSE"

    def test_to_dict_is_json_serializable(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="Source code manuscript",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="primary text authority",
        )
        d = result.to_dict()
        s = json.dumps(d, ensure_ascii=False)
        assert "code→history" in s
        assert "language_thread" in s


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = CodeHistoryTransformer()
        test_tokens = ["[PARSE]", "git", "commit", "[TAG]", "branch", "merge"]
        result = t.transform(
            origin_concept="Git version control",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="branching history",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = CodeHistoryTransformer()
        test_tokens = [f"t{i}" for i in range(18)]
        result = t.transform(
            origin_concept="Recursion self-call base case",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="self-referential progressive unfolding",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodeHistoryTransformer()
        moves = [
            {"from_concept": "Git version control", "from_domain": "Coda", "to_domain": "History", "structural_property": "branching history"},
            {"from_concept": "Industrial revolution", "from_domain": "History", "to_domain": "Coda", "structural_property": "machines replacing labor"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "code→history"
        assert results[1].direction == "history→code"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodeHistoryTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "version_control__historical_record" in catalog
        assert "automation__industrial_revolution" in catalog

    def test_catalog_excludes_rule(self):
        t = CodeHistoryTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data


class TestFallback:
    """Test fallback behavior for unknown concepts."""

    def test_fallback_isomorphism_for_obscure_concept(self):
        t = CodeHistoryTransformer()
        result = t.transform(
            origin_concept="zzz unknown xyz concept",
            origin_domain="Coda",
            destination_domain="History",
            structural_property="vagueness",
        )
        assert "generic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])