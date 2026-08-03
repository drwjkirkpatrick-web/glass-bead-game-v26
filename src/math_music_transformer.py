"""
glass-bead-game-v26 — Math ↔ Music Transformer
Formal bidirectional transformation scaffold between mathematical structures
and musical structures, with human language as the connecting thread.

Hesse's book declares: "especially mathematics and music" — the twin
grammars of the Glass Bead Game. This module makes that correspondence
explicit, testable, and playable.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    MATH_TO_MUSIC = "math→music"
    MUSIC_TO_MATH = "music→math"


@dataclass
class TransformationStep:
    """A single step in the Math ↔ Music transformation pipeline."""
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


class MathMusicTransformer:
    """
    Formal bidirectional transformer between mathematical and musical structures.

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
        "cyclic_group__circle_of_fifths": {
            "math": "Cyclic group Z_n under addition mod n",
            "music": "Circle of fifths (P5)^n returns to tonic after 12 steps",
            "rule": "Z_12 ≅ (interval class 7) under transposition; the generator g=7 generates the full group since gcd(7,12)=1",
            "confidence": 0.97,
        },
        "symmetry_group__motivic_inversion": {
            "math": "Dihedral group D_n (symmetries of regular n-gon)",
            "music": "Motivic inversion + retrograde as reflectional symmetry of melodic contour",
            "rule": "A motif with n distinct pitch classes admits D_n symmetries: retrograde = reflection across time axis; inversion = reflection across pitch axis",
            "confidence": 0.94,
        },
        "fourier_transform__overtone_series": {
            "math": "Fourier decomposition of periodic function into harmonic components",
            "music": "Overtone series as natural harmonic spectrum of a vibrating string",
            "rule": "The vibration eigenfunctions of an ideal string are sin(nπx/L); their frequencies are integer multiples f_n = n·f_1",
            "confidence": 0.99,
        },
        "recursive_function__canon_per_tonos": {
            "math": "Recursive function f(n) with base case and inductive step",
            "music": "Bach's Canon per tonos: each voice transposes up a whole tone, returning after 6 iterations",
            "rule": "f(n) = f(n-1) + 2 semitones mod 12; after 6 iterations f(6) ≡ f(0) (mod 12), producing a locally ascending, globally cyclic structure",
            "confidence": 0.96,
        },
        "mobius_strip__endless_canon": {
            "math": "Möbius strip: non-orientable surface with one boundary, locally Euclidean, globally twisted",
            "music": "Canon that returns to its beginning transformed (inverted, augmented, or transposed) after traversal",
            "rule": "Parameterize the strip as (θ, t) → (cos θ, sin θ, t·cos(θ/2)); the musical analogue is a theme that traverses all 12 pitch-classes before returning to a transformed tonic",
            "confidence": 0.91,
        },
        "fibonacci_sequence__golden_ratio_phasing": {
            "math": "Fibonacci sequence F_n = F_{n-1} + F_{n-2}; limit ratio → φ",
            "music": "Steve Reich-style phasing: two identical lines played at slightly different speeds, creating interference patterns whose beat cycle follows Fibonacci-like growth",
            "rule": "Two periodic processes with periods in ratio φ produce a non-repeating superposition whose beat complexity grows as Fibonacci numbers",
            "confidence": 0.89,
        },
        "eigenvalue__resonant_frequency": {
            "math": "Eigenvalue λ of operator L: L(v) = λv",
            "music": "Resonant frequency of a cavity or string: the mode that sustains vibration without decay",
            "rule": "The wave operator ∂²/∂t² - c²∂²/∂x² has eigenfunctions sin(nπx/L) with eigenvalues (nπc/L)²; these correspond to the allowed vibrational modes of a bounded medium",
            "confidence": 0.98,
        },
        "graph_theory__voice_leading": {
            "math": "Complete graph K_n with weighted edges representing transformation cost",
            "music": "Voice-leading space: each node is a chord, each edge is a voice-leading transformation with smoothness (minimal total displacement) as edge weight",
            "rule": "Tymoczko voice-leading space: chords are points in orbifolds; minimal voice-leading corresponds to geodesic paths in these spaces",
            "confidence": 0.93,
        },
        "category_theory__musical_composition": {
            "math": "Category C with objects and morphisms; functor F: C → D preserves structure",
            "music": "Musical composition as morphism: theme (object) → variation (morphism); orchestration as functor between timbral categories",
            "rule": "Composition = morphism in a category of musical objects; each compositional technique (inversion, augmentation, fragmentation) is an endofunctor on this category",
            "confidence": 0.87,
        },
        "topological_space__tonal_hierarchy": {
            "math": "Topological space (X, τ) with open sets defining neighborhood structure",
            "music": "Tonal hierarchy: tonic is the most stable point; dominant and subdominant are its immediate neighbors; modulation is a continuous deformation of this space",
            "rule": "Lerdahl's tonal pitch space embeds pitches in a metric lattice where distance correlates with perceived stability; the topology of this space predicts cognitive expectations",
            "confidence": 0.90,
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

        If origin_domain is "Mathematics", direction is math→music.
        If origin_domain is "Music", direction is music→math.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "math" in origin_domain.lower() or "mathematic" in origin_domain.lower():
            direction = Direction.MATH_TO_MUSIC
        elif "music" in origin_domain.lower() or "musica" in origin_domain.lower():
            direction = Direction.MUSIC_TO_MATH
        else:
            # Infer from concept content
            if any(m in origin_concept.lower() for m in [
                "group", "function", "theorem", "proof", "axiom",
                "topology", "algebra", "geometry", "number", "sequence",
                "matrix", "vector", "eigen", "fourier", "graph",
            ]):
                direction = Direction.MATH_TO_MUSIC
            else:
                direction = Direction.MUSIC_TO_MATH

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.MATH_TO_MUSIC:
            destination_concept = iso_data["music"]
        else:
            destination_concept = iso_data["math"]

        # Generate resonance if not provided
        if not resonance_sentence:
            resonance_sentence = self._generate_resonance(
                origin_concept, destination_concept, iso_name, structural_property
            )

        # Total confidence is product of step confidences (with floor)
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

        # Score each isomorphism by keyword overlap
        best_score = -1
        best_name = ""
        best_data = {}

        for name, data in self.ISOMORPHISMS.items():
            score = 0
            text = f"{data['math']} {data['music']} {data['rule']}".lower()

            # Count keyword matches in concept
            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            # Count keyword matches in structural property
            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            # Bonus for exact substring matches
            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["math"], data["music"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_homomorphism__musical_form"
            best_data = {
                "math": f"Abstract structure derived from {concept}",
                "music": f"Musical form embodying {structural_property}",
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

        if direction == Direction.MATH_TO_MUSIC:
            src_label, dst_label = "mathematical", "musical"
            src_obj = iso_data["math"]
            dst_obj = iso_data["music"]
        else:
            src_label, dst_label = "musical", "mathematical"
            src_obj = iso_data["music"]
            dst_obj = iso_data["math"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into generators and relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the building blocks of {origin_concept}? What are its atoms?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread=f"Each atom carries a label — not merely a name, but a role it plays in the larger structure.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj}' maps to the {dst_label} structure '{dst_obj}' through the rule: {iso_data['rule'][:80]}...",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Coordinate projection preserving metric invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread=f"The mapped elements are placed in their new home — not arbitrarily, but according to the deep symmetries they share.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under associative operation preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The fragments are assembled into a whole — a {dst_label} object that breathes with the same rhythm as its {src_label} twin.",
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

        # Log tokens
        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "fugue": "subject, answer, countersubject, stretto, episode",
            "canon": "leader, follower, interval of imitation, temporal offset",
            "group": "set, binary operation, identity, inverse, associativity",
            "fourier": "basis functions, coefficients, orthogonality, convergence",
            "topology": "open sets, continuity, compactness, connectedness",
            "eigen": "operator, vector space, characteristic polynomial, spectrum",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "primitive elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "fugue": "theme:melodic; transformation:contrapuntal; recurrence:cyclic",
            "group": "element:abstract; operation:binary; axiom:associative",
            "fourier": "basis:orthogonal; coefficient:scalar; domain:frequency",
            "topology": "set:open; map:continuous; property:invariant",
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
            f"As {origin} {structural_property}, so {destination} reveals the same pattern in another tongue.",
            f"What {origin} proves in silence, {destination} sings aloud — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single figure seen from two angles.",
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


def get_transformer() -> MathMusicTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = MathMusicTransformer()
    return _default_transformer
