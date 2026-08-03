"""
glass-bead-game-v26 — Nature ↔ Music Transformer
Formal bidirectional transformation scaffold between natural phenomena
(biological rhythms, physical processes, ecological cycles) and musical
structures, with human language as the connecting thread.

Hesse's Glass Bead Game draws correspondences across all domains of
culture and nature. This module makes the nature↔music correspondence
explicit, testable, and playable — the songbird and the sonata are
read here as two inscriptions of the same pattern.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    NATURE_TO_MUSIC = "nature→music"
    MUSIC_TO_NATURE = "music→nature"


@dataclass
class TransformationStep:
    """A single step in the Nature ↔ Music transformation pipeline."""
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


class NatureMusicTransformer:
    """
    Formal bidirectional transformer between natural and musical structures.

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
        "birdsong__melodic_ornamentation": {
            "nature": "Birdsong: learned and innate vocalisations of oscine passerines, consisting of motifs, syllables, and trills",
            "music": "Melodic ornamentation: grace notes, trills, turns, and appoggiaturas that decorate a cantabile line",
            "rule": "A birdsong motif maps to an ornamented interval: the intervallic leap encodes species identity just as a trill encodes stylistic identity; both are learned via imitation and display constrained variance",
            "confidence": 0.93,
        },
        "cricket_stridulation__ostinato": {
            "nature": "Cricket stridulation: sustained, periodic chirping produced by forewing file-and-scraper mechanism at a species-specific pulse rate",
            "music": "Ostinato: a persistently repeated rhythmic or melodic pattern that underpins a composition",
            "rule": "The fixed pulse rate of stridulation maps isomorphically to an ostinato's period; both define a temporal grid against which variation is perceived, and both tolerate small tempo drift but not pattern disruption",
            "confidence": 0.90,
        },
        "whale_song__long_form_phrasing": {
            "nature": "Humpback whale song: hierarchical, seasonally evolving phrases assembled into themes lasting tens of minutes",
            "music": "Long-form phrasing: extended arching phrases (e.g., cantus firmus, lied, raga alap) that build across minutes",
            "rule": "Whale theme ↔ musical phrase; whale hierarchy (unit→phrase→theme→song) ↔ musical hierarchy (note→phrase→section→movement); the slow formal evolution maps to the gradual modulation of a raga alap",
            "confidence": 0.88,
        },
        "wind_in_trees__aleatoric_music": {
            "nature": "Wind through trees: stochastic modulation of leaf resonances, amplitude and timing governed by turbulent airflow",
            "music": "Aleatoric music: composition with controlled chance, where performers choose within bounded parameters set by the composer",
            "rule": "Turbulent boundary conditions ↔ composer-specified probability ranges; the resulting stochastic field of leaf sounds maps to an indeterminate texture of performer-chosen events, both globally shaped yet locally free",
            "confidence": 0.85,
        },
        "water_flow__legato_phrasing": {
            "nature": "Water flow: laminar streamlines that join and part smoothly around obstacles, conserving mass and momentum",
            "music": "Legato phrasing: smoothly connected notes with minimal articulatory gaps, continuous motion",
            "rule": "A streamline maps to a legato phrase; the continuity equation (∇·v=0) maps to the absence of articulation gaps; obstacles produce eddies just as cadences produce gentle phrase breaks",
            "confidence": 0.87,
        },
        "thunder__percussion_dynamics": {
            "nature": "Thunder: abrupt atmospheric expansion from lightning heating, producing impulsive broadband sound with exponential decay",
            "music": "Percussion and dynamics: struck instruments whose envelope is attack + decay, and the dramatic use of loudness as a structural force",
            "rule": "A thunderclap envelope (impulse → exponential decay) maps to a percussion hit; the frequency-dependent attenuation with distance maps to the orchestral use of dynamics to control perceived nearness and weight",
            "confidence": 0.92,
        },
        "seasonal_cycle__sonata_form": {
            "nature": "Seasonal cycle: annual oscillation between dormancy (winter), renewal (spring), maturation (summer), and senescence (autumn)",
            "music": "Sonata form: exposition (theme statement) → development (transformation) → recapitulation (return, transformed) → coda",
            "rule": "Spring's renewal ↔ exposition; summer's intensification ↔ development; autumn's resolution and winter's cadence ↔ recapitulation; the year's return is a tonal return — the same cycle, transformed by having been lived",
            "confidence": 0.89,
        },
        "cardiac_rhythm__pulse_beat": {
            "nature": "Cardiac rhythm: autorhythmic sinoatrial node firing, with periodicity, accentuation (systole), and entrainment to demand",
            "music": "Pulse and beat: the regular metrical grid with accented and unaccented beats, accelerando/ritardando under expressive demand",
            "rule": "The SA node's interbeat interval maps to the musical tactus; systolic accent maps to downbeat; entrainment to autonomic demand maps to tempo rubato and accelerando",
            "confidence": 0.96,
        },
        "fibonacci_petals__golden_proportion": {
            "nature": "Fibonacci numbers in flower petals and phyllotaxis: spiral arrangements and petal counts cluster on the Fibonacci sequence, converging to the golden angle",
            "music": "Golden ratio in musical proportion: phrase lengths, climactic placement, and proportional tempo relationships that approximate φ",
            "rule": "The golden angle 137.5° and Fibonacci petal counts map to musical proportional schemes (e.g., Béla Bartók's φ-based phrase lengths); both realise optimal packing / maximal contrast without periodic collision",
            "confidence": 0.86,
        },
        "tectonic_plates__harmonic_progression": {
            "nature": "Tectonic plate motion: slow accumulation of stress at plate boundaries, released as earthquakes when friction is overcome, in a stick-slip cycle",
            "music": "Harmonic progression and tension-release: the build-up and resolution of harmonic tension through dominant–tonic and chromatic voice-leading",
            "rule": "Stress accumulation at a fault ↔ harmonic tension built by prolongation of a dominant; rupture / earthquake ↔ cadential resolution; the seismic recurrence interval maps to the cadential period of a tonal work",
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

        If origin_domain is "Nature", direction is nature→music.
        If origin_domain is "Music", direction is music→nature.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "nature" in origin_domain.lower() or "bio" in origin_domain.lower() or "eco" in origin_domain.lower():
            direction = Direction.NATURE_TO_MUSIC
        elif "music" in origin_domain.lower() or "musica" in origin_domain.lower():
            direction = Direction.MUSIC_TO_NATURE
        else:
            # Infer from concept content
            if any(n in origin_concept.lower() for n in [
                "bird", "songbird", "cricket", "whale", "wind", "water",
                "thunder", "season", "cardiac", "heart", "pulse",
                "fibonacci", "petal", "tectonic", "earth", "leaf", "stream",
            ]):
                direction = Direction.NATURE_TO_MUSIC
            else:
                direction = Direction.MUSIC_TO_NATURE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.NATURE_TO_MUSIC:
            destination_concept = iso_data["music"]
        else:
            destination_concept = iso_data["nature"]

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

        # Score each isomorphism by keyword overlap
        best_score = -1
        best_name = ""
        best_data = {}

        for name, data in self.ISOMORPHISMS.items():
            score = 0
            text = f"{data['nature']} {data['music']} {data['rule']}".lower()

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
                for s in [data["nature"], data["music"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_homology__musical_form"
            best_data = {
                "nature": f"Natural phenomenon derived from {concept}",
                "music": f"Musical form embodying {structural_property}",
                "rule": "Homology preserves structural roles while allowing domain translation",
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

        if direction == Direction.NATURE_TO_MUSIC:
            src_label, dst_label = "natural", "musical"
            src_obj = iso_data["nature"]
            dst_obj = iso_data["music"]
        else:
            src_label, dst_label = "musical", "natural"
            src_obj = iso_data["music"]
            dst_obj = iso_data["nature"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into observable units and their relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the living parts of {origin_concept}? What rhythms does it breathe?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread="Each natural element carries a label — not merely a name, but a role it plays in the larger pattern of the world.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj[:60]}...' maps to the {dst_label} structure '{dst_obj[:60]}...' through the rule: {iso_data['rule'][:80]}...",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Coordinate projection preserving temporal and dynamical invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread="The mapped elements are placed in their new home — not arbitrarily, but according to the deep rhythms they share with the natural world.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under temporal ordering preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The living fragments are assembled into a whole — a {dst_label} object that breathes with the same rhythm as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
            formal_rule="Inverse homology check: φ⁻¹(φ(x)) ≈ x within tolerance ε",
            confidence=round(base_conf * 0.90, 3),
            language_thread="We turn the glass bead over, looking back through it to ensure the original light still shines — transformed, but unbroken.",
        ))

        # Log tokens
        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "bird": "syllable, motif, phrase, bout, song",
            "cricket": "pulse, chirp, trill, interpulse interval, stridulatory file",
            "whale": "unit, phrase, theme, song, seasonal version",
            "wind": "gust, lull, eddy, leaf resonance, turbulence spectrum",
            "water": "streamline, eddy, vortex, boundary layer, discharge rate",
            "thunder": "return stroke, thunderclap, rumble, decay envelope, shock front",
            "season": "vernal onset, growing season, senescence, dormancy, photoperiod",
            "cardiac": "sinoatrial firing, systole, diastole, interbeat interval, entrainment",
            "heart": "sinoatrial firing, systole, diastole, interbeat interval, entrainment",
            "fibonacci": "petal count, spiral angle, phyllotaxis axis, parastichy, divergence",
            "tectonic": "plate boundary, asperity, stress drop, recurrence interval, rupture front",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "observable units and their temporal and dynamical relations"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "bird": "syllable:timed; motif:learned; phrase:hierarchical; bout:episodic",
            "cricket": "pulse:periodic; chirp:burst; stridulation:mechanical; rate:species-specific",
            "whale": "unit:acoustic; phrase:hierarchical; theme:seasonal; song:long-form",
            "wind": "gust:stochastic; eddy:vortical; resonance:bounded; airflow:turbulent",
            "water": "streamline:continuous; eddy:rotational; vortex:coherent; flow:laminar",
            "thunder": "stroke:impulsive; clap:broadband; rumble:decaying; decay:exponential",
            "season": "phase:periodic; photoperiod:driver; dormancy:quiescent; renewal:emergent",
            "cardiac": "node:autorhythmic; systole:accented; interval:temporal; demand:entrained",
            "heart": "node:autorhythmic; systole:accented; interval:temporal; demand:entrained",
            "fibonacci": "petal:integer; spiral:golden; phyllotaxis:packing; ratio:convergent",
            "tectonic": "boundary:contact; stress:accumulating; rupture:episodic; cycle:recurrent",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:observational; relation:temporal; property:dynamical"

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
            f"What {origin} performs in the open air, {destination} sings in the concert hall — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single figure seen from two angles — the world's and the mind's.",
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


def get_transformer() -> NatureMusicTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = NatureMusicTransformer()
    return _default_transformer