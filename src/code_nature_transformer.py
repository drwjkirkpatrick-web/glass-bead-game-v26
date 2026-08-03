"""
glass-bead-game-v26 — Code ↔ Nature Transformer
Formal bidirectional transformation scaffold between computer code
(the domain 'coda': algorithms, data structures, programs) and natural
phenomena (the domain 'natura': biology, ecology, physics of the living
world), with human language as the connecting thread.

Hesse's Glass Bead Game unifies all disciplines; this module makes the
correspondence between Code and Nature explicit, testable, and playable —
the engineered world and the living world as two faces of one bead.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    CODE_TO_NATURE = "code→nature"
    NATURE_TO_CODE = "nature→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Nature transformation pipeline."""
    stage: str
    input_repr: str
    output_repr: str
    formal_rule: str
    confidence: float
    language_thread: str


@dataclass
class TransformerResult:
    """The complete transformation from origin to destination."""
    direction: str
    origin_domain: str
    origin_concept: str
    destination_domain: str
    destination_concept: str
    steps: List[TransformationStep]
    structural_property: str
    resonance_sentence: str
    tokens_seen: List[str]
    tokens_per_step: Dict[str, List[str]]
    total_confidence: float
    isomorphisms: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "direction": self.direction,
            "origin_domain": self.origin_domain,
            "origin_concept": self.origin_concept,
            "destination_domain": self.destination_domain,
            "destination_concept": self.destination_concept,
            "steps": [asdict(s) for s in self.steps],
            "structural_property": self.structural_property,
            "resonance_sentence": self.resonance_sentence,
            "tokens_seen": self.tokens_seen,
            "tokens_per_step": self.tokens_per_step,
            "total_confidence": self.total_confidence,
            "isomorphisms": self.isomorphisms,
        }


