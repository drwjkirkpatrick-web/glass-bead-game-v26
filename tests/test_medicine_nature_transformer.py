"""
Tests for the Medicine ↔ Nature Transformer module.
"""
import pytest
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from medicine_nature_transformer import (
    MedicineNatureTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_immune_system_ecological_balance(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Immune system",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="self non-self recognition clonal selection equilibrium",
        )
        assert result.direction == "medicine→nature"
        assert "immune" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_neural_pathways_mycelial_networks(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Neural pathways",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="neurons synapses Hebbian strengthening adaptive network",
        )
        assert "neural" in result.isomorphisms[0].lower()
        assert "mycel" in result.destination_concept.lower() or "fungal" in result.destination_concept.lower()

    def test_circulatory_river_branching(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Circulatory system",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="branching from large to small vessels fractal",
        )
        assert "circulatory" in result.isomorphisms[0].lower() or "river" in result.isomorphisms[0].lower()

    def test_pharmacognosy_plant_chemistry(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Pharmacognosy",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="bioactive plant compounds alkaloids glycosides",
        )
        assert "pharmacog" in result.isomorphisms[0].lower() or "plant" in result.isomorphisms[0].lower()

    def test_homeostasis_ecosystem_equilibrium(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Homeostasis",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="negative feedback loops maintaining equilibrium",
        )
        assert "homeostasis" in result.isomorphisms[0].lower()

    def test_bone_crystallography(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Bone structure",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="hydroxyapatite crystalline lattice collagen scaffold",
        )
        assert "bone" in result.isomorphisms[0].lower()

    def test_circadian_seasonal(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Circadian rhythm",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="clock genes entrained by light photoperiod",
        )
        assert "circadian" in result.isomorphisms[0].lower()

    def test_viral_replication_fractals(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Viral replication",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="self-replicating recursive exponential proliferation",
        )
        assert "viral" in result.isomorphisms[0].lower() or "fractal" in result.isomorphisms[0].lower()

    def test_dna_repair_error_correction(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="DNA repair",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="mismatch repair redundancy genetic code degenerate",
        )
        assert "dna" in result.isomorphisms[0].lower() or "error" in result.isomorphisms[0].lower()

    def test_stem_cells_regenerative_growth(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Stem cells",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="undifferentiated self-renewing differentiation niche",
        )
        assert "stem" in result.isomorphisms[0].lower()


class TestBidirectionalTransformations:
    """Test nature→medicine direction."""

    def test_nature_to_medicine_ecosystem(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Ecosystem balance",
            origin_domain="Nature",
            destination_domain="Medicine",
            structural_property="predator prey dynamics equilibrium disturbance",
        )
        assert result.direction == "nature→medicine"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_nature_to_medicine_mycelium(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Mycelial network",
            origin_domain="Nature",
            destination_domain="Medicine",
            structural_property="branching nutrient routing adaptive reinforcement",
        )
        assert result.direction == "nature→medicine"
        assert "neural" in result.destination_concept.lower() or "mycel" in result.destination_concept.lower()

    def test_round_trip_fidelity(self):
        """medicine→nature round-trip should produce nature-flavored destination."""
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Immune system",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="self non-self recognition equilibrium",
        )
        assert any(word in result.destination_concept.lower() for word in
                    ["ecolog", "ecosystem", "balance", "population", "predator"])


class TestPipelineStructure:
    """Test the 6-stage pipeline structure."""

    def test_six_stages_in_order(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Neural pathways",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="adaptive network",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Circadian rhythm",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="oscillator entrained by light",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10

    def test_resonance_sentence_generated(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Stem cells",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="regeneration",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Something obscure and unrelated",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Circadian rhythm",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="clock genes entrained by light photoperiod",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        for name, data in MedicineNatureTransformer.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict / from_dict round-trip."""

    def test_to_dict_from_dict_roundtrip(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="Neural pathways",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="adaptive network",
        )
        d = result.to_dict()
        assert d["direction"] == "medicine→nature"
        restored = TransformerResult.from_dict(d)
        assert restored.direction == result.direction
        assert restored.origin_concept == result.origin_concept
        assert restored.destination_concept == result.destination_concept
        assert len(restored.steps) == 6
        assert restored.steps[0].stage == "PARSE"


class TestTokenLogging:
    """Test token visualization support."""

    def test_tokens_are_logged(self):
        t = MedicineNatureTransformer()
        test_tokens = ["[PARSE]", "decompose", "cell", "[TAG]", "label", "neural"]
        result = t.transform(
            origin_concept="Neural pathways",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="synapses",
            tokens=test_tokens,
        )
        assert len(result.tokens_seen) > 0
        assert "PARSE" in str(result.tokens_seen)

    def test_tokens_per_step(self):
        t = MedicineNatureTransformer()
        test_tokens = [f"t{i}" for i in range(18)]
        result = t.transform(
            origin_concept="Immune system",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="self non-self recognition",
            tokens=test_tokens,
        )
        assert "PARSE" in result.tokens_per_step
        assert "VERIFY" in result.tokens_per_step


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = MedicineNatureTransformer()
        moves = [
            {"from_concept": "Immune system", "from_domain": "Medicine", "to_domain": "Nature", "structural_property": "equilibrium"},
            {"from_concept": "Ecosystem", "from_domain": "Nature", "to_domain": "Medicine", "structural_property": "balance"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "medicine→nature"
        assert results[1].direction == "nature→medicine"


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = MedicineNatureTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "immune_system__ecological_balance" in catalog
        assert "stem_cells__regenerative_growth_plants" in catalog

    def test_catalog_excludes_rule(self):
        t = MedicineNatureTransformer()
        catalog = t.get_isomorphism_catalog()
        for name, data in catalog.items():
            assert "rule" not in data


class TestFallback:
    """Test fallback behavior for unknown concepts."""

    def test_fallback_isomorphism_for_obscure_concept(self):
        t = MedicineNatureTransformer()
        result = t.transform(
            origin_concept="zzz unknown xyz concept",
            origin_domain="Medicine",
            destination_domain="Nature",
            structural_property="vagueness",
        )
        assert result.isomorphisms[0] == "generic_homomorphism__natural_form"
        assert result.total_confidence >= 0.3


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])