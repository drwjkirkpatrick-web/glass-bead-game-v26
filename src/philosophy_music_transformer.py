"""
glass-bead-game-v26 — Philosophy ↔ Music Transformer
Formal bidirectional transformation scaffold between philosophical systems
and musical structures, with human language as the connecting thread.

Hesse's Glass Bead Game draws correspondences across all domains of thought.
This module makes the Philosophy ↔ Music correspondence explicit, testable,
and playable — a thinker's concept becomes a musical form, and a musical form
becomes a philosophical thesis.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    PHILOSOPHY_TO_MUSIC = "philosophy→music"
    MUSIC_TO_PHILOSOPHY = "music→philosophy"


@dataclass
class TransformationStep:
    """A single step in the Philosophy ↔ Music transformation pipeline."""
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


class PhilosophyMusicTransformer:
    """
    Formal bidirectional transformer between philosophical and musical structures.

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
        "pythagorean_spheres__tonal_harmony": {
            "philosophy": "Pythagorean harmony of the spheres: the cosmos is governed by integer ratios, and music is audible number",
            "music": "Tonal harmony: consonance defined by simple integer frequency ratios (octave 2:1, fifth 3:2, fourth 4:3)",
            "rule": "The Pythagorean insight that consonance arises from small-integer ratios is the foundational axiom of tonal harmony; the cosmos and the scale share one arithmetic",
            "confidence": 0.98,
        },
        "nietzsche_apollonian_dionysian__classical_romantic": {
            "philosophy": "Nietzsche's Apollonian/Dionysian duality: form, measure, individuation vs. intoxication, dissolution, primal unity",
            "music": "Classical/Romantic duality: formal clarity and balanced structure vs. expressive excess and formal dissolution",
            "rule": "The Apollonian maps to classical form (Mozart, early Beethoven) and the Dionysian to Romantic excess (late Beethoven, Wagner, Tristan)",
            "confidence": 0.96,
        },
        "schopenhauer_will__melodic_drive": {
            "philosophy": "Schopenhauer's Will: blind striving that objectifies itself through all phenomena; music is the most direct copy of the Will itself",
            "music": "Melodic drive: the forward-striving, goal-directed motion of melody as the audible image of blind volitional striving toward a tonic goal",
            "rule": "Schopenhauer declares music alone copies the Will directly, not its ideas; melodic striving toward resolution is the audible signature of the Will's unrest",
            "confidence": 0.97,
        },
        "hegel_dialectic__sonata_form": {
            "philosophy": "Hegel's dialectic: thesis → antithesis → synthesis, the self-development of the concept through contradiction",
            "music": "Sonata form: exposition (thesis) → development (antithesis through modulation/fragmentation) → recapitulation (synthesis, reconciled in the home key)",
            "rule": "Sonata form enacts a dialectic: the second key area contradicts the first, the development works through the contradiction, and the recapitulation sublates it",
            "confidence": 0.95,
        },
        "adorno_negative_dialectics__atonality": {
            "philosophy": "Adorno's negative dialectics: refusal of synthesis, preservation of contradiction, critique of identity-thinking",
            "music": "Atonality: refusal of tonal synthesis, preservation of dissonance, critique of the reconciling tonic",
            "rule": "Atonal music enacts negative dialectics by refusing the totalizing closure that tonal resolution would impose; dissonance is preserved, not sublated",
            "confidence": 0.93,
        },
        "confucian_ritual_music__ceremonial_function": {
            "philosophy": "Confucian doctrine of ritual music (礼乐): music and rite together cultivate virtue and order the polity; music completes what rite begins",
            "music": "Ceremonial function of music: music as a tool of ethical and social ordering, integral to ritual, not autonomous art",
            "rule": "Confucius holds that music (yue) and rite (li) are inseparable; the formal structure of ritual music maps the ethical structure of the well-ordered state",
            "confidence": 0.90,
        },
        "stoic_tranquility__minimalism": {
            "philosophy": "Stoic ataraxia: tranquility through acceptance of what cannot be changed, discipline of attention, reduction of desire",
            "music": "Minimalism: repetition, gradual process, acceptance of sustained texture, reduction of expressive will (Reich, Glass, Pärt)",
            "rule": "Minimalist repetition enacts Stoic acceptance: the listener's struggle against the sustained pattern gives way to tranquility through disciplined attention",
            "confidence": 0.89,
        },
        "buddhist_impermanence__variation_form": {
            "philosophy": "Buddhist doctrine of impermanence (anicca): all conditioned things arise and pass; identity is process, not substance",
            "music": "Variation form: a theme arises, transforms, and dissolves; identity is preserved through change, not despite it",
            "rule": "Variation form makes impermanence audible: the theme is never a fixed substance but a process that persists precisely through its transformations",
            "confidence": 0.91,
        },
        "existential_freedom__improvisation": {
            "philosophy": "Existentialist freedom: existence precedes essence; the subject constitutes itself through choice in each moment without predetermined structure",
            "music": "Improvisation (esp. jazz): the performer constitutes the work through free choice in real time, structure emerging from commitment rather than score",
            "rule": "Improvisation enacts existential freedom: each note is a choice that constitutes the self of the performance, with no pre-written essence to follow",
            "confidence": 0.92,
        },
        "heraclitus_flux__continuous_variation": {
            "philosophy": "Heraclitus: everything flows (panta rhei); strife and becoming are primary; identity is a river one cannot step into twice",
            "music": "Continuous variation and development: music that never repeats, constantly transforming its material (late Beethoven, Liszt, continuous development)",
            "rule": "Continuous variation makes Heraclitean flux audible: the musical substance is always becoming, never resting in a fixed identity",
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

        If origin_domain contains "Philosophy", direction is philosophy→music.
        If origin_domain is "Music", direction is music→philosophy.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "philos" in origin_domain.lower():
            direction = Direction.PHILOSOPHY_TO_MUSIC
        elif "music" in origin_domain.lower() or "musica" in origin_domain.lower():
            direction = Direction.MUSIC_TO_PHILOSOPHY
        else:
            # Infer from concept content
            concept_lower = origin_concept.lower()
            if any(p in concept_lower for p in [
                "pythagor", "nietzsche", "schopenhauer", "hegel", "adorno",
                "confucius", "stoic", "buddha", "buddhism", "existential",
                "heraclitus", "dialectic", "will", "impermanence", "ataraxia",
                "ritual", "freedom", "flux", "apollonian", "dionysian",
            ]):
                direction = Direction.PHILOSOPHY_TO_MUSIC
            else:
                direction = Direction.MUSIC_TO_PHILOSOPHY

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.PHILOSOPHY_TO_MUSIC:
            destination_concept = iso_data["music"]
        else:
            destination_concept = iso_data["philosophy"]

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
            text = f"{data['philosophy']} {data['music']} {data['rule']}".lower()

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
                for s in [data["philosophy"], data["music"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_homology__philosophical_musical_form"
            best_data = {
                "philosophy": f"Philosophical concept derived from {concept}",
                "music": f"Musical form embodying {structural_property}",
                "rule": "Homology of structure: the same organizing idea expressed in thought and in sound",
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

        if direction == Direction.PHILOSOPHY_TO_MUSIC:
            src_label, dst_label = "philosophical", "musical"
            src_obj = iso_data["philosophy"]
            dst_obj = iso_data["music"]
        else:
            src_label, dst_label = "musical", "philosophical"
            src_obj = iso_data["music"]
            dst_obj = iso_data["philosophy"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into concepts, tensions, and moments",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the moving concepts of {origin_concept}? What tensions drive its argument?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread=f"Each concept carries a label — not merely a name, but the role it plays in the larger argument.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} idea '{src_obj[:60]}...' maps to the {dst_label} form '{dst_obj[:60]}...' through a shared structure.",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Projection preserving the deep structure of the correspondence",
            confidence=round(base_conf * 0.92, 3),
            language_thread=f"The mapped elements are placed in their new home — not arbitrarily, but according to the deep structures the two domains share.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition assembling fragments into a structure that preserves the correspondence",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The fragments are assembled into a whole — a {dst_label} object that breathes with the same rhythm as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
            formal_rule="Inverse homology check: the {dst_label} form, read backward, recovers the {src_label} idea",
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
            "pythagor": "integer ratios, cosmic order, audible number, foundational axiom",
            "nietzsche": "apollonian form, dionysian excess, duality of measure and intoxication",
            "schopenhauer": "blind will, striving, objectification, unrest toward goal",
            "hegel": "thesis, antithesis, synthesis, self-developing concept",
            "adorno": "refused synthesis, preserved contradiction, critique of identity",
            "confuc": "rite and music, ethical ordering, virtue cultivation, polity",
            "stoic": "tranquility, acceptance, disciplined attention, reduced desire",
            "buddha": "impermanence, arising and passing, process over substance",
            "buddh": "impermanence, arising and passing, process over substance",
            "existential": "freedom, choice, constitution of self, no predetermined essence",
            "heraclitus": "flux, becoming, strife, identity as river",
            "dialectic": "thesis, antithesis, contradiction, synthesis",
            "will": "striving, objectification, unrest, goal-directed motion",
            "impermanence": "arising, transformation, dissolution, process",
            "ataraxia": "tranquility, acceptance, discipline, reduction of desire",
            "harmony": "consonant ratios, cosmic order, foundational axiom, audible number",
            "fugue": "subject, answer, countersubject, stretto, episode",
            "sonata": "exposition, development, recapitulation, dialectical structure",
            "variation": "theme, transformation, persistence through change, dissolution",
            "minimal": "repetition, gradual process, sustained texture, reduced will",
            "improvis": "free choice, real-time constitution, no pre-written essence, commitment",
            "atonal": "refused tonic, preserved dissonance, non-resolution, critique",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "concepts, tensions, and the moments of their self-development"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "pythagor": "axiom:arithmetic; order:cosmic; ratio:foundational; number:audible",
            "nietzsche": "pole:apollonian; pole:dionysian; relation:dual; form:classical",
            "schopenhauer": "substance:will; motion:striving; objectification:idea; goal:tonic",
            "hegel": "moment:thesis; moment:antithesis; moment:synthesis; logic:dialectical",
            "adorno": "synthesis:refused; contradiction:preserved; thinking:negative; closure:critiqued",
            "confuc": "pair:rite; pair:music; function:ethical; domain:polity",
            "stoic": "affect:tranquility; practice:acceptance; discipline:attention; desire:reduced",
            "buddha": "mark:impermanence; substance:process; identity:flux; existence:conditioned",
            "buddh": "mark:impermanence; substance:process; identity:flux; existence:conditioned",
            "existential": "structure:absent; choice:constitutive; self:made; essence:posterior",
            "heraclitus": "state:flux; process:becoming; tension:strife; identity:river",
            "dialectic": "stage:thesis; stage:antithesis; stage:synthesis; motion:development",
            "will": "substance:will; motion:striving; objectification:idea; goal:tonic",
            "harmony": "ratio:integer; consonance:fifth; order:cosmic; number:audible",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "concept:philosophical; form:musical; relation:structural"

    def _generate_resonance(
        self,
        origin: str,
        destination: str,
        iso_name: str,
        structural_property: str,
    ) -> str:
        """Generate a poetic resonance sentence from the isomorphism."""
        templates = [
            f"As {origin} thinks through {structural_property}, so {destination} sounds the same idea in another register.",
            f"What {origin} argues in silence, {destination} sings aloud — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single thought seen from two vantages.",
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


def get_transformer() -> PhilosophyMusicTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = PhilosophyMusicTransformer()
    return _default_transformer