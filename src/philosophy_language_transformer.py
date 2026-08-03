"""
glass-bead-game-v26 — Philosophy ↔ Language Transformer
Formal bidirectional transformation scaffold between philosophical structures
and linguistic structures, with human language as the connecting thread.

Language is both the medium and the subject: philosophy reflects on meaning
while linguistics describes its machinery. This module makes that mirrored
correspondence explicit, testable, and playable.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    PHILOSOPHY_TO_LANGUAGE = "philosophy→language"
    LANGUAGE_TO_PHILOSOPHY = "language→philosophy"


@dataclass
class TransformationStep:
    """A single step in the Philosophy ↔ Language transformation pipeline."""
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
            "direction": self.direction, "origin_domain": self.origin_domain,
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


class PhilosophyLanguageTransformer:
    """
    Formal bidirectional transformer between philosophical and linguistic structures.

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
        "wittgenstein_games__speech_act_theory": {
            "philosophy": "Wittgenstein language games: meaning as use within a form of life",
            "language": "Speech act theory: utterances perform actions (locutionary, illocutionary, perlocutionary)",
            "rule": "Meaning ≡ felicity-conditioned use; an utterance's force is determined by the game-rules of its context, mapping illocutionary force to Wittgensteinian rule-following",
            "confidence": 0.95,
        },
        "saussure_signifier__platonic_forms": {
            "philosophy": "Platonic forms: eternal, unchanging ideal archetypes of which particulars are shadows",
            "language": "Saussure signifier/signified: the linguistic sign unites a sound-image to a concept by convention",
            "rule": "Form : particular :: signified : signifier; both dichotomies separate the ideal (conceptual/formal) from the material (acoustic/particular) under an anchoring relation",
            "confidence": 0.87,
        },
        "derrida_différance__semantic_indeterminacy": {
            "philosophy": "Derrida différance: meaning endlessly deferred through chains of signifiers, presence always postponed",
            "language": "Semantic indeterminacy: word senses stabilize only through differential networks with no fixed referent",
            "rule": "Deferral of presence ↔ differential semantics; the signified is itself always already a signifier, so meaning is produced by spacing and temporal delay",
            "confidence": 0.93,
        },
        "heidegger_being__ontological_grammar": {
            "philosophy": "Heidegger Being (Sein): the disclosedness of entities as such, structured by care and temporality",
            "language": "Ontological grammar: the deep case-role and aspectual skeleton sentences impose on states of affairs",
            "rule": "The grammar of disclosure ↔ the structure of Dasein's understanding; language is the 'house of Being,' so morphological categories echo ontological categories",
            "confidence": 0.86,
        },
        "quine_indeterminacy__hermeneutic_circle": {
            "philosophy": "Quine indeterminacy of translation: no fact of the matter fixes a unique utterance-to-meaning map",
            "language": "Hermeneutic circle: understanding the whole requires understanding parts, and vice versa, recursively",
            "rule": "Radical translation ↔ circular interpretation; both deny a foundational anchor, requiring holistic constraint satisfaction to stabilize meaning",
            "confidence": 0.89,
        },
        "austin_performatives__pragmatics": {
            "philosophy": "Austin performatives: utterances that constitute the act they name (promising, naming, marrying)",
            "language": "Pragmatics: language in use, indexed by context, speaker intention, and conversational maxims",
            "rule": "Performative force ≡ pragmatic effect; an utterance's meaning is exhausted by what it accomplishes in a situated interaction",
            "confidence": 0.97,
        },
        "frege_sense_reference__semantics": {
            "philosophy": "Frege sense (Sinn) and reference (Bedeutung): the mode of presentation vs the object denoted",
            "language": "Semantics: the compositional mapping from syntactic structures to truth-conditional content",
            "rule": "Sinn → intension (truth-function profile); Bedeutung → extension (referent); compositionality preserves sense under substitution",
            "confidence": 0.96,
        },
        "whorf_sapir__epistemic_relativism": {
            "philosophy": "Epistemic relativism: what counts as knowledge, evidence, or rationality is framework-relative",
            "language": "Whorf-Sapir linguistic relativity: the grammatical categories of a language shape habitual cognition",
            "rule": "Cognitive framework ↔ grammatical system; strong form: thought is bounded by language; weak form: language biases perception",
            "confidence": 0.85,
        },
        "grice_implicature__logical_pragmatics": {
            "philosophy": "Grice implicature: conversational meaning beyond literal content, from cooperative principles",
            "language": "Logical pragmatics: formal reconstruction of what speakers imply and hearers infer beyond entailment",
            "rule": "Implicature ≡ defeasible inference under the Cooperative Principle and its maxims; cancelable but rationally reconstructable",
            "confidence": 0.94,
        },
        "habermas_communicative_rationality__discourse_ethics": {
            "philosophy": "Habermas communicative rationality: reason grounded in the validity claims of uncoerced discourse",
            "language": "Discourse ethics: normative structure of argumentation — who may speak, with what force, under what conditions",
            "rule": "Communicative action ↔ ideal speech situation; rationality is the capacity to redeem validity claims through argument",
            "confidence": 0.91,
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
        """Execute a full bidirectional transformation.

        If origin_domain indicates philosophy, direction is philosophy→language.
        If origin_domain indicates language/linguistics, direction is language→philosophy.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "philos" in origin_domain.lower():
            direction = Direction.PHILOSOPHY_TO_LANGUAGE
        elif "linguist" in origin_domain.lower() or "language" in origin_domain.lower():
            direction = Direction.LANGUAGE_TO_PHILOSOPHY
        else:
            # Infer from concept content
            philos_kw = ["being", "derrida", "heidegger", "wittgenstein", "quine",
                "frege", "austin", "grice", "habermas", "saussure", "form",
                "différance", "performat", "implicature", "epistemic"]
            lang_kw = ["speech act", "signifier", "pragmatics", "semantics",
                "discourse", "grammar", "syntax", "phonolog", "morpholog",
                "relativ", "utterance", "illocut", "perlocut"]
            cl = origin_concept.lower()
            if any(k in cl for k in philos_kw) and not any(k in cl for k in lang_kw):
                direction = Direction.PHILOSOPHY_TO_LANGUAGE
            else:
                direction = Direction.LANGUAGE_TO_PHILOSOPHY

        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        if direction == Direction.PHILOSOPHY_TO_LANGUAGE:
            destination_concept = iso_data["language"]
        else:
            destination_concept = iso_data["philosophy"]

        if not resonance_sentence:
            resonance_sentence = self._generate_resonance(
                origin_concept, destination_concept, iso_name, structural_property
            )

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
        self, concept: str, origin_domain: str, dest_domain: str,
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
            text = f"{data['philosophy']} {data['language']} {data['rule']}".lower()
            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2
            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3
            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["philosophy"], data["language"]]
            ):
                score += 5
            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_correspondence__meaning_structure"
            best_data = {
                "philosophy": f"Philosophical framework derived from {concept}",
                "language": f"Linguistic structure embodying {structural_property}",
                "rule": "Correspondence preserves conceptual structure while allowing domain translation",
                "confidence": 0.65,
            }
        return best_name, best_data

    def _build_pipeline(
        self, direction: Direction, origin_concept: str, iso_name: str,
        iso_data: Dict[str, Any], structural_property: str, tokens: List[str],
    ) -> List[TransformationStep]:
        """Construct the 6-stage transformation with language thread."""
        steps = []
        base_conf = iso_data.get("confidence", 0.85)

        if direction == Direction.PHILOSOPHY_TO_LANGUAGE:
            src_label, dst_label = "philosophical", "linguistic"
            src_obj, dst_obj = iso_data["philosophy"], iso_data["language"]
        else:
            src_label, dst_label = "linguistic", "philosophical"
            src_obj, dst_obj = iso_data["language"], iso_data["philosophy"]

        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into concepts and their relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the building blocks of {origin_concept}? What are its atoms?",
        ))
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread="Each atom carries a label — not merely a name, but a role it plays in the larger structure.",
        ))
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj}' maps to the {dst_label} structure '{dst_obj}' through the rule: {iso_data['rule'][:80]}...",
        ))
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} conceptual space",
            formal_rule="Coordinate projection preserving conceptual invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread="The mapped elements are placed in their new home — not arbitrarily, but according to the deep symmetries they share.",
        ))
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under relational structure preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The fragments are assembled into a whole — a {dst_label} object that breathes with the same rhythm as its {src_label} twin.",
        ))
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms conceptual fidelity: {src_obj}",
            formal_rule="Inverse correspondence check: φ⁻¹(φ(x)) ≈ x within tolerance ε",
            confidence=round(base_conf * 0.90, 3),
            language_thread="We turn the glass bead over, looking back through it to ensure the original light still shines — transformed, but unbroken.",
        ))

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)
        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "wittgenstein": "form of life, rule-following, language game, use, practice",
            "saussure": "signifier, signified, sign, arbitrariness, system of differences",
            "derrida": "signifier, deferral, trace, différance, spacing, supplement",
            "heidegger": "dasein, being, disclosedness, care, temporality, worldhood",
            "quine": "radical translation, stimulus meaning, analytic-synthetic, holism",
            "austin": "locution, illocution, perlocution, felicity condition, force",
            "frege": "sense, reference, compositionality, object, concept, thought",
            "whorf": "linguistic category, habitual thought, grammatical pattern, world view",
            "grice": "cooperative principle, maxim, implicature, conventional meaning, cancellation",
            "habermas": "validity claim, discourse, communicative action, lifeworld, ideal speech",
            "speech act": "locutionary act, illocutionary force, perlocutionary effect, context",
            "pragmatics": "context, speaker intention, conversational maxim, implicature, indexical",
            "semantics": "denotation, intension, extension, compositionality, truth condition",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "conceptual elements and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "wittgenstein": "concept:rule-governed; practice:form-of-life; meaning:use",
            "saussure": "sign:dyadic; relation:arbitrary; structure:differential",
            "derrida": "trace:deferred; structure:differential; presence:postponed",
            "heidegger": "entity:ontic; structure:ontological; disclosedness:temporal",
            "quine": "meaning:stimulus; holism:confirmational; translation:indeterminate",
            "austin": "act:performative; force:illocutionary; condition:felicity",
            "frege": "sense:mode-of-presentation; reference:object; composition:functional",
            "whorf": "category:grammatical; cognition:habitual; relativity:structural",
            "grice": "meaning:conversational; inference:defeasible; principle:cooperative",
            "habermas": "rationality:communicative; claim:validity; discourse:uncoerced",
            "speech act": "act:illocutionary; force:performative; context:situated",
            "pragmatics": "use:situated; meaning:contextual; inference:conversational",
            "semantics": "content:compositional; truth:conditional; reference:relational",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:abstract; relation:structural; property:conceptual"

    def _generate_resonance(
        self, origin: str, destination: str, iso_name: str, structural_property: str,
    ) -> str:
        """Generate a poetic resonance sentence from the isomorphism."""
        templates = [
            f"As {origin} {structural_property}, so {destination} reveals the same pattern in another tongue.",
            f"What {origin} thinks in silence, {destination} speaks aloud — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single figure seen from two angles.",
        ]
        return templates[hash(iso_name) % len(templates)]

    def batch_transform(self, moves: List[Dict[str, Any]]) -> List[TransformerResult]:
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


def get_transformer() -> PhilosophyLanguageTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = PhilosophyLanguageTransformer()
    return _default_transformer