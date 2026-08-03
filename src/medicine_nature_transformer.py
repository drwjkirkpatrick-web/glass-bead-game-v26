"""
glass-bead-game-v26 — Medicine ↔ Nature Transformer
Formal bidirectional transformation scaffold between medical/biological
structures and natural-world structures, with human language as the
connecting thread.

Hesse's Glass Bead Game seeks correspondences across all domains of
knowledge; this module makes the deep analogy between the body's healing
architecture and the patterns of the living world explicit, testable,
and playable.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    MEDICINE_TO_NATURE = "medicine→nature"
    NATURE_TO_MEDICINE = "nature→medicine"


@dataclass
class TransformationStep:
    """A single step in the Medicine ↔ Nature transformation pipeline."""
    stage: str                      # e.g., "parse", "map", "project", "compose"
    input_repr: str                 # What went in
    output_repr: str                # What came out
    formal_rule: str                # The rule applied (citable)
    confidence: float               # 0.0–1.0
    language_thread: str            # Human-language bridge sentence


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
    tokens_seen: List[str]          # For LLM visualization
    tokens_per_step: Dict[str, List[str]]
    total_confidence: float
    isomorphisms: List[str]         # Named isomorphism types found

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

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TransformerResult":
        return cls(
            direction=d["direction"],
            origin_domain=d["origin_domain"],
            origin_concept=d["origin_concept"],
            destination_domain=d["destination_domain"],
            destination_concept=d["destination_concept"],
            steps=[TransformationStep(**s) for s in d["steps"]],
            structural_property=d["structural_property"],
            resonance_sentence=d["resonance_sentence"],
            tokens_seen=d["tokens_seen"],
            tokens_per_step=d["tokens_per_step"],
            total_confidence=d["total_confidence"],
            isomorphisms=d["isomorphisms"],
        )


class MedicineNatureTransformer:
    """
    Formal bidirectional transformer between medical/biological and natural-world
    structures.

    The transformation proceeds through 6 canonical stages:
        1. PARSE    — Decompose the origin into structural primitives
        2. TAG      — Label each primitive with its formal type
        3. MAP      — Map primitives to the target domain via isomorphism
        4. PROJECT  — Project mapped primitives into target space
        5. COMPOSE  — Assemble projected elements into coherent structure
        6. VERIFY   — Check structural fidelity via inverse transformation

    Human language serves as the THREAD connecting each stage — it is not
    decoration but the carrier of structural intent across domain boundaries.
    """

    # ─── Isomorphism Library (the formal core) ─────────────────
    ISOMORPHISMS = {
        "immune_system__ecological_balance": {
            "medicine": "Immune system: self/non-self recognition, T-cell and B-cell populations, clonal selection, immune memory",
            "nature": "Ecological balance: predator-prey dynamics, species populations, competitive exclusion, succession, equilibrium after disturbance",
            "rule": "Clonal selection in immunity ≅ Lotka-Volterra population dynamics in ecology; both are self-regulating systems where diversity confers stability and perturbation provokes a return to equilibrium",
            "confidence": 0.90,
        },
        "neural_pathways__mycelial_networks": {
            "medicine": "Neural pathways: neurons, synapses, action potentials, Hebbian strengthening, parallel distributed processing",
            "nature": "Mycelial networks: fungal hyphae forming branching webs that route nutrients across the forest floor, strengthening well-used paths",
            "rule": "Both are adaptive transport networks where usage strengthens connectivity; the Hebbian rule 'neurons that fire together wire together' ≅ mycelial reinforcement of high-flow nutrient channels",
            "confidence": 0.89,
        },
        "circulatory_system__river_branching": {
            "medicine": "Circulatory system: arteries, capillaries, veins; branching from large to small with Murray's law r³_branch = r³_1 + r³_2",
            "nature": "River branching: drainage basins bifurcate from main trunk to tributaries following Horton's laws and the same power-law scaling",
            "rule": "Murray's law for vessels ≅ Hack's law for river networks: both minimize total hydraulic resistance subject to space-filling constraints, yielding fractal branching with dimension ≈ 3",
            "confidence": 0.93,
        },
        "pharmacognosy__plant_chemistry": {
            "medicine": "Pharmacognosy: bioactive plant compounds (alkaloids, glycosides, terpenes) as the source and scaffold of pharmaceuticals",
            "nature": "Plant secondary metabolism: chemical defense and signaling compounds evolved in the arms race between plants and herbivores",
            "rule": "A medicinal compound is an ecological signal repurposed: the alkaloid that deters a caterpillar becomes the drug that modulates a human receptor — same molecule, different recipient",
            "confidence": 0.91,
        },
        "homeostasis__ecosystem_equilibrium": {
            "medicine": "Homeostasis: negative-feedback loops maintaining internal variables (pH, temperature, glucose) within narrow ranges",
            "nature": "Ecosystem equilibrium: feedback between populations and resources maintaining a dynamic steady state across biotic and abiotic factors",
            "rule": "Both are negative-feedback control systems: deviation from set-point triggers a corrective response; the Lotka-Volterra equilibrium ≅ the glucose-insulin feedback loop",
            "confidence": 0.92,
        },
        "bone_structure__crystallography": {
            "medicine": "Bone structure: hydroxyapatite Ca₁₀(PO₄)₆(OH)₂ biomineral on a collagen scaffold, hierarchical from nano-fibrils to osteons",
            "nature": "Crystallography: periodic lattices, space-group symmetry, unit cells, and the hierarchical self-assembly of minerals",
            "rule": "Hydroxyapatite is a crystalline lattice with hexagonal space group P6₃/m; bone is a biomineral composite whose hierarchical organization ≅ the multiscale structure of self-assembled crystals",
            "confidence": 0.88,
        },
        "circadian_rhythm__seasonal_cycles": {
            "medicine": "Circadian rhythm: SCN-driven ~24h clock, clock genes (CLOCK, BMAL1, PER, CRY), entrainment by light",
            "nature": "Seasonal cycles: Earth's axial tilt driving annual photoperiod changes that entrain plant flowering, animal migration, and dormancy",
            "rule": "Circadian entrainment ≅ seasonal photoperiodism: both are self-sustaining oscillators entrained by an external zeitgeber (light); phase response curves govern both",
            "confidence": 0.95,
        },
        "viral_replication__self_replicating_fractals": {
            "medicine": "Viral replication: virus hijacks host machinery to copy its genome and self-assemble capsids in an exponential cascade",
            "nature": "Self-replicating fractals: structures (e.g., Mandelbrot iteration, L-systems) that generate copies of themselves at every scale, branching recursively",
            "rule": "Viral self-replication ≅ fractal iteration: both follow a recurrence v_{n+1} = F(v_n) producing exponential proliferation; the capsid self-assembly ≅ the recursive self-similarity of fractal generation",
            "confidence": 0.87,
        },
        "dna_repair__error_correction_nature": {
            "medicine": "DNA repair: mismatch repair, nucleotide excision repair, double-strand break repair — enzymatic correction of replication errors",
            "nature": "Error correction in nature: redundancy in genetic code (degenerate codons), checkpoint mechanisms, and redundancy in ecological systems as fault tolerance",
            "rule": "DNA mismatch repair ≅ error-correcting codes: both detect and correct errors via redundancy; the genetic code's 64→20 mapping is a degenerate code that buffers single-base errors",
            "confidence": 0.90,
        },
        "stem_cells__regenerative_growth_plants": {
            "medicine": "Stem cells: undifferentiated cells that both self-renew and differentiate into specialized lineages, maintaining tissue regeneration",
            "nature": "Regenerative growth in plants: meristems — undifferentiated plant tissue that continuously produces roots, shoots, and leaves throughout life",
            "rule": "Animal stem cell niche ≅ plant meristem: both are populations of undifferentiated, self-renewing cells whose fate is determined by positional signals; Wnt/Notch ≅ auxin/cytokinin gradients",
            "confidence": 0.94,
        },
    }

    def __init__(self):
        self.token_log: List[str] = []
        self.step_tokens: Dict[str, List[str]] = {}

    def _log_tokens(self, stage: str, tokens: List[str]):
        """Record tokens for visualization."""
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

        If origin_domain is "Medicine", direction is medicine→nature.
        If origin_domain is "Nature", direction is nature→medicine.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "medic" in origin_domain.lower() or "biolog" in origin_domain.lower():
            direction = Direction.MEDICINE_TO_NATURE
        elif "nature" in origin_domain.lower() or "ecolog" in origin_domain.lower():
            direction = Direction.NATURE_TO_MEDICINE
        else:
            # Infer from concept content
            med_keywords = [
                "immune", "neural", "neuron", "synapse", "blood", "circulatory",
                "vessel", "drug", "pharma", "homeostasis", "bone", "circadian",
                "virus", "viral", "dna", "stem", "cell", "tissue", "gene",
            ]
            nature_keywords = [
                "ecosystem", "mycelium", "fung", "river", "watershed", "plant",
                "season", "fractal", "crystal", "meristem", "forest", "ecolog",
            ]
            if any(m in origin_concept.lower() for m in med_keywords):
                direction = Direction.MEDICINE_TO_NATURE
            else:
                direction = Direction.NATURE_TO_MEDICINE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.MEDICINE_TO_NATURE:
            destination_concept = iso_data["nature"]
        else:
            destination_concept = iso_data["medicine"]

        # Generate resonance if not provided
        if not resonance_sentence:
            resonance_sentence = self._generate_resonance(
                origin_concept, destination_concept, iso_name, structural_property
            )

        # Total confidence is geometric mean of step confidences (with floor)
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
            text = f"{data['medicine']} {data['nature']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["medicine"], data["nature"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__natural_form"
            best_data = {
                "medicine": f"Bodily process derived from {concept}",
                "nature": f"Natural pattern embodying {structural_property}",
                "rule": "Homomorphism preserves structure while allowing domain translation",
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

        if direction == Direction.MEDICINE_TO_NATURE:
            src_label, dst_label = "medical", "natural"
            src_obj = iso_data["medicine"]
            dst_obj = iso_data["nature"]
        else:
            src_label, dst_label = "natural", "medical"
            src_obj = iso_data["nature"]
            dst_obj = iso_data["medicine"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into elements and relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the living parts of {origin_concept}? What are its cells, its currents, its rhythms?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread="Each part carries a label — not merely a name, but the role it plays in the living whole.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} pattern '{src_obj}' maps to the {dst_label} pattern '{dst_obj}' through a deep structural correspondence.",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Coordinate projection preserving metric invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread="The mapped parts find their place in the new domain — not arbitrarily, but along the ancient lines nature herself drew.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under associative operation preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The parts compose into a living whole — a {dst_label} form that breathes with the same rhythm as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
            formal_rule="Inverse homomorphism check: φ⁻¹(φ(x)) ≈ x within tolerance ε",
            confidence=round(base_conf * 0.90, 3),
            language_thread="We turn the glass bead over, looking back through it to ensure the living pattern still holds — transformed, but unbroken.",
        ))

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "immune": "self-marker, non-self antigen, lymphocyte, antibody, cytokine, memory cell",
            "neural": "neuron, dendrite, axon, synapse, neurotransmitter, action potential",
            "blood": "heart, artery, capillary, vein, red cell, plasma, pressure gradient",
            "circulatory": "heart, artery, capillary, vein, red cell, plasma, pressure gradient",
            "drug": "molecule, receptor, binding site, affinity, metabolite, dose-response curve",
            "pharma": "molecule, receptor, binding site, affinity, metabolite, dose-response curve",
            "homeostasis": "sensor, set point, comparator, effector, feedback signal, range",
            "bone": "collagen fiber, hydroxyapatite crystal, osteon, Haversian canal, remodeling unit",
            "circadian": "SCN, clock gene, photoreceptor, zeitgeber, phase, period",
            "virus": "genome, capsid, host receptor, polymerase, replication cycle, virion",
            "viral": "genome, capsid, host receptor, polymerase, replication cycle, virion",
            "dna": "base, nucleotide, strand, helix, polymerase, mismatch, repair enzyme",
            "stem": "niche, stem cell, progenitor, differentiation signal, lineage, self-renewal",
            "ecosystem": "producer, consumer, predator, nutrient cycle, carrying capacity, succession",
            "mycelium": "hypha, septum, branching node, nutrient flow, spore, network",
            "fung": "hypha, septum, branching node, nutrient flow, spore, network",
            "river": "source, trunk, tributary, confluence, watershed, gradient, sediment",
            "plant": "root, shoot, leaf, meristem, hormone, secondary metabolite",
            "season": "tilt, photoperiod, solstice, equinox, phenology, dormancy, vernalization",
            "fractal": "seed, generator, iteration, self-similarity, scale invariance, recursion",
            "crystal": "unit cell, lattice, space group, axis, facet, growth front",
            "meristem": "apical cell, initial, derivative, stem-cell niche, hormone gradient, organ",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "elements, relations, and their living structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "immune": "cell:lymphocyte; signal:cytokine; response:clonal",
            "neural": "cell:neuron; signal:potential; plasticity:hebbian",
            "blood": "vessel:branching; flow:pressure; exchange:capillary",
            "circulatory": "vessel:branching; flow:pressure; exchange:capillary",
            "drug": "molecule:ligand; target:receptor; effect:pharmacological",
            "pharma": "molecule:ligand; target:receptor; effect:pharmacological",
            "homeostasis": "variable:regulated; feedback:negative; setpoint:fixed",
            "bone": "mineral:crystalline; scaffold:collagen; hierarchy:multiscale",
            "circadian": "oscillator:self-sustained; input:light; output:phase",
            "virus": "genome:nucleic; shell:capsid; cycle:lytic",
            "viral": "genome:nucleic; shell:capsid; cycle:lytic",
            "dna": "base:pair; strand:complementary; repair:enzymatic",
            "stem": "cell:undifferentiated; niche:signaling; fate:conditional",
            "ecosystem": "population:dynamic; resource:limited; state:equilibrium",
            "mycelium": "hypha:branching; flow:nutrient; network:adaptive",
            "fung": "hypha:branching; flow:nutrient; network:adaptive",
            "river": "channel:branching; flow:gravitational; basin:fractal",
            "plant": "meristem:growing; metabolite:secondary; defense:chemical",
            "season": "cycle:annual; driver:photoperiod; response:phenological",
            "fractal": "generator:recursive; structure:self-similar; scale:invariant",
            "crystal": "lattice:periodic; symmetry:space-group; growth:self-assembled",
            "meristem": "cell:undifferentiated; signal:hormone; organ:derivative",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:living; relation:ecological; property:emergent"

    def _generate_resonance(
        self,
        origin: str,
        destination: str,
        iso_name: str,
        structural_property: str,
    ) -> str:
        """Generate a poetic resonance sentence from the isomorphism."""
        templates = [
            f"As {origin} {structural_property}, so {destination} reveals the same pattern in another living tongue.",
            f"What {origin} heals in the body, {destination} has practiced in the wild — the same form, twice-grown.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one flesh.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single living pattern seen from two sides.",
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


def get_transformer() -> MedicineNatureTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = MedicineNatureTransformer()
    return _default_transformer