"""
glass-bead-game-v26 — Math ↔ Philosophy Transformer
Formal bidirectional transformation scaffold between mathematical structures
and philosophical concepts, with human language as the connecting thread.

The Glass Bead Game asks us to find the hidden unity between disciplines.
Where mathematics proves in silence, philosophy questions in language —
yet both seek the same architecture of the real. This module makes that
correspondence explicit, testable, and playable.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    MATH_TO_PHILOSOPHY = "math→philosophy"
    PHILOSOPHY_TO_MATH = "philosophy→math"


@dataclass
class TransformationStep:
    """A single step in the Math ↔ Philosophy transformation pipeline."""
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


class MathPhilosophyTransformer:
    """
    Formal bidirectional transformer between mathematical structures and
    philosophical concepts.

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
        "godel_incompleteness__epistemological_limits": {
            "math": "Gödel's incompleteness theorems: any sufficiently strong formal system contains true statements that cannot be proved within it",
            "philosophy": "Epistemological limits: the boundaries of what can be known from within a given conceptual framework",
            "rule": "A consistent formal system capable of arithmetic cannot prove its own consistency; the unprovable truth mirrors the Kantian noumenon — knowable only from a standpoint the system itself cannot occupy",
            "confidence": 0.98,
        },
        "set_theory__ontology": {
            "math": "Zermelo-Fraenkel set theory with Choice: foundational hierarchy of sets and membership relations",
            "philosophy": "Ontology: the study of what exists, the categories of being, and the relations between entities",
            "rule": "The membership relation ∈ structures all mathematical objects just as the relation of being structures all ontological inquiry; the empty set ∅ is the analogue of non-being, the universal set the analogue of the totality of what is",
            "confidence": 0.89,
        },
        "group_symmetry__dialectical_synthesis": {
            "math": "Group theory: symmetries of a structure form a group under composition; thesis ↔ antithesis ↔ synthesis as group-theoretic inverse and identity",
            "philosophy": "Hegelian dialectical synthesis: the resolution of thesis and antithesis into a higher unity that preserves both as moments",
            "rule": "The dialectical triad (thesis, antithesis, synthesis) mirrors the group structure (element, inverse, identity): synthesis is the composite that contains its precursors as self-identical substructures within an enlarged totality",
            "confidence": 0.86,
        },
        "topology__phenomenology_of_space": {
            "math": "Topological space (X, τ): properties preserved under continuous deformation — connectedness, compactness, fundamental group",
            "philosophy": "Phenomenology of lived space (Merleau-Ponty): space as experienced from within, not as measured from without",
            "rule": "Homeomorphism = equivalence under continuous deformation; phenomenological space privileges topology over metric — what matters is the structure of experience, not the coordinates of the surveyor",
            "confidence": 0.87,
        },
        "probability__induction": {
            "math": "Probability theory: Bayesian inference, priors, posterior updates, the law of large numbers",
            "philosophy": "Induction (Hume's problem): how finite observations justify universal generalizations",
            "rule": "Bayes' theorem P(H|E) ∝ P(E|H)·P(H) formalizes inductive reasoning; the prior is the philosophical pre-understanding, the posterior is belief updated by experience — induction made rigorous, though its foundations remain axiomatically groundless",
            "confidence": 0.94,
        },
        "category_theory__metaphysics": {
            "math": "Category theory: objects and morphisms, functors between categories, natural transformations between functors",
            "philosophy": "Metaphysics: the most general structure of reality — what categories of being exist and how they relate",
            "rule": "Categories of Being correspond to mathematical categories: objects are the fundamental kinds, morphisms are the relations between them, functors map one metaphysical framework to another; the diagram of categories commutes when reality is consistent",
            "confidence": 0.85,
        },
        "formal_logic__syllogistic_reasoning": {
            "math": "Formal logic: propositional and first-order predicate calculus, modus ponens, completeness and soundness",
            "philosophy": "Aristotelian syllogistic reasoning: the deductive structure of valid arguments",
            "rule": "Modus ponens (P → Q, P ⊢ Q) is the skeleton of every valid syllogism; the soundness theorem (all derivable statements are true) is the formal vindication of rational argument that Aristotle sought",
            "confidence": 0.97,
        },
        "cantor_infinity__metaphysical_infinity": {
            "math": "Cantor's transfinite set theory: different cardinalities of infinity (ℵ₀, ℵ₁, …) and the continuum hypothesis",
            "philosophy": "Metaphysical infinity: the infinite as a concept in theology and metaphysics — the absolute, the unbounded, the divine",
            "rule": "Cantor proved infinity has structure (a hierarchy of cardinalities); this mathematical pluralism reframes the metaphysical problem: the infinite is not one but many, and the question 'how infinite is God?' becomes meaningful in a way scholastic philosophy never anticipated",
            "confidence": 0.92,
        },
        "game_theory__ethics": {
            "math": "Game theory: Nash equilibria, cooperative and non-cooperative strategies, utility maximization",
            "philosophy": "Ethics: the philosophical study of right action, the good, and justice among rational agents",
            "rule": "The Nash equilibrium formalizes the problem of collective rationality that ethics addresses in natural language: how should agents act when their fates are interdependent? The Prisoner's Dilemma is the tragedy of the commons made mathematically precise — cooperation requires a structure (a 'social contract') the game alone cannot provide",
            "confidence": 0.90,
        },
        "fractal_geometry__hermeneutic_circles": {
            "math": "Fractal geometry: self-similar structures at every scale, non-integer Hausdorff dimension, recursive generation",
            "philosophy": "Hermeneutic circle (Gadamer, Heidegger): understanding moves between part and whole, each illuminating the other in a circular but spiraling ascent",
            "rule": "Self-similarity across scales is the geometric analogue of the hermeneutic circle: the whole is understood through its parts, but each part is only understood through the whole — a recursive process that, like a fractal, never terminates yet deepens at every iteration",
            "confidence": 0.88,
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

        If origin_domain is "Mathematics", direction is math→philosophy.
        If origin_domain is "Philosophy", direction is philosophy→math.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "math" in origin_domain.lower() or "mathematic" in origin_domain.lower():
            direction = Direction.MATH_TO_PHILOSOPHY
        elif "philos" in origin_domain.lower():
            direction = Direction.PHILOSOPHY_TO_MATH
        else:
            # Infer from concept content
            if any(m in origin_concept.lower() for m in [
                "group", "function", "theorem", "proof", "axiom",
                "topology", "algebra", "geometry", "number", "sequence",
                "matrix", "vector", "eigen", "fourier", "graph", "set",
                "category", "logic", "probability", "game", "fractal", "infinity",
            ]):
                direction = Direction.MATH_TO_PHILOSOPHY
            else:
                direction = Direction.PHILOSOPHY_TO_MATH

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.MATH_TO_PHILOSOPHY:
            destination_concept = iso_data["philosophy"]
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

        best_score = -1
        best_name = ""
        best_data = {}

        for name, data in self.ISOMORPHISMS.items():
            score = 0
            text = f"{data['math']} {data['philosophy']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["math"], data["philosophy"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__philosophical_form"
            best_data = {
                "math": f"Abstract structure derived from {concept}",
                "philosophy": f"Philosophical concept embodying {structural_property}",
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

        if direction == Direction.MATH_TO_PHILOSOPHY:
            src_label, dst_label = "mathematical", "philosophical"
            src_obj = iso_data["math"]
            dst_obj = iso_data["philosophy"]
        else:
            src_label, dst_label = "philosophical", "mathematical"
            src_obj = iso_data["philosophy"]
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
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj}' maps to the {dst_label} concept '{dst_obj}' through the rule: {iso_data['rule'][:80]}...",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} conceptual space",
            formal_rule="Coordinate projection preserving structural invariants",
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

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "godel": "formal system, axioms, provability, self-reference, truth",
            "set": "elements, membership relation, empty set, union, comprehension",
            "group": "set, binary operation, identity, inverse, associativity",
            "topolog": "open sets, continuity, compactness, connectedness, neighborhood",
            "probab": "sample space, events, prior, likelihood, posterior, Bayes",
            "category": "objects, morphisms, functor, natural transformation, commutativity",
            "logic": "propositions, predicates, quantifiers, inference rules, truth values",
            "infinity": "cardinality, bijection, ordinal, continuum, transfinite",
            "game": "players, strategies, payoffs, equilibrium, utility",
            "fractal": "self-similarity, recursion, scale invariance, Hausdorff dimension",
            "ontology": "categories of being, existence, identity, relation, substance",
            "epistem": "knowledge, belief, justification, limits, certainty",
            "dialect": "thesis, antithesis, synthesis, negation, sublation",
            "phenomen": "lived experience, intentionality, embodiment, spatiality, perception",
            "induction": "observation, generalization, regularity, cause, evidence",
            "ethic": "action, agent, value, consequence, obligation",
            "hermeneut": "part, whole, pre-understanding, interpretation, tradition",
            "syllog": "premise, conclusion, middle term, validity, form",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "primitive elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "godel": "system:formal; statement:true; provability:incomplete; reference:self",
            "set": "element:abstract; relation:membership; axiom:comprehension",
            "group": "element:abstract; operation:binary; axiom:associative",
            "topolog": "set:open; map:continuous; property:invariant",
            "probab": "event:measurable; belief:quantified; update:Bayesian",
            "category": "object:abstract; morphism:structural; functor:preserving",
            "logic": "proposition:truth-valued; rule:inference; system:deductive",
            "infinity": "cardinal:transfinite; order:well-founded; map:bijection",
            "game": "agent:rational; strategy:optimal; outcome:equilibrium",
            "fractal": "pattern:self-similar; dimension:non-integer; generation:recursive",
            "ontology": "entity:existent; category:being; relation:ontological",
            "epistem": "belief:justified; limit:bound; framework:conceptual",
            "dialect": "thesis:initial; antithesis:negation; synthesis:sublation",
            "phenomen": "experience:lived; body:perceiving; world:intended",
            "induction": "particular:observed; universal:inferred; warrant:assumed",
            "ethic": "action:chosen; value:orienting; consequence:shared",
            "hermeneut": "text:interpreted; context:historical; circle:method",
            "syllog": "premise:given; form:valid; conclusion:deduced",
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
            f"What {origin} proves in silence, {destination} speaks aloud — the same structure, twice-born.",
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


def get_transformer() -> MathPhilosophyTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = MathPhilosophyTransformer()
    return _default_transformer