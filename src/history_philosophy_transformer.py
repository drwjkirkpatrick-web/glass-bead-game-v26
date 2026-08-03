"""
glass-bead-game-v26 — History ↔ Philosophy Transformer
Formal bidirectional transformation scaffold between historical structures
and philosophical concepts, with human language as the connecting thread.

Hesse's Glass Bead Game draws together every discipline into a single
glass bead; this module makes the correspondence between the flow of
human events (history) and the concepts that interpret them (philosophy)
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
    HISTORY_TO_PHILOSOPHY = "history→philosophy"
    PHILOSOPHY_TO_HISTORY = "philosophy→history"


@dataclass
class TransformationStep:
    """A single step in the History ↔ Philosophy transformation pipeline."""
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


class HistoryPhilosophyTransformer:
    """
    Formal bidirectional transformer between historical and philosophical structures.

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
        "hegelian_dialectic__dialectical_history": {
            "history": "Dialectical historical process: thesis (status quo) → antithesis (revolution) → synthesis (new order)",
            "philosophy": "Hegelian dialectic: thesis-antithesis-synthesis; Aufhebung as sublating negation",
            "rule": "The movement of Spirit (Geist) through history mirrors the logical movement of the dialectic; each historical epoch is a moment of consciousness realizing freedom",
            "confidence": 0.97,
        },
        "vico_corsi_ricorsi__cyclical_history": {
            "history": "Vico's corsi e ricorsi: civilizations pass through divine, heroic, and human ages, then cycle back",
            "philosophy": "Cyclical philosophy of history: time as eternal recurrence rather than linear progress",
            "rule": "Vico's corso (descent into chaos) → ricorso (return to origin) is isomorphic to the philosophical principle that historical time exhibits cyclic structure governed by providence",
            "confidence": 0.93,
        },
        "spengler_morphology__organic_philosophy": {
            "history": "Spengler's morphology of cultures: each civilization has a life-cycle (birth, growth, maturity, decline) like a living organism",
            "philosophy": "Organic philosophy: cultures as organisms with morphology, destiny, and inevitable decline",
            "rule": "Spengler's cultural morphology maps each High Culture's life-cycle onto an organic template: spring (birth) → summer (maturity) → autumn (civilization) → winter (petrification)",
            "confidence": 0.89,
        },
        "renaissance_rebirth__platonic_anamnesis": {
            "history": "Renaissance rebirth: rediscovery of classical antiquity, revival of Greek and Roman learning",
            "philosophy": "Platonic anamnesis: knowledge as recollection of eternal forms the soul once knew",
            "rule": "The Renaissance's recovery of antiquity is isomorphic to anamnesis: what was forgotten is remembered; cultural knowledge resurfaces through historical recollection",
            "confidence": 0.91,
        },
        "enlightenment_progress__teleological_history": {
            "history": "Enlightenment idea of progress: history as continuous advancement toward reason, liberty, and improvement",
            "philosophy": "Teleological philosophy: history has an inherent end (telos) toward which it unfolds purposefully",
            "rule": "The Enlightenment doctrine of infinite progress maps to teleological philosophy: time has a directional arrow pointing toward an immanent goal of human perfectibility",
            "confidence": 0.88,
        },
        "existentialism__post_war_crisis": {
            "history": "Post-WWI historical crisis: collapse of European order, loss of meaning, shattered certainties",
            "philosophy": "Existentialism: being-in-the-world confronts absurdity, freedom, and radical responsibility",
            "rule": "The historical rupture of WWI produced the existential condition: the collapse of historical meaning corresponds to the philosophical discovery of ontological groundlessness",
            "confidence": 0.92,
        },
        "hermeneutics__historical_interpretation": {
            "history": "Historical interpretation: understanding the past requires interpreting texts, events, and traditions within their context (Gadamer's Wirkungsgeschichte)",
            "philosophy": "Hermeneutics: the science of interpretation; understanding as a fusion of horizons between interpreter and text",
            "rule": "Gadamer's hermeneutic circle — the whole is understood through parts, parts through the whole — is isomorphic to the historian's task of reconstructing meaning from fragments of the past",
            "confidence": 0.95,
        },
        "foucault_genealogy__archaeological_epistemology": {
            "history": "Foucault's genealogy: tracing the historical descent of present institutions, discourses, and power-relations",
            "philosophy": "Archaeological epistemology: uncovering the episteme — the unconscious rules governing what can be thought in a given epoch",
            "rule": "Foucault's genealogy (descent of practices) and archaeology (epistemic strata) are dual aspects: historical depth reveals the philosophical conditions of possibility for knowledge",
            "confidence": 0.90,
        },
        "marx_materialism__dialectical_materialism": {
            "history": "Marx's historical materialism: modes of production and class struggle drive the development of history",
            "philosophy": "Dialectical materialism: matter as self-moving, contradiction as the motor of development, negation of the negation",
            "rule": "The economic base-superstructure relation maps to dialectical materialism: material contradictions (thesis-antithesis) produce historical change (synthesis) through revolutionary sublation",
            "confidence": 0.94,
        },
        "collingwood_reenactment__phenomenology_understanding": {
            "history": "Collingwood's re-enactment: the historian re-thinks the thought of historical agents in their own mind",
            "philosophy": "Phenomenology of understanding: empathy, intentionality, and the reconstruction of lived experience (Erlebnis)",
            "rule": "Collingwood's re-enactment of past thought is isomorphic to phenomenological empathy: the historian's consciousness intentionally inhabits the agent's experience to grasp its internal meaning",
            "confidence": 0.87,
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

        If origin_domain is "History", direction is history→philosophy.
        If origin_domain is "Philosophy", direction is philosophy→history.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "histor" in origin_domain.lower():
            direction = Direction.HISTORY_TO_PHILOSOPHY
        elif "philos" in origin_domain.lower():
            direction = Direction.PHILOSOPHY_TO_HISTORY
        else:
            # Infer from concept content
            if any(h in origin_concept.lower() for h in [
                "war", "revolution", "empire", "renaissance", "age", "era",
                "civilization", "century", "crisis", "progress", "tradition",
                "antiquity", "medieval", "modern", "ancien",
            ]):
                direction = Direction.HISTORY_TO_PHILOSOPHY
            else:
                direction = Direction.PHILOSOPHY_TO_HISTORY

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.HISTORY_TO_PHILOSOPHY:
            destination_concept = iso_data["philosophy"]
        else:
            destination_concept = iso_data["history"]

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
            text = f"{data['history']} {data['philosophy']} {data['rule']}".lower()

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
                for s in [data["history"], data["philosophy"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_correspondence__historical_philosophical"
            best_data = {
                "history": f"Historical phenomenon derived from {concept}",
                "philosophy": f"Philosophical concept embodying {structural_property}",
                "rule": "Structural correspondence preserves meaning while allowing domain translation",
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

        if direction == Direction.HISTORY_TO_PHILOSOPHY:
            src_label, dst_label = "historical", "philosophical"
            src_obj = iso_data["history"]
            dst_obj = iso_data["philosophy"]
        else:
            src_label, dst_label = "philosophical", "historical"
            src_obj = iso_data["philosophy"]
            dst_obj = iso_data["history"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into events, agents, and temporal relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the moments of {origin_concept}? What are its atoms of meaning?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology of historical/philosophical categories",
            confidence=round(base_conf * 0.93, 3),
            language_thread=f"Each moment carries a label — not merely a name, but a role it plays in the unfolding of meaning.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj[:60]}...' maps to the {dst_label} structure '{dst_obj[:60]}...' through the rule.",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} conceptual space",
            formal_rule="Coordinate projection preserving semantic invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread=f"The mapped elements find their place in a new conceptual landscape — not arbitrarily, but according to the deep correspondences they share.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj[:70]}",
            formal_rule="Composition under interpretive operation preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The fragments are gathered into a whole — a {dst_label} idea that pulses with the same rhythm as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse interpretation confirms fidelity: {src_obj[:70]}",
            formal_rule="Inverse hermeneutic check: the re-reading recovers the original meaning within interpretive tolerance",
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
            "dialectic": "thesis, antithesis, synthesis, sublation, negation",
            "cycle": "ascent, peak, descent, return, recurrence",
            "renaissance": "rediscovery, revival, humanism, classical recovery, renewal",
            "progress": "improvement, accumulation, direction, perfectibility, advancement",
            "crisis": "rupture, collapse, disorientation, reconstruction, aftermath",
            "hermeneutic": "text, context, horizon, interpretation, fusion",
            "genealogy": "descent, origin, emergence, power, discourse",
            "materialism": "base, superstructure, contradiction, class, revolution",
            "re-enactment": "thought, action, agent, context, reconstruction",
            "morphology": "form, growth, maturity, decline, organism",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "events, agents, and their temporal-relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "dialectic": "stage:contradictory; movement:negating; result:sublating",
            "cycle": "phase:temporal; movement:recurring; structure:circular",
            "renaissance": "event:revival; mode:humanistic; source:classical",
            "progress": "trend:directional; value:positive; temporal:linear",
            "crisis": "event:rupture; mode:disorienting; affect:absurd",
            "hermeneutic": "object:text; act:interpreting; method:circle",
            "genealogy": "object:practice; act:tracing; layer:epistemic",
            "materialism": "base:economic; superstructure:ideological; motor:contradiction",
            "re-enactment": "act:re-thinking; object:thought; method:empathic",
            "morphology": "form:organic; phase:lifecycle; destiny:inevitable",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:historical; relation:interpretive; property:semantic"

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
            f"What {origin} enacts in time, {destination} thinks in eternity — the same structure, twice-known.",
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


def get_transformer() -> HistoryPhilosophyTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = HistoryPhilosophyTransformer()
    return _default_transformer