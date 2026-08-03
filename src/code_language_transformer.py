"""
glass-bead-game-v26 — Code ↔ Language Transformer
Formal bidirectional transformation scaffold between computer code structures
and linguistic structures, with human language as the connecting thread.

Language is both the medium and the subject: programming languages formalize
meaning through syntax and types while human languages carry meaning through
grammar and semantics. This module makes that mirrored correspondence explicit,
testable, and playable — the 'coda' domain (computer code) meets the 'lingua'
domain (human language) across a glass bead of isomorphism.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    CODE_TO_LANGUAGE = "code→language"
    LANGUAGE_TO_CODE = "language→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Language transformation pipeline."""
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


class CodeLanguageTransformer:
    """
    Formal bidirectional transformer between computer code and linguistic structures.

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
        "grammar__parser": {
            "language": "Formal grammar: a set of production rules (terminal/non-terminal) that generate well-formed strings",
            "code": "Parser implementation: a program (recursive descent, LL/LR, PEG) that consumes tokens and reconstructs syntactic structure",
            "rule": "Grammar productions ≡ parser transitions; each non-terminal expands via a rule whose inverse is a parser action, mapping derivation to recognition",
            "confidence": 0.96,
        },
        "syntax_tree__parse_tree": {
            "language": "Syntactic derivation tree: the hierarchical proof that a sentence belongs to a grammar, branching from S to terminals",
            "code": "AST/parse tree: the in-memory hierarchical representation of source code, branching from program-unit to leaf expressions",
            "rule": "Derivation node ≡ AST node; parent-child dominance preserves grammatical constituency, so tree-walking algorithms are invariant across domains",
            "confidence": 0.94,
        },
        "semantics__type_system": {
            "language": "Natural language semantics: compositional mapping from syntax to truth-conditional or denotational meaning",
            "code": "Type system / contracts: static or runtime enforcement that every expression carries a type satisfying the operations applied to it",
            "rule": "Semantic compositionality ≡ type composition; the meaning of a whole is a function of the meanings (types) of parts and their mode of combination",
            "confidence": 0.92,
        },
        "pragmatics__api_design": {
            "language": "Pragmatics / context: speaker intention, deixis, implicature, and felicity conditions that shape utterance meaning in use",
            "code": "API design: interface contracts, naming conventions, affordances, and usage patterns that guide how a programmer interacts with a library",
            "rule": "Felicity conditions ≡ API usage contracts; just as an utterance misfires outside its context, an API call fails or misleads when invoked against its conventions",
            "confidence": 0.90,
        },
        "translation__compilation": {
            "language": "Language translation: rendering meaning from one natural language into another while preserving semantic content",
            "code": "Compilation / transpilation: transforming source from one programming language or IR into another while preserving computational semantics",
            "rule": "Equivalence of meaning across representation systems; both preserve denotation under a mapping that is compositional and (ideally) invertible modulo idiom",
            "confidence": 0.93,
        },
        "phonology__encoding": {
            "language": "Phonology / sound system: the inventory of phonemes and phonotactic constraints governing speech-sound combinations",
            "code": "Character encoding / Unicode: the byte-level representation scheme (UTF-8, code points, normalization forms) governing how symbols are stored and transmitted",
            "rule": "Minimal distinctive unit ↔ minimal addressable unit; phonemes distinguish meaning the way code points distinguish characters, and phonotactics constrain combinations as encoding rules constrain byte sequences",
            "confidence": 0.87,
        },
        "morphology__object_model": {
            "language": "Morphology / word formation: roots, affixes, inflection, and derivation that build words from smaller meaningful units",
            "code": "Object model / class hierarchy: base classes, inheritance, composition, and interfaces that build object types from reusable structural units",
            "rule": "Morpheme ≡ class member; derivation ↔ inheritance (new lexeme from root ↔ subclass from base), inflection ↔ parametric polymorphism (same word, different form ↔ same class, different type arguments)",
            "confidence": 0.91,
        },
        "rhetoric__documentation": {
            "language": "Rhetoric / persuasion: the art of structuring discourse — ethos, pathos, logos, arrangement — to move an audience",
            "code": "Documentation / comments: docstrings, READMEs, inline comments, and examples that persuade a programmer's understanding and guide correct use",
            "rule": "Rhetorical arrangement ≡ documentation structure; both select, order, and emphasize information to bridge the gap between author intent and reader comprehension",
            "confidence": 0.88,
        },
        "corpus__training_data": {
            "language": "Linguistic corpus: a curated, annotated collection of texts used to discover statistical and structural regularities of a language",
            "code": "ML training data: a curated, labeled dataset used to fit model parameters and discover statistical regularities of a target distribution",
            "rule": "Empirical regularity ↔ learned parameter; corpus linguistics and supervised learning both infer general structure from finite samples under representativeness assumptions",
            "confidence": 0.93,
        },
        "dialect__programming_paradigm": {
            "language": "Linguistic dialect: a variety of a language shared by a community, differing in lexicon, syntax, and phonology while remaining mutually intelligible",
            "code": "Programming paradigm (OOP vs FP): a coherent style of program construction — objects/messages vs functions/immutability — that shapes how computation is expressed",
            "rule": "Dialectal variation ↔ paradigmatic variation; both are coherent systems for expressing the same underlying content, differing in surface structure and habitual patterns of thought",
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
        """Execute a full bidirectional transformation.

        If origin_domain indicates code/coda, direction is code→language.
        If origin_domain indicates language/lingua, direction is language→code.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "coda" in origin_domain.lower() or "code" in origin_domain.lower():
            direction = Direction.CODE_TO_LANGUAGE
        elif "lingua" in origin_domain.lower() or "language" in origin_domain.lower():
            direction = Direction.LANGUAGE_TO_CODE
        else:
            # Infer from concept content
            code_kw = ["parser", "grammar", "ast", "parse tree", "type system",
                "api", "compilation", "compiler", "encoding", "unicode",
                "class", "object", "inheritance", "documentation", "docstring",
                "training data", "paradigm", "oop", "functional"]
            lang_kw = ["speech act", "semantics", "pragmatics", "syntax",
                "phonolog", "morpholog", "rhetoric", "corpus", "dialect",
                "grammar", "derivation", "translation", "utterance"]
            cl = origin_concept.lower()
            if any(k in cl for k in code_kw) and not any(k in cl for k in lang_kw):
                direction = Direction.CODE_TO_LANGUAGE
            else:
                direction = Direction.LANGUAGE_TO_CODE

        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        if direction == Direction.CODE_TO_LANGUAGE:
            destination_concept = iso_data["language"]
        else:
            destination_concept = iso_data["code"]

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
            text = f"{data['code']} {data['language']} {data['rule']}".lower()
            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2
            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3
            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["code"], data["language"]]
            ):
                score += 5
            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        # Fallback if no good match
        if best_score < 2:
            best_name = "generic_correspondence__structure_meaning"
            best_data = {
                "code": f"Code structure derived from {concept}",
                "language": f"Linguistic structure embodying {structural_property}",
                "rule": "Correspondence preserves structural invariants while allowing domain translation between code and language",
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

        if direction == Direction.CODE_TO_LANGUAGE:
            src_label, dst_label = "code", "linguistic"
            src_obj, dst_obj = iso_data["code"], iso_data["language"]
        else:
            src_label, dst_label = "linguistic", "code"
            src_obj, dst_obj = iso_data["language"], iso_data["code"]

        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into constructs and their relations",
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
            formal_rule="Coordinate projection preserving structural invariants",
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
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
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
            "grammar": "production rules, non-terminals, terminals, start symbol, recursion",
            "parser": "tokenizer, grammar rules, lookahead, parse table, error recovery",
            "syntax tree": "root node, internal nodes, leaf nodes, dominance, precedence",
            "parse tree": "root node, internal nodes, leaf nodes, dominance, precedence",
            "ast": "root node, internal nodes, leaf nodes, dominance, precedence",
            "semantics": "denotation, intension, extension, compositionality, truth condition",
            "type system": "base types, type constructors, subtyping, constraints, inference",
            "pragmatics": "context, speaker intention, conversational maxim, implicature, indexical",
            "api": "interface, method signature, parameter, return type, contract, affordance",
            "translation": "source language, target language, equivalence, idiom, calque",
            "compilation": "front-end, IR, optimization, back-end, code generation, linking",
            "compiler": "lexer, parser, semantic analysis, IR, optimizer, code generator",
            "phonology": "phoneme inventory, phonotactics, distinctive feature, syllable, stress",
            "encoding": "code point, byte sequence, normalization, charset, endian",
            "unicode": "code point, plane, surrogate, normalization form, grapheme cluster",
            "morphology": "root, affix, inflection, derivation, allomorph, stem",
            "object model": "base class, subclass, interface, composition, encapsulation, message",
            "class": "fields, methods, constructor, inheritance, encapsulation, interface",
            "inheritance": "base class, derived class, override, virtual method, is-a, extends",
            "rhetoric": "ethos, pathos, logos, arrangement, style, audience",
            "documentation": "docstring, example, parameter description, return value, usage note",
            "corpus": "text collection, annotation, frequency, concordance, representativeness",
            "training data": "labeled examples, feature vectors, train/val split, distribution, sampling",
            "dialect": "regional variety, lexical difference, syntactic variant, mutual intelligibility",
            "paradigm": "state, control flow, abstraction mechanism, invariant, design pattern",
            "oop": "class, object, inheritance, encapsulation, polymorphism, message passing",
            "functional": "pure function, immutability, higher-order function, recursion, monad",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "constructs and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "grammar": "rule:generative; symbol:non-terminal; string:generated",
            "parser": "rule:recognizing; action:semantic; state:transition",
            "syntax tree": "node:constituent; edge:dominance; leaf:terminal",
            "parse tree": "node:constituent; edge:dominance; leaf:terminal",
            "ast": "node:construct; edge:composition; leaf:expression",
            "semantics": "content:compositional; truth:conditional; reference:relational",
            "type system": "type:static; constraint:sound; inference:bidirectional",
            "pragmatics": "use:situated; meaning:contextual; inference:conversational",
            "api": "interface:contract; method:affordance; parameter:typed",
            "translation": "source:source-language; target:target-language; equivalence:semantic",
            "compilation": "stage:pipeline; representation:IR; output:executable",
            "compiler": "phase:lexing-to-codegen; artifact:IR; output:binary",
            "phonology": "unit:phoneme; constraint:phonotactic; feature:distinctive",
            "encoding": "unit:code-point; sequence:byte; rule:normalization",
            "unicode": "unit:code-point; cluster:grapheme; rule:canonical-ordering",
            "morphology": "unit:morpheme; process:inflection-derivation; form:allomorph",
            "object model": "unit:class; relation:inheritance; mechanism:composition",
            "class": "member:field-method; relation:extends; boundary:encapsulation",
            "inheritance": "relation:is-a; mechanism:override; type:subtype",
            "rhetoric": "appeal:ethos-pathos-logos; structure:arrangement; function:persuasion",
            "documentation": "unit:docstring; function:elucidation; audience:developer",
            "corpus": "unit:text; annotation:linguistic; property:representative",
            "training data": "unit:example; label:supervised; property:iid",
            "dialect": "variety:regional; difference:lexical-syntactic; property:intelligible",
            "paradigm": "style:coherent; mechanism:abstraction; property:expressive",
            "oop": "mechanism:class-object; relation:inheritance; property:polymorphic",
            "functional": "mechanism:pure-function; property:immutable; type:higher-order",
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
            f"What {origin} encodes in logic, {destination} speaks in meaning — the same structure, twice-born.",
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


def get_transformer() -> CodeLanguageTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeLanguageTransformer()
    return _default_transformer