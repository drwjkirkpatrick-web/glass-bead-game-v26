"""
Tests for the Code ↔ Nature Transformer module.
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from code_nature_transformer import (
    CodeNatureTransformer, TransformerResult, TransformationStep,
    Direction, get_transformer
)


class TestCoreIsomorphisms:
    """Test the 10 core isomorphisms from the library."""

    def test_genetic_algorithm_natural_selection(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Genetic algorithm with fitness-proportionate selection",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="selection crossover mutation fitness landscape",
        )
        assert result.direction == "code→nature"
        assert "genetic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99
        assert len(result.steps) == 6
        assert result.steps[0].stage == "PARSE"
        assert result.steps[-1].stage == "VERIFY"

    def test_neural_network_biological_brain(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Neural network with backpropagation",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="weights activation function learning synaptic",
        )
        assert "neural" in result.isomorphisms[0].lower()
        assert "brain" in result.destination_concept.lower() or "biological" in result.destination_concept.lower()

    def test_cellular_automaton_biological_growth(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Cellular automaton with local transition rules",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="grid cells neighborhood emergent pattern morphogenesis",
        )
        assert "cellular" in result.isomorphisms[0].lower() or "automaton" in result.isomorphisms[0].lower()
        assert "growth" in result.destination_concept.lower() or "life" in result.destination_concept.lower()

    def test_fractal_natural_patterns(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Fractal generation code with recursive subdivision",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="self-similar recursive coastline fractal dimension",
        )
        assert "fractal" in result.isomorphisms[0].lower()
        assert "coastline" in result.destination_concept.lower() or "pattern" in result.destination_concept.lower() or "fractal" in result.destination_concept.lower()

    def test_swarm_algorithm_flocking(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Swarm optimization with local agent rules",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="flocking schooling separation alignment cohesion",
        )
        assert "swarm" in result.isomorphisms[0].lower() or "flocking" in result.isomorphisms[0].lower()

    def test_ecological_model_ecosystem_sim(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Ecological simulation with trophic interactions",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="ecosystem food web nutrient cycling biodiversity",
        )
        assert "ecological" in result.isomorphisms[0].lower() or "ecosystem" in result.isomorphisms[0].lower()

    def test_molecular_dynamics_protein_folding(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Molecular dynamics simulation with force field",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="force field energy minimization protein folding conformational",
        )
        assert "molecular" in result.isomorphisms[0].lower() or "protein" in result.isomorphisms[0].lower()

    def test_perlin_noise_natural_texture(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Perlin noise generator with octaves and persistence",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="gradient noise texture cloud terrain organic",
        )
        assert "perlin" in result.isomorphisms[0].lower() or "noise" in result.isomorphisms[0].lower() or "texture" in result.isomorphisms[0].lower()

    def test_phylogenetic_tree_class_hierarchy(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Phylogenetic tree algorithm with branching divergence",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="class hierarchy inheritance common ancestor cladistics",
        )
        assert "phylogenetic" in result.isomorphisms[0].lower() or "class" in result.isomorphisms[0].lower()

    def test_homeostasis_feedback_control(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Feedback control loop with PID controller",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="homeostasis set point sensor actuator negative feedback",
        )
        assert "homeostasis" in result.isomorphisms[0].lower() or "feedback" in result.isomorphisms[0].lower()


class TestNatureToCode:
    """Test nature→code direction."""

    def test_nature_to_code_genetic(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Natural selection and evolution",
            origin_domain="natura",
            destination_domain="coda",
            structural_property="fitness selection heritable variation reproduction",
        )
        assert result.direction == "nature→code"
        assert len(result.steps) == 6
        assert result.total_confidence >= 0.3
        assert "genetic" in result.destination_concept.lower() or "algorithm" in result.destination_concept.lower()

    def test_nature_to_code_neural(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Biological brain neural network",
            origin_domain="natura",
            destination_domain="coda",
            structural_property="neurons synapses weights activation plasticity",
        )
        assert result.direction == "nature→code"
        assert "neural" in result.destination_concept.lower() or "network" in result.destination_concept.lower()

    def test_nature_to_code_flocking(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Bird flocking and schooling behavior",
            origin_domain="natura",
            destination_domain="coda",
            structural_property="local interaction rules separation alignment cohesion emergent",
        )
        assert result.direction == "nature→code"
        assert "swarm" in result.destination_concept.lower() or "optimization" in result.destination_concept.lower() or "flocking" in result.destination_concept.lower()

    def test_nature_to_code_homeostasis(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Biological homeostasis and self-regulation",
            origin_domain="nature",
            destination_domain="coda",
            structural_property="set point feedback negative control stability",
        )
        assert result.direction == "nature→code"
        assert "feedback" in result.destination_concept.lower() or "control" in result.destination_concept.lower()


class TestPipelineStructure:
    """Test the 6-stage pipeline."""

    def test_six_stages_present(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Genetic algorithm",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="selection fitness crossover mutation",
        )
        stages = [s.stage for s in result.steps]
        assert stages == ["PARSE", "TAG", "MAP", "PROJECT", "COMPOSE", "VERIFY"]

    def test_each_step_has_language_thread(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Neural network",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="weights activation learning",
        )
        for step in result.steps:
            assert step.language_thread
            assert len(step.language_thread) > 10


class TestConfidenceBounds:
    """Test confidence stays within bounds."""

    def test_confidence_never_below_floor(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Something obscure and entirely unrelated",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="vagueness",
        )
        assert result.total_confidence >= 0.3
        assert result.total_confidence <= 0.99

    def test_confidence_high_for_known_isomorphisms(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Genetic algorithm",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="fitness selection crossover mutation population",
        )
        assert result.total_confidence >= 0.85

    def test_all_isomorphism_confidences_in_range(self):
        t = CodeNatureTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert 0.85 <= data["confidence"] <= 0.99, f"{name} confidence out of range"


class TestSerialization:
    """Test to_dict round-trip."""

    def test_to_dict_round_trip(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Fractal generation code",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="recursive self-similar dimension",
        )
        d = result.to_dict()
        assert d["direction"] == "code→nature"
        assert d["origin_domain"] == "coda"
        assert d["destination_domain"] == "natura"
        assert len(d["steps"]) == 6
        assert all("language_thread" in s for s in d["steps"])
        assert "total_confidence" in d
        assert "isomorphisms" in d


class TestBatchTransform:
    """Test batch processing."""

    def test_batch_transform(self):
        t = CodeNatureTransformer()
        moves = [
            {"from_concept": "Genetic algorithm", "from_domain": "coda",
             "to_domain": "natura", "structural_property": "fitness selection mutation"},
            {"from_concept": "Natural selection evolution", "from_domain": "natura",
             "to_domain": "coda", "structural_property": "selection fitness heritable variation"},
        ]
        results = t.batch_transform(moves)
        assert len(results) == 2
        assert results[0].direction == "code→nature"
        assert results[1].direction == "nature→code"


class TestFallbackIsomorphism:
    """Test fallback when no good match is found."""

    def test_fallback_isomorphism(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="zzz qqq xxx yyy",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="zzz",
        )
        assert result.isomorphisms  # non-empty — fallback was used
        assert "generic" in result.isomorphisms[0].lower()
        assert result.total_confidence >= 0.3


class TestIsomorphismCatalog:
    """Test catalog browsing."""

    def test_catalog_has_all_isomorphisms(self):
        t = CodeNatureTransformer()
        catalog = t.get_isomorphism_catalog()
        assert len(catalog) == 10
        assert "genetic_algorithm__natural_selection" in catalog
        assert "homeostasis__feedback_control" in catalog

    def test_catalog_excludes_rule(self):
        t = CodeNatureTransformer()
        catalog = t.get_isomorphism_catalog()
        for entry in catalog.values():
            assert "rule" not in entry
            assert "nature" in entry
            assert "code" in entry
            assert "confidence" in entry


class TestResonance:
    """Test resonance sentence generation."""

    def test_resonance_sentence_generated(self):
        t = CodeNatureTransformer()
        result = t.transform(
            origin_concept="Fractal generation code",
            origin_domain="coda",
            destination_domain="natura",
            structural_property="self-similar recursive dimension",
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
        assert Direction.CODE_TO_NATURE.value == "code→nature"
        assert Direction.NATURE_TO_CODE.value == "nature→code"


class TestIsomorphismCount:
    """Test that exactly 10 isomorphisms are defined."""

    def test_ten_isomorphisms(self):
        t = CodeNatureTransformer()
        assert len(t.ISOMORPHISMS) == 10

    def test_all_isomorphisms_have_required_keys(self):
        t = CodeNatureTransformer()
        for name, data in t.ISOMORPHISMS.items():
            assert "nature" in data, f"{name} missing 'nature' key"
            assert "code" in data, f"{name} missing 'code' key"
            assert "rule" in data, f"{name} missing 'rule' key"
            assert "confidence" in data, f"{name} missing 'confidence' key"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])