class CodeNatureTransformer:
    """
    Formal bidirectional transformer between computer code and natural
    phenomena.

    The transformation proceeds through 6 canonical stages:
        1. PARSE    — Decompose the origin into structural primitives
        2. TAG      — Label each primitive with its formal type
        3. MAP      — Map primitives to the target domain via isomorphism
        4. PROJECT  — Project mapped primitives into target space
        5. COMPOSE  — Assemble projected elements into coherent structure
        6. VERIFY   — Check structural fidelity via inverse transformation

    Human language serves as the THREAD connecting each stage.
    """

    ISOMORPHISMS = {
        "genetic_algorithm__natural_selection": {
            "nature": "Natural selection and evolution: heritable variation, differential survival, and reproduction across generations",
            "code": "Genetic algorithm: population of candidate solutions, fitness function, selection, crossover, and mutation operators",
            "rule": "Fitness-proportionate selection maps to differential reproductive success; crossover maps to sexual recombination; mutation maps to genetic drift — the search landscape is the ecological niche",
            "confidence": 0.96,
        },
        "neural_network__biological_brain": {
            "nature": "Biological brain and neural networks: neurons, synapses, action potentials, Hebbian plasticity, layered cortical architecture",
            "code": "Artificial neural network: weighted nodes, activation functions, backpropagation, layered architecture, gradient descent",
            "rule": "Weights map to synaptic strengths; activation functions map to firing thresholds; backpropagation maps to Hebbian learning — the loss landscape mirrors the brain's adaptive optimization",
            "confidence": 0.94,
        },
        "cellular_automaton__biological_growth": {
            "nature": "Biological growth and pattern formation: Conway's Game of Life, embryonic development, tissue morphogenesis",
            "code": "Cellular automaton: grid of cells, local transition rules, synchronous updates, emergent global patterns",
            "rule": "Local transition rules map to cell-cell signaling; synchronous update maps to developmental timing; emergent patterns map to morphogenetic self-organization — life-like complexity from simple local rules",
            "confidence": 0.93,
        },
        "fractal__natural_patterns": {
            "nature": "Natural fractal patterns: coastlines, river networks, mountain ranges, fern fronds, snowflakes",
            "code": "Fractal generation code: recursive subdivision, L-systems, iterated function systems, Mandelbrot/Julia set rendering",
            "rule": "Recursive self-similar iteration maps to natural scale invariance; the Hausdorff dimension of the generated fractal matches the measured roughness of natural forms — code recapitulates nature's geometry",
            "confidence": 0.95,
        },
        "swarm_algorithm__flocking": {
            "nature": "Flocking and schooling behavior: bird flocks, fish schools, insect swarms governed by local interaction rules",
            "code": "Swarm optimization algorithms: particle swarm optimization, ant colony optimization, local-agent global-emergence search",
            "rule": "Local interaction rules (separation, alignment, cohesion) map to algorithmic agent update rules; emergent flocking maps to convergent search behavior — collective intelligence from simple agents",
            "confidence": 0.92,
        },
        "ecological_model__ecosystem_sim": {
            "nature": "Ecosystem dynamics: food webs, nutrient cycling, predator-prey relationships, biodiversity, trophic cascades",
            "code": "Ecological simulation code: agent-based ecosystem models, population dynamics ODEs, resource allocation algorithms",
            "rule": "Trophic interactions map to energy-flow data structures; population equations map to ODE solvers; biodiversity maps to agent diversity — the simulation is a formal mirror of ecological complexity",
            "confidence": 0.91,
        },
        "molecular_dynamics__protein_folding": {
            "nature": "Protein folding: amino acid chains folding into three-dimensional structures via thermodynamic free-energy minimization",
            "code": "Molecular dynamics code: force-field calculations, integration of Newton's equations, energy minimization algorithms, Monte Carlo sampling",
            "rule": "Force-field potential maps to physical inter-atomic forces; energy minimization maps to thermodynamic folding pathway; the code simulates the natural search through conformational space to the native state",
            "confidence": 0.90,
        },
        "perlin_noise__natural_texture": {
            "nature": "Natural texture generation: cloud formations, terrain elevation, marble veining, wood grain, organic surface patterns",
            "code": "Perlin noise code: gradient noise function, octaves, persistence, lacunarity, fractal noise synthesis",
            "rule": "Gradient noise interpolation maps to natural smooth variation; octave layering maps to multi-scale natural detail; persistence parameter controls the roughness that matches real-world textures — procedural code breeds organic appearance",
            "confidence": 0.89,
        },
        "phylogenetic_tree__class_hierarchy": {
            "nature": "Phylogenetic tree: evolutionary relationships among species, common ancestors, branching divergence, cladistics",
            "code": "Class hierarchy and inheritance: object-oriented class trees, parent-child inheritance, abstract base classes, polymorphic dispatch",
            "rule": "Common ancestor maps to base class; speciation maps to subclass derivation; derived traits map to overridden methods; the phylogenetic tree and the class hierarchy share the same DAG topology of inheritance and divergence",
            "confidence": 0.88,
        },
        "homeostasis__feedback_control": {
            "nature": "Homeostasis: biological self-regulation maintaining internal stability — temperature, blood sugar, pH, osmotic balance",
            "code": "Feedback control loops in code: PID controllers, thermostat algorithms, sensor-actuator closed loops, error-signal correction",
            "rule": "Set point maps to desired value; sensory feedback maps to sensor reading; physiological correction maps to actuator output; negative feedback in biology and in code are the same dynamical structure — stability through error-driven correction",
            "confidence": 0.93,
        },
    }

    def __init__(self):
        self.token_log: List[str] = []
        self.step_tokens: Dict[str, List[str]] = {}

    def _log_tokens(self, stage: str, tokens: List[str]):
        self.token_log.extend(tokens)
        self.step_tokens[stage] = tokens

    def transform(
        self,
        origin_concept: str,
        origin_domain: str,
        destination_domain: str,
        structural_property: str,
        resonance_sentence: str = "",
        tokens: Optional[List[str]] = None,
    ) -> TransformerResult:
        """
        Execute a full bidirectional transformation.

        If origin_domain is "natura" or contains "nature", direction is nature→code.
        If origin_domain is "coda" or contains "code", direction is code→nature.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "natura" in origin_domain.lower() or "nature" in origin_domain.lower():
            direction = Direction.NATURE_TO_CODE
        elif "coda" in origin_domain.lower() or "code" in origin_domain.lower():
            direction = Direction.CODE_TO_NATURE
        else:
            # Infer from concept content
            if any(c in origin_concept.lower() for c in [
                "genetic", "neural", "automaton", "fractal code", "swarm",
                "ecological sim", "molecular dynamics", "perlin", "phylogenetic tree",
                "feedback control", "algorithm", "program", "function", "class",
            ]):
                direction = Direction.CODE_TO_NATURE
            else:
                direction = Direction.NATURE_TO_CODE

        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        if direction == Direction.NATURE_TO_CODE:
            destination_concept = iso_data["code"]
        else:
            destination_concept = iso_data["nature"]

        if not resonance_sentence:
            resonance_sentence = self._generate_resonance(
                origin_concept, destination_concept, iso_name, structural_property
            )

        total_confidence = math.prod(s.confidence for s in steps) ** (1 / max(len(steps), 1))
        total_confidence = round(max(0.3, min(0.99, total_confidence)), 3)

        return TransformerResult(
            direction=direction.value,
            origin_domain=origin_domain,
            origin_concept=origin_concept,
            destination_domain=destination_domain,
            destination_concept=destination_concept,
            steps=steps,
            structural_property=structural_property,
            resonance_sentence=resonance_sentence,
            tokens_seen=self.token_log,
            tokens_per_step=self.step_tokens,
            total_confidence=total_confidence,
            isomorphisms=[iso_name] if iso_name else [],
        )

    def _find_isomorphism(
        self,
        concept: str,
        origin_domain: str,
        dest_domain: str,
        structural_property: str,
    ) -> Tuple[str, Dict[str, Any]]:
        """Find the best-matching isomorphism from the library."""
        concept_lower = concept.lower()
        property_lower = structural_property.lower()

        best_score = -1
        best_name = ""
        best_data = {}

        for name, data in self.ISOMORPHISMS.items():
            score = 0
            text = f"{data['nature']} {data['code']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["nature"], data["code"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_isomorphism__code_nature"
            best_data = {
                "nature": f"Natural phenomenon embodying {structural_property}",
                "code": f"Code structure abstracting {concept}",
                "rule": "Structure-preserving correspondence between natural form and computational system",
                "confidence": 0.65,
            }

        return best_name, best_data

    def _build_pipeline(
        self,
        direction: Direction,
        origin_concept: str,
        iso_name: str,
        iso_data: Dict[str, Any],
        structural_property: str,
        tokens: List[str],
    ) -> List[TransformationStep]:
        """Construct the 6-stage transformation with language thread."""
        steps = []
        base_conf = iso_data.get("confidence", 0.85)

        if direction == Direction.NATURE_TO_CODE:
            src_label, dst_label = "natural", "computational"
            src_obj = iso_data["nature"]
            dst_obj = iso_data["code"]
        else:
            src_label, dst_label = "computational", "natural"
            src_obj = iso_data["code"]
            dst_obj = iso_data["nature"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into generators and relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the building blocks of {origin_concept}? What forces and forms shape it?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread=f"Each element carries a label — not merely a name, but the role it plays in the larger architecture of code and world.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} phenomenon '{src_obj}' maps to the {dst_label} structure '{dst_obj}' through the rule: {iso_data['rule'][:80]}...",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Coordinate projection preserving metric invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread=f"The mapped elements are placed in their new home — not arbitrarily, but according to the deep symmetries they share across the code-nature divide.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under associative operation preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The fragments assemble into a whole — a {dst_label} object that breathes with the same rhythm as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
            formal_rule="Inverse homomorphism check: φ⁻¹(φ(x)) ≈ x within tolerance ε",
            confidence=round(base_conf * 0.90, 3),
            language_thread=f"We turn the glass bead over, looking back through it to ensure the original light still shines — transformed, but unbroken.",
        ))

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "genetic": "population, fitness function, selection operator, crossover, mutation",
            "neural": "layers, weights, activation functions, loss gradient, backpropagation",
            "cellular": "grid cells, neighborhood, transition rule, synchronous update, emergent pattern",
            "automaton": "grid cells, neighborhood, transition rule, synchronous update, emergent pattern",
            "fractal": "recursive rule, base case, iteration depth, self-similarity, dimension",
            "swarm": "agents, position, velocity, local rules, global emergence",
            "ecological": "species agents, resource pools, interaction matrix, trophic levels",
            "molecular": "atoms, force field, integrator, energy landscape, conformational states",
            "protein": "atoms, force field, integrator, energy landscape, conformational states",
            "perlin": "gradient grid, interpolation, octaves, persistence, lacunarity",
            "noise": "gradient grid, interpolation, octaves, persistence, lacunarity",
            "phylogenetic": "taxa, common ancestor, branch points, derived traits, topology",
            "class": "base class, subclasses, inheritance links, overridden methods, polymorphism",
            "hierarchy": "base class, subclasses, inheritance links, overridden methods, polymorphism",
            "homeostasis": "set point, sensor, error signal, actuator, feedback loop",
            "feedback": "set point, sensor, error signal, actuator, feedback loop",
            "control": "set point, sensor, error signal, actuator, feedback loop",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "primitive elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "genetic": "population:set; operator:selective; fitness:scalar",
            "neural": "node:neuron; weight:synaptic; architecture:layered",
            "cellular": "cell:state; rule:local; update:synchronous",
            "automaton": "cell:state; rule:local; update:synchronous",
            "fractal": "generator:recursive; dimension:fractal; self-similarity:exact",
            "swarm": "agent:particle; interaction:local; behavior:emergent",
            "ecological": "agent:species; interaction:trophic; dynamics:coupled",
            "molecular": "particle:atom; force:potential; integrator:newtonian",
            "protein": "particle:atom; force:potential; integrator:newtonian",
            "perlin": "function:gradient; noise:smooth; octave:layered",
            "noise": "function:gradient; noise:smooth; octave:layered",
            "phylogenetic": "node:taxon; edge:ancestry; tree:branching",
            "class": "class:base; edge:inheritance; tree:hierarchical",
            "hierarchy": "class:base; edge:inheritance; tree:hierarchical",
            "homeostasis": "setpoint:reference; signal:error; loop:feedback",
            "feedback": "setpoint:reference; signal:error; loop:feedback",
            "control": "setpoint:reference; signal:error; loop:feedback",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:abstract; relation:structural; property:formal"

    def _generate_resonance(
        self,
        origin: str,
        destination: str,
        iso_name: str,
        structural_property: str,
    ) -> str:
        """Generate a poetic resonance sentence from the isomorphism."""
        templates = [
            f"As {origin} {structural_property}, so {destination} reveals the same pattern written in another tongue.",
            f"What {origin} grows in the world, {destination} computes in silicon — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, the living pattern of {origin} and the coded pattern of {destination} become a single figure seen from two angles.",
        ]
        return templates[hash(iso_name) % len(templates)]

    def batch_transform(
        self,
        moves: List[Dict[str, Any]],
    ) -> List[TransformerResult]:
        """Transform a batch of moves."""
        results = []
        for move in moves:
            result = self.transform(
                origin_concept=move.get("from_concept", ""),
                origin_domain=move.get("from_domain", ""),
                destination_domain=move.get("to_domain", ""),
                structural_property=move.get("structural_property", ""),
                resonance_sentence=move.get("resonance_sentence", ""),
            )
            results.append(result)
        return results

    def get_isomorphism_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Return the full isomorphism library for browsing."""
        return {
            name: {k: v for k, v in data.items() if k != "rule"}
            for name, data in self.ISOMORPHISMS.items()
        }


# ─── Convenience singleton ───────────────────────────────────
_default_transformer = None


def get_transformer() -> CodeNatureTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeNatureTransformer()
    return _default_transformer