"""
Tests for the Code ↔ Technology Transformer module.
"""
import pytest
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_technology_transformer import (
    CodeTechnologyTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_api_hardware_interface(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="function signatures type contracts parameter return conventions",
        )
        assert result.direction == "code→technology"
        assert "api" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_embedded_code_firmware(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Embedded code",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="registers interrupts boot persistent low-level",
        )
        assert "embedded" in result.isomorphisms[0].lower() or "firmware" in result.isomorphisms[0].lower()
        assert "firmware" in result.destination_concept.lower()

    def test_network_protocol_network_code(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Network protocol specification",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="packet format handshake state machine sequencing",
        )
        assert result.direction == "technology→code"
        assert "network" in result.isomorphisms[0].lower() or "protocol" in result.isomorphisms[0].lower()

    def test_database_query_language(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Database engine",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="storage optimizer transaction index ACID",
        )
        assert "database" in result.isomorphisms[0].lower()

    def test_os_kernel_kernel_code(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="OS kernel architecture",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="scheduler memory manager syscall VFS process",
        )
        assert "kernel" in result.isomorphisms[0].lower()

    def test_cloud_infrastructure_iac(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Cloud infrastructure",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="virtual machines load balancers VPC subnets",
        )
        assert "cloud" in result.isomorphisms[0].lower()

    def test_cryptography_crypto_libraries(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Cryptographic algorithms AES RSA",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="finite fields number theory security proof constant-time",
        )
        assert "crypt" in result.isomorphisms[0].lower()

    def test_ui_framework_frontend_code(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="UI framework React Vue",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="component tree virtual DOM reactive state lifecycle",
        )
        assert "ui" in result.isomorphisms[0].lower() or "frontend" in result.isomorphisms[0].lower()

    def test_vcs_git_internals(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Version control concepts",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="commits branches merges diffs history graph",
        )
        assert "vcs" in result.isomorphisms[0].lower() or "git" in result.isomorphisms[0].lower()

    def test_compiler_toolchain_build_systems(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Compiler toolchain",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="lexer parser IR optimizer code generator",
        )
        assert "compiler" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test both directions of the transformation."""

    def test_code_to_technology_api(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="function signatures type contracts",
        )
        assert result.direction == "code→technology"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3
        assert "hardware" in result.destination_concept.lower() or "interface" in result.destination_concept.lower()

    def test_technology_to_code_firmware(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Firmware",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="persistent low-level registers interrupts boot",
        )
        assert result.direction == "technology→code"
        assert "embedded" in result.destination_concept.lower() or "code" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """code→technology round-trip should produce tech-flavored destination."""
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="function signatures type contracts parameter return",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["hardware", "interface", "pinout", "spec", "signal", "device"])

    def test_direction_inference_from_code_keyword(self):
        """If origin_domain has 'code' it should infer code→technology."""
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Git internals",
            origin_domain="code",
            destination_domain="technologia",
            structural_property="object store DAG commit hash",
        )
        assert result.direction == "code→technology"


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages_in_order(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="contracts signatures",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="React frontend",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="components hooks virtual DOM",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="SQL query language",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="declarative statements execution plans",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="function signatures type contracts parameter return conventions",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        for name, data in CodeTechnologyTransformer.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict / from_dict round-trip."""

    def test_to_dict_from_dict_roundtrip(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="function signatures type contracts",
        )
        d = result.to_dict()
        assert d["direction"] == "code→technology"
        restored = TransformerResult.from_dict(d)
        assert restored.direction == result.direction
        assert restored.origin_concept == result.origin_concept
        assert restored.destination_concept == result.destination_concept
        assert len(restored.steps) == 6
        assert restored.steps[0].stage == "PARSE"


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = CodeTechnologyTransformer()
        test_tokens = ["[PARSE]", "decompose", "api", "[TAG]", "label", "contract"]
        result = t.transform(
            origin_concept="Software API",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="function signatures",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = CodeTechnologyTransformer()
        test_tokens = [f"t{i}" for i in range(18)]
        result = t.transform(
            origin_concept="Embedded code",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="registers interrupts",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodeTechnologyTransformer()
        moves = [
            {"from_concept": "Software API", "from_domain": "coda", "to_domain": "technologia", "structural_property": "function signatures"},
            {"from_concept": "Firmware", "from_domain": "technologia", "to_domain": "coda", "structural_property": "registers interrupts"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "code→technology"
        assert results[1].direction == "technology→code"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodeTechnologyTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "api__hardware_interface" in catalog
        assert "compiler_toolchain__build_systems" in catalog

    def test_catalog_excludes_rule(self):
        t = CodeTechnologyTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data

    def test_catalog_has_all_ten_names(self):
        t = CodeTechnologyTransformer()
        catalog = t.get_isomorphism_catalog()
        expected = [
            "api__hardware_interface",
            "embedded_code__firmware",
            "network_protocol__network_code",
            "database__query_language",
            "os_kernel__kernel_code",
            "cloud_infrastructure__iac",
            "cryptography__crypto_libraries",
            "ui_framework__frontend_code",
            "vcs__git_internals",
            "compiler_toolchain__build_systems",
        ]
        for name in expected:
            assert name in catalog, f"Missing isomorphism: {name}"


class TestFallback:
    """Test fallback behavior for unknown concepts."""

    def test_fallback_isomorphism_for_obscure_concept(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="zzz quark nebula xyz",
            origin_domain="coda",
            destination_domain="technologia",
            structural_property="vagueness",
        )
        assert result.isomorphisms[0] == "generic_homomorphism__code_technology"
        assert result.total_confidence >= 0.3

    def test_fallback_still_provides_six_steps(self):
        t = CodeTechnologyTransformer()
        result = t.transform(
            origin_concept="zzz quark nebula xyz",
            origin_domain="technologia",
            destination_domain="coda",
            structural_property="vagueness",
        )
        assert len(result.steps) == 6
        assert result.direction == "technology→code"


class TestDirectionEnum:
    """Test Direction enum values."""

    def test_direction_values(self):
        assert Direction.CODE_TO_TECHNOLOGY.value == "code→technology"
        assert Direction.TECHNOLOGY_TO_CODE.value == "technology→code"


class TestIsomorphismStructure:
    """Test that all isomorphism entries have required keys."""

    def test_all_entries_have_required_keys(self):
        for name, data in CodeTechnologyTransformer.ISOMORPHISMS.items():
            assert "technology" in data, f"{name} missing 'technology' key"
            assert "code" in data, f"{name} missing 'code' key"
            assert "rule" in data, f"{name} missing 'rule' key"
            assert "confidence" in data, f"{name} missing 'confidence' key"


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])