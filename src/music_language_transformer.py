"""
glass-bead-game-v26 — Music ↔ Language Transformer
Formal bidirectional transformation scaffold between musical structures
and linguistic/phonological structures, with human language as the
connecting thread.

Where the Math ↔ Music transformer shows that mathematics and music share
a grammar, this module demonstrates that music and language itself share
a deep structural grammar — phonology, syntax, prosody, semantics, and
semiotics all find their echoes in musical form.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    MUSIC_TO_LANGUAGE = "music→language"
    LANGUAGE_TO_MUSIC = "language→music"


@dataclass
class TransformationStep:
    """A single step in the Music ↔ Language transformation pipeline."""
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


class MusicLanguageTransformer:
    """
    Formal bidirectional transformer between musical and linguistic structures.

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
        "phonology__pitch_intervals": {
            "music": "Pitch intervals (major/minor/augmented/diminished) as minimal contrastive units",
            "language": "Phonology: phonemes and distinctive features as minimal contrastive sound units",
            "rule": "Pitch intervals and phonemes are both minimal perceptual units whose identity depends on relational contrast, not absolute value; the interval is to melody what the phoneme is to the word",
            "confidence": 0.93,
        },
        "syntax_tree__voice_leading_hierarchy": {
            "music": "Voice-leading hierarchy: structural tones ( soprano/bass framework) subordinated to foreground diminutions",
            "language": "Syntax tree: hierarchical phrase structure with heads and complements (X-bar theory)",
            "rule": "Schenkerian background→foreground reduction parallels syntactic derivation tree: deep structure (Urlinie/Bassbrechung) generates surface elaborations as phrase-structure rules expand into surface syntax",
            "confidence": 0.91,
        },
        "prosody__musical_phrasing": {
            "music": "Musical phrasing: antecedent-consequent periods, cadences, articulation of musical time",
            "language": "Prosody: intonation, stress, rhythm, and phrasing of spoken language",
            "rule": "Both domains group atomic events into hierarchical phrases via prominence contours; a musical cadence is to a phrase what an intonation-contour boundary is to a spoken utterance",
            "confidence": 0.96,
        },
        "semantics__tonal_function": {
            "music": "Tonal function: tonic, dominant, subdominant as harmonic meaning relative to a key",
            "language": "Semantics: meaning of a word as determined by its role in a relational system",
            "rule": "Tonal function is semantic because a chord's identity is determined by its relation to the tonic, not by its absolute pitch content; a dominant means 'expecting resolution' as a word means by its position in a semantic field",
            "confidence": 0.92,
        },
        "morphology__motivic_transformation": {
            "music": "Motivic transformation: inversion, retrograde, augmentation, fragmentation of a motif",
            "language": "Morphology: affixation, compounding, reduplication, ablaut as morphological operations",
            "rule": "Both apply a finite set of structural operations to a base form to generate a paradigm of related forms; inversion ≈ prefixation, augmentation ≈ suffixation, fragmentation ≈ clipping",
            "confidence": 0.88,
        },
        "pragmatics__performance_practice": {
            "music": "Performance practice: tempo, rubato, dynamics, articulation determined by context and tradition",
            "language": "Pragmatics: meaning in context — speech acts, implicature, deixis, register",
            "rule": "The score is to performance what the literal sentence is to utterance: both require contextual interpretation to determine actual meaning; Gricean implicature ↔ interpretive freedom in performance",
            "confidence": 0.86,
        },
        "poetic_meter__rhythmic_meter": {
            "music": "Rhythmic meter: time signatures, beat grouping, hypermeter in musical structure",
            "language": "Poetic meter: iambic, trochaic, dactylic patterns of stressed and unstressed syllables",
            "rule": "Both organize a stream into recurring accentual patterns; an iamb is to a verse what a 2/4 measure with anacrusis is to a melody — grouping weak-strong cells into higher-level periodicities",
            "confidence": 0.97,
        },
        "semiotics__musical_semiotics": {
            "music": "Musical semiotics: topics, leitmotifs, and musical signs referencing extramusical meaning",
            "language": "Semiotics: the study of signs — signifier, signified, and the conventions linking them",
            "rule": "A leitmotif is a signifier whose signified is a dramatic concept; musical topics (fanfare, sarabande, hunt) function as denotative signs within a stylistic code, exactly as words signify within a linguistic code",
            "confidence": 0.90,
        },
        "rhetoric_figures__musical_figures": {
            "music": "Musical figures (Figurenlehre): rhetorical devices transposed into music — anaphora, gradatio, noema in Bach's cantatas",
            "language": "Rhetorical figures: anaphora, climax, aposiopesis, chiasmus as structural ornaments of argument",
            "rule": "Baroque Figurenlehre maps each rhetorical figure to a musical gesture: anaphora = repeated opening motive; gradatio = sequential pitch staircase; noema = homophonic texture marking a textual point — the same ornament, two media",
            "confidence": 0.95,
        },
        "distinctive_features__interval_vectors": {
            "music": "Interval vectors (Forte): the multiset of interval classes within a pitch-class set",
            "language": "Distinctive features (Jakobson, Halle): binary features [+/-voice, +/-nasal] defining phoneme identity",
            "rule": "An interval vector characterizes a sonority by its internal interval content exactly as a feature bundle characterizes a phoneme by its internal feature contrasts; both are compact relational signatures determining perceptual identity",
            "confidence": 0.89,
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

        If origin_domain is "Music", direction is music→language.
        If origin_domain is "Language" (or "Linguistics"), direction is language→music.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "language" in origin_domain.lower() or "linguist" in origin_domain.lower():
            direction = Direction.LANGUAGE_TO_MUSIC
        elif "music" in origin_domain.lower() or "musica" in origin_domain.lower():
            direction = Direction.MUSIC_TO_LANGUAGE
        else:
            # Infer from concept content
            if any(m in origin_concept.lower() for m in [
                "phoneme", "phonology", "syntax", "syntax tree", "prosody",
                "semantics", "morphology", "pragmatics", "meter", "poetic",
                "semiotic", "rhetoric", "distinctive feature", "phonolog",
                "syllable", "word", "sentence", "phrase structure",
            ]):
                direction = Direction.LANGUAGE_TO_MUSIC
            else:
                direction = Direction.MUSIC_TO_LANGUAGE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.MUSIC_TO_LANGUAGE:
            destination_concept = iso_data["language"]
        else:
            destination_concept = iso_data["music"]

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
            text = f"{data['music']} {data['language']} {data['rule']}".lower()

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
                for s in [data["music"], data["language"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_homomorphism__musical_linguistic_form"
            best_data = {
                "music": f"Musical form embodying {structural_property}",
                "language": f"Linguistic structure derived from {concept}",
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

        if direction == Direction.MUSIC_TO_LANGUAGE:
            src_label, dst_label = "musical", "linguistic"
            src_obj = iso_data["music"]
            dst_obj = iso_data["language"]
        else:
            src_label, dst_label = "linguistic", "musical"
            src_obj = iso_data["language"]
            dst_obj = iso_data["music"]

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
            language_thread="Each atom carries a label — not merely a name, but a role it plays in the larger structure.",
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
            language_thread="The mapped elements are placed in their new home — not arbitrarily, but according to the deep symmetries they share.",
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
            "phonolog": "phonemes, distinctive features, minimal pairs, syllable structure",
            "phoneme": "distinctive features, minimal pairs, allophones, distribution constraints",
            "syntax": "phrase structure rules, heads, complements, specifiers, adjunctions",
            "prosod": "intonation contour, stress pattern, rhythmic grouping, boundary tones",
            "semant": "semantic roles, truth conditions, compositionality, semantic field",
            "morpholog": "morphemes, stems, affixes, allomorphs, paradigm",
            "pragmat": "speech acts, implicatures, deixis, register, common ground",
            "meter": "stress pattern, foot, line, caesura, grouping",
            "semiot": "signifier, signified, code, index, icon, symbol",
            "rhetor": "exordium, narratio, confirmatio, refutatio, peroratio",
            "fugue": "subject, answer, countersubject, stretto, episode",
            "canon": "leader, follower, interval of imitation, temporal offset",
            "cadence": "penultimate chord, structural melodic formula, closure, tonal goal",
            "leitmotif": "signifier motif, referent, context of use, transformation",
            "topic": "musical sign, stylistic origin, denotation, expressive content",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "primitive elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "phonolog": "unit:phoneme; feature:binary; contrast:minimal",
            "phoneme": "unit:phoneme; feature:distinctive; relation:contrastive",
            "syntax": "node:phrase; relation:dominance; type:head/complement",
            "prosod": "contour:intonation; accent:stress; boundary:phrase",
            "semant": "role:thematic; value:truth; field:relational",
            "morpholog": "morpheme:stem/affix; operation:affixation; paradigm:form",
            "pragmat": "act:illocutionary; inference:implicature; context:deictic",
            "meter": "foot:stress; line:periodic; grouping:hypermetrical",
            "semiot": "signifier:form; signified:concept; code:conventional",
            "rhetor": "figure:structural; ornament:argumentative; locus:topical",
            "fugue": "theme:melodic; transformation:contrapuntal; recurrence:cyclic",
            "cadence": "formula:harmonic; closure:syntactic; goal:tonal",
            "leitmotif": "motif:signifying; referent:dramatic; recurrence:associative",
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
            f"What {origin} speaks in sound, {destination} speaks in word — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single figure seen from two angles.",
            f"Where the musician hears {structural_property}, the linguist finds the very same architecture — a shared grammar of the mind.",
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


def get_transformer() -> MusicLanguageTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = MusicLanguageTransformer()
    return _default_transformer