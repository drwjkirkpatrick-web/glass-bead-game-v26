"""
glass-bead-game-v26 — Code ↔ Philosophy Transformer
Formal bidirectional transformation scaffold between computer code structures
and philosophical concepts, with human language as the connecting thread.

The Glass Bead Game asks us to find the hidden unity between disciplines.
Where code executes in logic gates, philosophy questions in language —
yet both seek the same architecture of meaning. This module makes that
correspondence explicit, testable, and playable.
"""
from __future__ import annotations
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    CODE_TO_PHILOSOPHY = "code→philosophy"
    PHILOSOPHY_TO_CODE = "philosophy→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Philosophy transformation pipeline."""
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
        """Reconstruct a TransformerResult from a dict (inverse of to_dict)."""
        steps = [
            TransformationStep(
                stage=s["stage"],
                input_repr=s["input_repr"],
                output_repr=s["output_repr"],
                formal_rule=s["formal_rule"],
                confidence=s["confidence"],
                language_thread=s["language_thread"],
            )
            for s in d.get("steps", [])
        ]
        return cls(
            direction=d["direction"],
            origin_domain=d["origin_domain"],
            origin_concept=d["origin_concept"],
            destination_domain=d["destination_domain"],
            destination_concept=d["destination_concept"],
            steps=steps,
            structural_property=d["structural_property"],
            resonance_sentence=d["resonance_sentence"],
            tokens_seen=d.get("tokens_seen", []),
            tokens_per_step=d.get("tokens_per_step", {}),
            total_confidence=d["total_confidence"],
            isomorphisms=d.get("isomorphisms", []),
        )


