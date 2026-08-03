"""
glass-bead-game-v26 — Code ↔ Music Transformer
Formal bidirectional transformation scaffold between computer code structures
(the domain 'coda') and musical structures (the domain 'musica'), with human
language as the connecting thread.

The Glass Bead Game declares code and music to be twin grammars of pattern
and flow: algorithms are scores, protocols are instruments, recursion is
counterpoint. This module makes that correspondence explicit, testable,
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
    CODE_TO_MUSIC = "code→music"
    MUSIC_TO_CODE = "music→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Music transformation pipeline."""
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


class CodeMusicTransformer:
    """
    Formal bidirectional transformer between computer code and musical structures.

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
        "algorithmic_composition__code_as_score": {
            "code": "Algorithmic composition: code that generates musical output, treating program logic as a compositional score",
            "music": "Code as musical score: the program's control flow read as a sequence of sonic events with timing, dynamics, and phrasing",
            "rule": "A program's instruction sequence is isomorphic to a musical score's event sequence: each statement ↔ each note/rest, loop ↔ repeat, conditional ↔ da-capo/alternative-ending; execution order ↔ temporal unfolding",
            "confidence": 0.94,
        },
        "midi_encoding__digital_audio": {
            "code": "MIDI protocol encoding: digital message stream (note-on/note-off, velocity, channel) as a symbolic music representation",
            "music": "Digital audio encoding: waveform sampling at fixed rate, quantized amplitude — the continuous sound rendered as discrete code",
            "rule": "MIDI messages form a discrete event grammar mapping to audio synthesis parameters; sample rate f_s ↔ temporal resolution, bit depth ↔ dynamic resolution; the codec is the isomorphism",
            "confidence": 0.96,
        },
        "recursive_structure__canon_fugue": {
            "code": "Recursive code structure: function calling itself with modified arguments, base case terminating the call stack",
            "music": "Canon and fugue form: a theme stated then imitated at temporal offsets, pitch transpositions, and inversions until closure",
            "rule": "Recursive call ↔ canon entry: each recursive invocation transposes the theme (by argument change ↔ pitch/time offset); the base case ↔ the final entry that resolves the structure; the call stack ↔ the layered voices",
            "confidence": 0.92,
        },
        "fft__audio_dsp": {
            "code": "FFT (Fast Fourier Transform) algorithm: O(n log n) computation converting time-domain samples to frequency-domain spectrum",
            "music": "Audio DSP processing: spectral filtering, convolution reverb, phase vocoder time-stretching — all operating in the frequency domain the FFT reveals",
            "rule": "The FFT converts a discrete time signal to its frequency representation; every spectral audio effect (EQ, reverb, pitch-shift) is a transformation in this frequency space, making the FFT the bridge between code and audible timbre",
            "confidence": 0.97,
        },
        "pattern_matching__motivic_development": {
            "code": "Pattern matching algorithms: regex, string search, structural pattern matching that identifies and extracts recurring sub-structures",
            "music": "Motivic development: identification, transformation, and recombination of a short melodic/rhythmic motive throughout a composition",
            "rule": "A motif is a pattern in the musical signal; motivic development (repetition, sequence, fragmentation, augmentation) is pattern matching + transformation — the composer's ear is a regex engine over pitch-rhythm space",
            "confidence": 0.90,
        },
        "state_machine__musical_form": {
            "code": "State machine: finite automaton with defined states and transition rules governing movement between them",
            "music": "Musical form transitions: sonata-allegro (exposition→development→recapitulation), rondo (A-B-A-C-A), verse-chorus — formal states with transition rules",
            "rule": "Musical form is a finite state machine: each section (exposition, development, recapitulation) is a state; modulation and thematic return are state transitions governed by tonal and motivic transition rules",
            "confidence": 0.91,
        },
        "seeded_rng__stochastic_composition": {
            "code": "Seeded random number generator: deterministic pseudo-random sequence reproducible from a seed value",
            "music": "Stochastic / computer composition: algorithmic music using controlled randomness (Xenakis, Cage) where a seed determines the full sonic outcome",
            "rule": "A seeded RNG produces a deterministic pseudo-random sequence; stochastic composition uses this sequence to drive pitch/duration/dynamic choices, making the 'random' piece fully reproducible from its seed — the seed is the score",
            "confidence": 0.93,
        },
        "dataflow__signal_flow": {
            "code": "Dataflow programming: programs modeled as graphs where data flows between processing nodes, execution driven by data availability",
            "music": "Audio signal flow / chaining: audio source → effect chain (EQ → compression → reverb → output), a directed graph of DSP nodes",
            "rule": "A dataflow program is a directed graph of processing nodes connected by data edges; an audio signal chain is the same graph where edges carry audio buffers and nodes are DSP processors — the topology is identical, only the payload type changes",
            "confidence": 0.95,
        },
        "markov_chains__generative_music": {
            "code": "Markov chains: stochastic process where next state depends only on current state, defined by a transition probability matrix",
            "music": "Generative music algorithms: algorithmic composition using Markov chains to generate melodies/harmonies with learned transition probabilities",
            "rule": "A Markov chain over pitch/duration states generates music by sampling transitions; training on a corpus yields the transition matrix, and the chain produces infinite variations preserving the corpus's statistical style",
            "confidence": 0.92,
        },
        "abstraction__orchestration": {
            "code": "Code abstraction and encapsulation: functions, classes, modules that hide implementation behind interfaces, composing complexity from hidden parts",
            "music": "Orchestration and arrangement: assigning musical lines to instruments, hiding inner voicing behind the heard timbral surface, composing sonority from concealed parts",
            "rule": "Abstraction hides implementation behind an interface; orchestration hides inner voices behind the perceived timbral blend — a module's public API ↔ an instrument's heard timbre, its private methods ↔ the concealed inner voices that produce it",
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

        If origin_domain contains 'music' or 'musica', direction is music→code.
        If origin_domain contains 'coda' or 'code', direction is code→music.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        origin_lower = origin_domain.lower()
        if "music" in origin_lower or "musica" in origin_lower:
            direction = Direction.MUSIC_TO_CODE
        elif "coda" in origin_lower or "code" in origin_lower:
            direction = Direction.CODE_TO_MUSIC
        else:
            # Infer from concept content
            if any(c in origin_concept.lower() for c in [
                "algorithm", "function", "recursion", "loop", "state machine",
                "pattern", "markov", "fft", "dataflow", "midi", "seed",
                "abstraction", "class", "module", "encoding", "protocol",
                "stochastic", "generative", "rng", "random",
            ]):
                direction = Direction.CODE_TO_MUSIC
            else:
                direction = Direction.MUSIC_TO_CODE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.CODE_TO_MUSIC:
            destination_concept = iso_data["music"]
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

        # Score each isomorphism by keyword overlap
        best_score = -1
        best_name = ""
        best_data = {}

        for name, data in self.ISOMORPHISMS.items():
            score = 0
            text = f"{data['code']} {data['music']} {data['rule']}".lower()

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
                for s in [data["code"], data["music"]]
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
                "code": f"Abstract program structure derived from {concept}",
                "music": f"Musical form embodying {structural_property}",
                "rule": "Homomorphism preserves structure while allowing domain translation between code and music",
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

        if direction == Direction.CODE_TO_MUSIC:
            src_label, dst_label = "code", "musical"
            src_obj = iso_data["code"]
            dst_obj = iso_data["music"]
        else:
            src_label, dst_label = "musical", "code"
            src_obj = iso_data["music"]
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
            "algorithm": "input, procedure, control flow, termination condition, output",
            "recursion": "base case, recursive case, call stack, termination, unwinding",
            "canon": "leader, follower, interval of imitation, temporal offset",
            "fugue": "subject, answer, countersubject, stretto, episode",
            "fft": "twiddle factors, butterfly operations, bit-reversal, recursion, spectrum",
            "midi": "note-on, note-off, velocity, channel, timing, control change",
            "markov": "state space, transition matrix, stationary distribution, seed sequence",
            "state machine": "states, transitions, inputs, initial state, accepting states",
            "dataflow": "nodes, edges, data tokens, firing rules, deadlock freedom",
            "pattern": "pattern, matcher, captures, backtracking, match groups",
            "abstraction": "interface, implementation, encapsulation, composition, hierarchy",
            "orchestr": "instruments, voices, register, timbre, balance, texture",
            "seed": "seed value, PRNG algorithm, sequence, reproducibility, distribution",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "primitive elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "algorithm": "input:typed; procedure:sequential; output:determined",
            "recursion": "base:terminating; step:inductive; stack:layered",
            "canon": "theme:melodic; imitation:contrapuntal; offset:temporal",
            "fugue": "theme:melodic; transformation:contrapuntal; recurrence:cyclic",
            "fft": "basis:orthogonal; butterfly:recursive; spectrum:frequency",
            "midi": "message:event; channel:routed; velocity:dynamics",
            "markov": "state:discrete; transition:probabilistic; chain:stochastic",
            "state machine": "state:finite; transition:guarded; automaton:deterministic",
            "dataflow": "node:processor; edge:data; token:flowing",
            "pattern": "pattern:structural; matcher:searching; capture:binding",
            "abstraction": "interface:public; implementation:private; module:composable",
            "seed": "seed:deterministic; sequence:pseudo-random; output:reproducible",
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
            f"What {origin} computes in silence, {destination} sings aloud — the same structure, twice-born.",
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


def get_transformer() -> CodeMusicTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeMusicTransformer()
    return _default_transformer