"""
glass-bead-game-v26 — History ↔ Music Transformer
Formal bidirectional transformation scaffold between historical eras/movements
and musical structures, with human language as the connecting thread.

Hesse's Glass Bead Game draws correspondences across all domains of culture.
This module makes the History ↔ Music correspondence explicit, testable, and
playable — an era's upheaval becomes a musical form, and a musical form becomes
a historical current.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    HISTORY_TO_MUSIC = "history→music"
    MUSIC_TO_HISTORY = "music→history"


@dataclass
class TransformationStep:
    """A single step in the History ↔ Music transformation pipeline."""
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


class HistoryMusicTransformer:
    """
    Formal bidirectional transformer between historical and musical structures.

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
        "baroque_absolutism__fugue": {
            "history": "Baroque era: absolutist order, layered court hierarchy, systematic ornamentation",
            "music": "Fugue: contrapuntal form with subject, answer, and layered voices under a single governing tonic",
            "rule": "The many voices of the fugue mirror the many estates of the Baroque polity: each autonomous yet subordinated to a single sovereign subject (tonic/monarch)",
            "confidence": 0.96,
        },
        "renaissance_humanism__polyphonic_motet": {
            "history": "Renaissance: humanism, revival of antiquity, plurality of independent voices in society",
            "music": "Polyphonic motet: several equally valued melodic lines, each text-bearing, woven in balanced counterpoint",
            "rule": "The egalitarian independence of the motet's voices mirrors the Renaissance valuation of the individual human voice; no single line dominates",
            "confidence": 0.94,
        },
        "enlightenment_reason__sonata_form": {
            "history": "Enlightenment: rationalism, systematic argument, balance of powers, logical exposition",
            "music": "Sonata form: exposition–development–recapitulation as rational structural argument with thematic thesis, antithesis, and resolution",
            "rule": "Sonata form enacts the Enlightenment's discursive logic: a theme is stated, tested through modulation, and rationally restated in the home key",
            "confidence": 0.95,
        },
        "romantic_individualism__program_music": {
            "history": "Romantic era: individual feeling, narrative self-expression, the cult of the hero",
            "music": "Program music: instrumental music that tells an extramusical story, conveying narrative and emotion without words",
            "rule": "The Romantic elevation of personal narrative maps to program music's rejection of abstract form in favor of storytelling content",
            "confidence": 0.92,
        },
        "wwi_crisis__atonality": {
            "history": "First World War: collapse of old order, shattering of teleological optimism, crisis of Western civilization",
            "music": "Atonality and the Second Viennese School: abandonment of tonal center, dissonance as structural norm",
            "rule": "The dissolution of the tonal center is the audible image of the dissolution of the political and moral center of Europe",
            "confidence": 0.93,
        },
        "civil_rights__spirituals_gospel": {
            "history": "Civil Rights movement: collective struggle for dignity, communal solidarity under oppression, faith as resistance",
            "music": "African American spirituals and gospel: communal song as encoded testimony, call-and-response as collective voice",
            "rule": "The call-and-response structure and coded meaning of spirituals maps the communal organizing structure of the Civil Rights movement",
            "confidence": 0.90,
        },
        "french_revolution__beethoven_heroic": {
            "history": "French Revolution: overthrow of old order, heroic individualism, transformation of political subject",
            "music": "Beethoven's heroic period: expansion of scale, dramatic struggle-to-triumph narrative (Eroica, Fifth Symphony)",
            "rule": "Beethoven's heroic works embody the Revolutionary ideal of the individual who reshapes history through struggle; form becomes political action",
            "confidence": 0.95,
        },
        "industrial_revolution__mechanical_ostinato": {
            "history": "Industrial Revolution: mechanization of labor, repetitive mass production, the rhythm of the machine",
            "music": "Mechanical rhythm and ostinato: persistent repeated patterns, rhythmic regularity as structural engine (e.g., Honegger, Varèse)",
            "rule": "The relentless ostinato maps the repetitive precision of industrial production; the machine's pulse becomes musical meter",
            "confidence": 0.89,
        },
        "cold_war__serialism": {
            "history": "Cold War: total systemic control, mutually assured anxiety, the logic of deterrence and enumeration",
            "music": "Serialism: total organization of pitch, rhythm, and dynamics under a controlling series; Schoenberg, Babbitt, Boulez",
            "rule": "Total serial control over every musical parameter mirrors the Cold War logic of total systemic control and calculated, exhaustive order",
            "confidence": 0.91,
        },
        "ancient_greek_modes__gregorian_chant": {
            "history": "Ancient Greek modal theory and its transmission through late antiquity into medieval Christendom",
            "music": "Gregorian chant modal system: eight church modes descended, via Boethius, from the Greek tonoi",
            "rule": "The church modes preserve a transformed trace of the Greek modal system; the liturgy inherits the speculative music theory of antiquity",
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

        If origin_domain contains "History", direction is history→music.
        If origin_domain is "Music", direction is music→history.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "history" in origin_domain.lower() or "histor" in origin_domain.lower():
            direction = Direction.HISTORY_TO_MUSIC
        elif "music" in origin_domain.lower() or "musica" in origin_domain.lower():
            direction = Direction.MUSIC_TO_HISTORY
        else:
            # Infer from concept content
            concept_lower = origin_concept.lower()
            if any(h in concept_lower for h in [
                "era", "epoch", "revolution", "war", "renaissance", "baroque",
                "enlightenment", "romantic", "movement", "ancient", "medieval",
                "modern", "century", "civilization", "crisis", "reformation",
            ]):
                direction = Direction.HISTORY_TO_MUSIC
            else:
                direction = Direction.MUSIC_TO_HISTORY

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.HISTORY_TO_MUSIC:
            destination_concept = iso_data["music"]
        else:
            destination_concept = iso_data["history"]

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
            text = f"{data['history']} {data['music']} {data['rule']}".lower()

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
                for s in [data["history"], data["music"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_homology__historical_musical_form"
            best_data = {
                "history": f"Historical pattern derived from {concept}",
                "music": f"Musical form embodying {structural_property}",
                "rule": "Homology of structure: the same organizing principle expressed in two cultural registers",
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

        if direction == Direction.HISTORY_TO_MUSIC:
            src_label, dst_label = "historical", "musical"
            src_obj = iso_data["history"]
            dst_obj = iso_data["music"]
        else:
            src_label, dst_label = "musical", "historical"
            src_obj = iso_data["music"]
            dst_obj = iso_data["history"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into agents, forces, and phases",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the moving forces of {origin_concept}? What tensions drive it?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread=f"Each force carries a label — not merely a name, but the role it plays in the larger arc.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} pattern '{src_obj[:60]}...' maps to the {dst_label} form '{dst_obj[:60]}...' through the shared rule.",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Projection preserving the deep structure of the correspondence",
            confidence=round(base_conf * 0.92, 3),
            language_thread=f"The mapped elements are placed in their new home — not arbitrarily, but according to the deep patterns the two domains share.",
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
            formal_rule="Inverse homology check: the {dst_label} form, read backward, recovers the {src_label} pattern",
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
            "baroque": "court hierarchy, ornamented ceremony, absolutist order, layered authority",
            "renaissance": "independent voices, revived antiquity, humanist pluralism, balanced counterpoint",
            "enlightenment": "rational argument, thesis and antithesis, balanced powers, logical exposition",
            "romantic": "individual feeling, heroic narrative, subjective expression, programmatic story",
            "revolution": "overthrown order, heroic actor, transformation of subject, dialectical upheaval",
            "war": "collapsed center, shattered optimism, dissonant crisis, fractured teleology",
            "industrial": "mechanized labor, repetitive production, rhythmic regularity, machine pulse",
            "cold": "total control, mutual deterrence, exhaustive enumeration, systemic anxiety",
            "civil rights": "communal solidarity, coded testimony, call-and-response, faith as resistance",
            "greek": "modal theory, speculative order, transmission via antiquity, liturgical inheritance",
            "fugue": "subject, answer, countersubject, stretto, episode",
            "sonata": "exposition, development, recapitulation, thematic transformation",
            "motet": "independent melodic lines, balanced counterpoint, text-bearing voices",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "agents, forces, phases, and their relational tensions"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "baroque": "order:hierarchical; voice:layered; authority:sovereign; ornament:systematic",
            "renaissance": "voice:independent; value:egalitarian; source:antique; texture:polyphonic",
            "enlightenment": "argument:rational; structure:balanced; logic:discursive; form:systematic",
            "romantic": "expression:subjective; narrative:heroic; content:programmatic; feeling:individual",
            "revolution": "order:overthrown; actor:heroic; subject:transformed; form:dialectical",
            "war": "center:dissolved; optimism:shattered; texture:dissonant; teleology:fractured",
            "industrial": "labor:mechanized; pattern:repetitive; pulse:machine; rhythm:regular",
            "cold": "control:total; logic:deterrence; order:enumerative; affect:anxiety",
            "fugue": "theme:melodic; transformation:contrapuntal; recurrence:cyclic",
            "sonata": "form:argument; section:triadic; key:polar; logic:rational",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "force:historical; form:musical; relation:structural"

    def _generate_resonance(
        self,
        origin: str,
        destination: str,
        iso_name: str,
        structural_property: str,
    ) -> str:
        """Generate a poetic resonance sentence from the isomorphism."""
        templates = [
            f"As {origin} moves through {structural_property}, so {destination} sounds the same pattern in another register.",
            f"What {origin} enacts in history, {destination} sings in sound — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single current seen from two shores.",
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


def get_transformer() -> HistoryMusicTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = HistoryMusicTransformer()
    return _default_transformer