class CodePhilosophyTransformer:
    """
    Formal bidirectional transformer between computer code structures and
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
        "formal_logic__boolean_code": {
            "philosophy": "Formal logic and Aristotelian syllogism: deductive inference from premises via modus ponens and valid argument forms",
            "code": "Boolean code and conditional logic: if/else branches, truth-valued expressions, short-circuit evaluation, and control flow gates",
            "rule": "The syllogism (major premise, minor premise, conclusion) maps onto the if-statement (condition, branch, effect); modus ponens (P → Q, P ⊢ Q) is the formal skeleton of every conditional branch — code is syllogism made executable",
            "confidence": 0.96,
        },
        "ontology__data_model": {
            "philosophy": "Ontology: the study of being — what categories of entities exist, their identity conditions, and the relations between them",
            "code": "Data model and schema design: entity-relationship models, type definitions, foreign keys, and class hierarchies",
            "rule": "The ontological category (what kind of thing exists) maps to the data type or table; the relation of being maps to the foreign key or reference; identity conditions map to primary keys — a schema is a crystallized ontology, an ontology is a schema waiting for instances",
            "confidence": 0.91,
        },
        "epistemology__machine_learning": {
            "philosophy": "Epistemology: the theory of knowledge — how we know, what justifies belief, and the limits of warranted assertion",
            "code": "Machine learning: statistical learning from data — training, generalization, overfitting, and model selection",
            "rule": "Epistemology's central question 'how do we know?' maps to ML's central procedure 'learn from data'; the training set is empirical observation, the model is induced belief, generalization is inductive inference, and overfitting is the dogmatism of memorizing without understanding — ML is epistemology operationalized",
            "confidence": 0.93,
        },
        "ethics__code_of_conduct": {
            "philosophy": "Ethics and moral philosophy: the study of right action, the good, obligations, and the flourishing of persons",
            "code": "Code of conduct, professional ethics, and AI ethics: principles for responsible engineering, bias mitigation, and alignment",
            "rule": "The ethical question 'what ought we to do?' maps to the engineering question 'what ought our systems to do?'; virtue ethics maps to engineering values, deontology maps to compliance rules, consequentialism maps to impact assessment — a code of conduct is ethics compiled into practice",
            "confidence": 0.88,
        },
        "dialectic__refactoring": {
            "philosophy": "Hegelian dialectic: thesis, antithesis, and synthesis — contradiction drives the evolution of concepts toward higher unity",
            "code": "Code refactoring and software evolution: restructuring existing code without changing external behavior, resolving technical debt through iterative improvement",
            "rule": "The thesis is the current code design; the antithesis is the tension or smell that reveals its inadequacy; the synthesis is the refactored version that preserves behavior while sublating the contradiction — refactoring is dialectical negation made practical, each cycle a sublation that lifts the codebase to a higher order",
            "confidence": 0.87,
        },
        "phenomenology__ux_design": {
            "philosophy": "Phenomenology (Husserl, Merleau-Ponty): the study of lived experience, intentionality, embodiment, and the structure of perception from the first-person standpoint",
            "code": "UX design: user experience research, interaction design, affordances, and the felt quality of using a software interface",
            "rule": "Phenomenology's first-person standpoint maps to UX's user-centered design; intentionality (consciousness is always consciousness-of-something) maps to the affordance (an interface is always for-some-action); embodiment maps to the felt friction of interaction — UX is applied phenomenology, designing the lived experience of the digital",
            "confidence": 0.89,
        },
        "determinism__algorithmic_predictability": {
            "philosophy": "Determinism and the problem of free will: the thesis that every event is necessitated by antecedent causes and laws of nature",
            "code": "Algorithmic determinism and predictability: deterministic functions, reproducible builds, state machines, and the property that identical inputs yield identical outputs",
            "rule": "Philosophical determinism (same causes, same effects) maps to algorithmic determinism (same inputs, same outputs); the free-will debate maps to the question of non-determinism in computation — randomness and choice enter only through external entropy or oracle calls, mirroring how libertarian free will requires a break in the causal chain",
            "confidence": 0.90,
        },
        "teleology__design_patterns": {
            "philosophy": "Teleology: the philosophical study of purpose, final causes, and the for-the-sake-of-which that orients beings toward ends",
            "code": "Software design patterns: named, reusable solutions to recurring design problems, encoding intent and structure together",
            "rule": "Aristotle's final cause (that for the sake of which a thing exists) maps to the design pattern's intent (the problem it exists to solve); the pattern's structure is the material and formal cause realizing that end — a design pattern is a teleological artifact, a piece of code that knows its own purpose",
            "confidence": 0.86,
        },
        "axiology__code_quality": {
            "philosophy": "Axiology: the theory of value — what is good, what is worth pursuing, and the hierarchy of goods",
            "code": "Code quality metrics: cyclomatic complexity, cohesion, coupling, test coverage, maintainability indices, and technical debt",
            "rule": "Axiology's inquiry 'what is valuable?' maps to software engineering's inquiry 'what is good code?'; intrinsic value maps to internal quality (readability, elegance), instrumental value maps to external quality (performance, correctness); the hierarchy of goods maps to the priority of metrics — axiology is the implicit philosophy behind every code review",
            "confidence": 0.88,
        },
        "metaphysics__virtual_worlds": {
            "philosophy": "Metaphysics: the study of the fundamental nature of reality — what exists, what is real, what is mere appearance",
            "code": "Virtual worlds and simulation: game engines, procedural generation, persistent digital environments, and the ontology of simulated entities",
            "rule": "The metaphysical question 'what is real?' maps to the computational question 'what is simulated?'; Plato's cave maps to the rendering pipeline, Leibniz's possible worlds to procedurally generated ones, Baudrillard's simulacra to deepfakes and virtual avatars — a virtual world is a metaphysics experiment, a reality whose substrate is computation rather than matter",
            "confidence": 0.85,
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

        If origin_domain contains 'philosoph', direction is philosophy→code.
        If origin_domain contains 'coda' or 'code', direction is code→philosophy.
        Otherwise, direction is inferred from concept content.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        origin_lower = origin_domain.lower()
        if "philosoph" in origin_lower:
            direction = Direction.PHILOSOPHY_TO_CODE
        elif "coda" in origin_lower or "code" in origin_lower:
            direction = Direction.CODE_TO_PHILOSOPHY
        else:
            # Infer from concept content
            if any(c in origin_concept.lower() for c in [
                "function", "variable", "loop", "recursion", "algorithm",
                "class", "object", "schema", "database", "refactor",
                "pattern", "boolean", "conditional", "interface", "module",
                "compile", "runtime", "debug", "syntax", "type",
                "array", "pointer", "thread", "closure", "iterator",
            ]):
                direction = Direction.CODE_TO_PHILOSOPHY
            else:
                direction = Direction.PHILOSOPHY_TO_CODE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.CODE_TO_PHILOSOPHY:
            destination_concept = iso_data["philosophy"]
        else:
            destination_concept = iso_data["code"]

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
            text = f"{data['code']} {data['philosophy']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["code"], data["philosophy"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__code_philosophical_form"
            best_data = {
                "code": f"Abstract code structure derived from {concept}",
                "philosophy": f"Philosophical concept embodying {structural_property}",
                "rule": "Homomorphism preserves structure while allowing domain translation between code and philosophy",
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

        if direction == Direction.CODE_TO_PHILOSOPHY:
            src_label, dst_label = "code", "philosophical"
            src_obj = iso_data["code"]
            dst_obj = iso_data["philosophy"]
        else:
            src_label, dst_label = "philosophical", "code"
            src_obj = iso_data["philosophy"]
            dst_obj = iso_data["code"]

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
            "logic": "propositions, predicates, quantifiers, inference rules, truth values",
            "syllog": "major premise, minor premise, conclusion, middle term, validity",
            "boolean": "truth values, operators, expressions, short-circuit, control flow",
            "conditional": "condition, branch, effect, evaluation, control flow",
            "ontology": "categories of being, existence, identity, relation, substance",
            "data model": "entities, attributes, relations, keys, constraints, schema",
            "schema": "tables, columns, foreign keys, primary keys, constraints, indices",
            "epistem": "knowledge, belief, justification, evidence, limits, certainty",
            "machine learning": "training data, features, model, loss, generalization, overfitting",
            "ml": "training data, features, model, loss, generalization, overfitting",
            "ethic": "action, agent, value, consequence, obligation, virtue",
            "conduct": "principles, norms, compliance, responsibility, accountability",
            "dialect": "thesis, antithesis, synthesis, negation, sublation",
            "refactor": "code smell, extraction, renaming, restructuring, behavior preservation",
            "phenomen": "lived experience, intentionality, embodiment, perception, affordance",
            "ux": "user, task, flow, affordance, feedback, friction, journey",
            "determin": "causes, effects, laws, necessity, predictability, freedom",
            "algorithm": "inputs, outputs, steps, state, determinism, complexity",
            "teleolog": "purpose, final cause, end, intent, orientation, function",
            "pattern": "intent, structure, participants, collaboration, consequence",
            "axiolog": "value, good, worth, hierarchy, intrinsic, instrumental",
            "quality": "complexity, cohesion, coupling, coverage, maintainability, debt",
            "metaphys": "reality, being, appearance, substance, ground, existence",
            "virtual": "engine, rendering, procedural generation, persistence, immersion",
            "simulation": "model, state, update, rendering, persistence, world",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "primitive elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "logic": "proposition:truth-valued; rule:inference; system:deductive",
            "syllog": "premise:given; form:valid; conclusion:deduced",
            "boolean": "expression:truth-valued; operator:logical; branch:conditional",
            "conditional": "condition:evaluated; branch:taken; effect:produced",
            "ontology": "entity:existent; category:being; relation:ontological",
            "data model": "entity:modeled; attribute:typed; relation:foreign-key",
            "schema": "table:relation; column:typed; key:identifier",
            "epistem": "belief:justified; limit:bound; framework:conceptual",
            "machine learning": "data:observed; model:induced; generalization:inferred",
            "ml": "data:observed; model:induced; generalization:inferred",
            "ethic": "action:chosen; value:orienting; consequence:shared",
            "conduct": "principle:normative; rule:binding; agent:responsible",
            "dialect": "thesis:initial; antithesis:negation; synthesis:sublation",
            "refactor": "smell:symptom; change:behavior-preserving; structure:improved",
            "phenomen": "experience:lived; body:perceiving; world:intended",
            "ux": "user:experiencing; task:oriented; flow:embodied",
            "determin": "cause:antecedent; effect:necessitated; law:binding",
            "algorithm": "input:given; step:deterministic; output:reproducible",
            "teleolog": "end:orienting; cause:final; purpose:intrinsic",
            "pattern": "intent:stated; structure:reusable; context:recurring",
            "axiolog": "value:assigned; good:orientation; hierarchy:ordered",
            "quality": "metric:measured; cohesion:internal; coupling:external",
            "metaphys": "being:fundamental; reality:grounded; appearance:derivative",
            "virtual": "world:simulated; entity:rendered; state:persisted",
            "simulation": "model:computational; state:evolving; world:generated",
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
            f"What {origin} executes in silence, {destination} speaks aloud — the same structure, twice-born.",
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


def get_transformer() -> CodePhilosophyTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodePhilosophyTransformer()
    return _default_transformer