"""
Tests for the Nature ↔ Math Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nature_math_transformer import (
    NatureMathTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_fibonacci_plants_recursive_sequence(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Fibonacci spirals in sunflower",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="recursive growth approaching golden ratio",
        )
        assert result.direction == "nature→math"
        assert "fibonacci" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_crystal_lattice_group_theory(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Crystal lattice symmetry",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="discrete symmetry group of atomic arrangement",
        )
        assert "crystal" in result.isomorphisms[0].lower() or "group" in result.isomorphisms[0].lower()
        assert "group" in result.destination_concept.lower()

    def test_planetary_orbit_conic_section(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Planetary orbit",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="inverse-square gravitational attraction conic trajectory",
        )
        assert "orbit" in result.isomorphisms[0].lower() or "conic" in result.isomorphisms[0].lower()
        assert "conic" in result.destination_concept.lower() or "kepler" in result.destination_concept.lower()

    def test_dna_helix_knot_theory(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="DNA double helix",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="linking number topology supercoiling",
        )
        assert "dna" in result.isomorphisms[0].lower() or "knot" in result.isomorphisms[0].lower()
        assert "knot" in result.destination_concept.lower() or "linking" in result.destination_concept.lower()

    def test_fractal_coastline_fractal_geometry(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Fractal coastline",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="self-similar scale-dependent roughness fractal dimension",
        )
        assert "fractal" in result.isomorphisms[0].lower()
        assert "hausdorff" in result.destination_concept.lower() or "fractal" in result.destination_concept.lower()

    def test_butterfly_wings_strange_attractor(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Butterfly wing pattern",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="reaction-diffusion chaos strange attractor",
        )
        assert "butterfly" in result.isomorphisms[0].lower() or "attractor" in result.isomorphisms[0].lower()

    def test_spider_web_minimal_surface(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Spider web geometry",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="minimal thread length optimization network",
        )
        assert "spider" in result.isomorphisms[0].lower() or "minimal" in result.isomorphisms[0].lower()

    def test_neural_network_graph_theory(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Biological neural network",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="weighted directed graph connectivity laplacian",
        )
        assert "neural" in result.isomorphisms[0].lower() or "graph" in result.isomorphisms[0].lower()

    def test_quantum_spin_group_representation(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Quantum spin",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="irreducible representation eigenvalue spectrum",
        )
        assert "spin" in result.isomorphisms[0].lower() or "quantum" in result.isomorphisms[0].lower()
        assert "representation" in result.destination_concept.lower() or "su(2)" in result.destination_concept.lower()

    def test_population_dynamics_lotka_volterra(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Predator-prey population dynamics",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="coupled differential equations periodic oscillation",
        )
        assert "population" in result.isomorphisms[0].lower() or "lotka" in result.isomorphisms[0].lower()
        assert "lotka" in result.destination_concept.lower() or "differential" in result.destination_concept.lower()


class TestMathToNature:
    """Test math→nature direction."""

    def test_math_to_nature_group_theory(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Crystal lattice symmetry group",
            origin_domain="Mathematics",
            destination_domain="Nature",
            structural_property="discrete subgroup of Euclidean space group",
        )
        assert result.direction == "math→nature"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3

    def test_math_to_nature_conic_section(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Conic section",
            origin_domain="Mathematics",
            destination_domain="Nature",
            structural_property="inverse-square law trajectory ellipse eccentricity",
        )
        assert result.direction == "math→nature"
        assert "orbit" in result.destination_concept.lower() or "planetary" in result.destination_concept.lower() or "gravitational" in result.destination_concept.lower()


class TestPipelineStructure:
    """Test the 6-stage pipeline."""

    def test_six_stages_present(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Fibonacci sequence in plants",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="recursive growth golden ratio",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="DNA helix",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="topology linking number",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Something obscure and entirely unrelated",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Quantum spin",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="irreducible representation eigenvalue spectrum",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        t = NatureMathTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict round-trip."""

    def test_to_dict_round_trip(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Crystal lattice",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="discrete symmetry group",
        )
        d = result.to_dict()
        assert d["direction"] == "nature→math"
        assert d["origin_domain"] == "Nature"
        assert d["destination_domain"] == "Mathematics"
        assert len(d["steps"]) == 6
        assert all("language_thread" in s for s in d["steps"])
        assert "total_confidence" in d
        assert "isomorphisms" in d


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = NatureMathTransformer()
        moves = [
            {"from_concept": "Fibonacci spirals in plants", "from_domain": "Nature",
             "to_domain": "Mathematics", "structural_property": "recursive golden ratio"},
            {"from_concept": "Conic section", "from_domain": "Mathematics",
             "to_domain": "Nature", "structural_property": "inverse-square orbit eccentricity"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "nature→math"
        assert results[1].direction == "math→nature"


class TestFallbackIsomorphism:
    """Test fallback when no good match is found."""

    def test_fallback_isomorphism(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="zzz qqq xxx yyy",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="zzz",
        )
        assert result.isomorphisms  # non-empty — fallback was used
        assert "generic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = NatureMathTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "fibonacci_plants__recursive_sequence" in catalog
        assert "quantum_spin__group_representation" in catalog

    def test_catalog_excludes_rule(self):
        t = NatureMathTransformer()
        catalog = t.get_isomorphism_catalog()
        for entry in catalog.values():
            assert "rule" not in entry
            assert "nature" in entry
            assert "math" in entry
            assert "confidence" in entry


class TestResonance:
    """Test resonance sentence generation."""

    def test_resonance_sentence_generated(self):
        t = NatureMathTransformer()
        result = t.transform(
            origin_concept="Fractal coastline",
            origin_domain="Nature",
            destination_domain="Mathematics",
            structural_property="self-similar fractal dimension",
        )
        assert result.resonance_sentence
        assert len(result.resonance_sentence) > 20


class TestSingleton:
    """Test transformer singleton."""

    def test_singleton_returns_same_instance(self):
        t1 = get_transformer()
        t2 = get_transformer()
        assert t1 is t2


class TestDirectionEnum:
    """Test the Direction enum values."""

    def test_direction_values(self):
        assert Direction.NATURE_TO_MATH.value == "nature→math"
        assert Direction.MATH_TO_NATURE.value == "math→nature"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])