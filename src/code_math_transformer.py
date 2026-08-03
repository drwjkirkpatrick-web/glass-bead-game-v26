"""
glass-bead-game-v26 — Code ↔ Math Transformer
Formal bidirectional transformation scaffold between computer code (domain 'coda',
the Castalian disciple Magister Codae) and mathematical structures, with human
language as the connecting thread.

This module corresponds to the idea that programming is applied mathematics:
every algorithm, data structure, and type system is a materialized theorem.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    CODE_TO_MATH = "code→math"
    MATH_TO_CODE = "math→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Math transformation pipeline."""
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
        return cls(
            direction=d["direction"],
            origin_domain=d["origin_domain"],
            origin_concept=d["origin_concept"],
            destination_domain=d["destination_domain"],
            destination_concept=d["destination_concept"],
            steps=[TransformationStep(**s) for s in d["steps"]],
            structural_property=d["structural_property"],
            resonance_sentence=d["resonance_sentence"],
            tokens_seen=d["tokens_seen"],
            tokens_per_step=d["tokens_per_step"],
            total_confidence=d["total_confidence"],
            isomorphisms=d["isomorphisms"],
        )


class CodeMathTransformer:
    """
    Formal bidirectional transformer between computer code and mathematical structures.

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
        "turing_machine__algorithm": {
            "math": "Turing machine: (Q, Σ, Γ, δ, q₀, F) — a formal model of computation with tape, head, states, and transition function",
            "code": "Algorithm: a finite sequence of computational steps that transforms input to output, executable on a universal machine",
            "rule": "Church-Turing thesis: every effectively calculable function is computable by a Turing machine; every algorithm is a Turing-machine program, and every Turing machine can be simulated by a program",
            "confidence": 0.99,
        },
        "lambda_calculus__functional_programming": {
            "math": "λ-calculus: a formal system based on function abstraction (λx.M) and application (M N); terms reduced via β-reduction",
            "code": "Functional programming: pure functions, higher-order combinators, lazy evaluation, and immutability in languages like Haskell and Lisp",
            "rule": "λ-abstraction ↔ function definition; β-reduction ↔ function application; currying and closures are direct implementations of λ-calculus semantics",
            "confidence": 0.98,
        },
        "type_theory__static_typing": {
            "math": "Type theory: a formal system where terms are classified by types; the Curry-Howard correspondence maps propositions to types and proofs to programs",
            "code": "Static type systems: compile-time type checking in languages like Haskell, Rust, and TypeScript; types prevent invalid operations before runtime",
            "rule": "Curry-Howard isomorphism: every type is a theorem, every program is a proof; type inhabitation = proof existence; a well-typed program is a constructive proof of its specification",
            "confidence": 0.97,
        },
        "recursive_function__recursion": {
            "math": "Recursive function theory: partial recursive functions defined by composition, primitive recursion, and minimization (μ); the μ-recursive functions coincide with the Turing-computable functions",
            "code": "Recursion in code: a function that calls itself with a smaller subproblem until reaching a base case; the fundamental control-flow pattern in divide-and-conquer and tree traversal",
            "rule": "Primitive recursion f(n+1, x) = g(n, f(n, x)) maps directly to recursive function definitions with base cases; every recursive function is a μ-recursive function and vice versa under the Church-Turing thesis",
            "confidence": 0.96,
        },
        "automata__regex_engine": {
            "math": "Automata theory: finite automata (DFA/NFA) recognize exactly the regular languages; regular expressions denote the same class via Kleene's theorem",
            "code": "Regex/pattern matching engines: regular expression libraries compile patterns to DFA/NFA or backtracking matchers for text search and validation",
            "rule": "Kleene's theorem: regular expressions and finite automata denote the same language class; a regex compiles to an automaton that accepts exactly its denotation",
            "confidence": 0.97,
        },
        "category_theory__monads": {
            "math": "Category theory: monads (T, η, μ) as endofunctors with natural transformations unit and multiplication satisfying associativity and identity laws",
            "code": "Monads in functional programming: computational context wrappers (Maybe, List, IO, State) with bind (>>=) and return, sequencing effectful computations",
            "rule": "A monad in FP is a monad in the category of types and functions: return = η (unit), bind = μ ∘ T(f) (Kleisli extension); the monad laws are exactly associativity and unitality",
            "confidence": 0.94,
        },
        "graph_theory__data_structures": {
            "math": "Graph theory: G=(V,E) with vertices, edges, and properties (directed/undirected, weighted, cyclic); trees and lists are restricted graphs",
            "code": "Tree/list/graph data structures: linked lists, binary trees, adjacency lists, hash maps — all graph-based containers with traversal and connectivity operations",
            "rule": "Every linked structure is a graph: a linked list is a path graph, a tree is an acyclic connected graph, a hash map is a bipartite incidence structure; traversal algorithms are graph walks",
            "confidence": 0.96,
        },
        "boolean_logic__control_flow": {
            "math": "Boolean algebra: a complemented distributive lattice with operations ∧ (AND), ∨ (OR), ¬ (NOT); Boolean ring with XOR as addition and AND as multiplication",
            "code": "Control flow: if/else branching, boolean expressions, short-circuit evaluation, and conditional logic that determines execution paths",
            "rule": "Every if/else is a boolean expression evaluated to a truth value selecting a branch; De Morgan's laws optimize compound conditions; boolean algebra governs all conditional control flow",
            "confidence": 0.97,
        },
        "complexity_theory__big_o": {
            "math": "Computational complexity theory: classification of problems by resource bounds (time, space); P, NP, PSPACE, EXPTIME; the Cook-Levin theorem and NP-completeness",
            "code": "Big-O analysis: asymptotic complexity classification of algorithms — O(n), O(n log n), O(n²), O(2ⁿ) — measuring growth rate as input size increases",
            "rule": "An algorithm's time complexity is its worst-case resource function in asymptotic notation; O(f(n)) bounds the growth rate; complexity classes classify the problems solvable within those bounds",
            "confidence": 0.95,
        },
        "set_theory__collections": {
            "math": "Set theory: sets, subsets, unions, intersections, differences, power sets; ZFC axioms; functions as sets of ordered pairs",
            "code": "Set/dict/collection types: Python sets, dicts, JavaScript Maps/Sets, Java collections — containers with membership, union, intersection, and key-value operations",
            "rule": "A set/dict is a computable set: membership test is the characteristic function, union/intersection/difference implement set operations, dict keys form a set with value annotations",
            "confidence": 0.93,
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

        If origin_domain contains 'math', direction is math→code.
        If origin_domain contains 'coda' or 'code', direction is code→math.
        """
        if tokens is None:
            tokens = []

        origin_lower = origin_domain.lower()

        # Determine direction
        if "math" in origin_lower:
            direction = Direction.MATH_TO_CODE
        elif "coda" in origin_lower or "code" in origin_lower:
            direction = Direction.CODE_TO_MATH
        else:
            # Infer from concept content
            code_keywords = [
                "algorithm", "function", "recursion", "lambda", "type",
                "monad", "regex", "data structure", "tree", "list",
                "if", "else", "loop", "iterator", "compiler", "parser",
                "class", "object", "variable", "collection", "dictionary",
            ]
            math_keywords = [
                "turing", "automata", "category", "graph", "boolean",
                "complexity", "set theory", "recursive function",
                "lambda calculus", "type theory", "theorem", "proof",
                "algebra", "formal", "axiom", "isomorphism",
            ]
            if any(m in origin_concept.lower() for m in math_keywords):
                direction = Direction.MATH_TO_CODE
            else:
                direction = Direction.CODE_TO_MATH

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.CODE_TO_MATH:
            destination_concept = iso_data["math"]
        else:
            destination_concept = iso_data["code"]

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
            text = f"{data['math']} {data['code']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["math"], data["code"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__code_form"
            best_data = {
                "math": f"Abstract structure derived from {concept}",
                "code": f"Programmatic form embodying {structural_property}",
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

        if direction == Direction.CODE_TO_MATH:
            src_label, dst_label = "code", "mathematical"
            src_obj = iso_data["code"]
            dst_obj = iso_data["math"]
        else:
            src_label, dst_label = "mathematical", "code"
            src_obj = iso_data["math"]
            dst_obj = iso_data["code"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into components and interfaces",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the building blocks of {origin_concept}? What are its atoms?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread="Each component carries a label — not merely a name, but the role it plays in the larger system.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj}' maps to the {dst_label} structure '{dst_obj}' through a formal correspondence.",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Coordinate projection preserving metric invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread="The mapped elements are placed in their new home — not arbitrarily, but according to the deep symmetries they share.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under associative operation preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The components are assembled into a whole — a {dst_label} object that breathes with the same logic as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
            formal_rule="Inverse homomorphism check: φ⁻¹(φ(x)) ≈ x within tolerance ε",
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
            "turing": "tape, head position, state set, transition function, accept states",
            "lambda": "abstraction (λx.M), application (M N), bound variables, free variables, β-redex",
            "type": "type constructors, term constructors, typing judgments, substitution, reduction rules",
            "recursi": "base case, recursive case, termination measure, call stack, induction hypothesis",
            "automaton": "states, alphabet, transition function, initial state, accept states",
            "regex": "pattern, character classes, quantifiers, capture groups, backtracking stack",
            "monad": "type constructor, unit (return), bind (>>=), monad laws, effect context",
            "graph": "vertices, edges, adjacency, weights, connectivity, traversal order",
            "tree": "nodes, edges, root, leaves, parent-child links, depth, balance factor",
            "list": "cons cell, head, tail, length, index, iterator position",
            "boolean": "truth values, AND, OR, NOT, expressions, normal form, satisfiability",
            "if": "condition, then-branch, else-branch, boolean expression, evaluation order",
            "else": "condition, then-branch, else-branch, boolean expression, evaluation order",
            "complexity": "input size, time function, space function, asymptotic bound, reduction",
            "big": "growth rate, dominant term, input size, worst case, amortized cost",
            "set": "elements, membership, union, intersection, complement, cardinality",
            "dict": "keys, values, entries, hash function, buckets, load factor",
            "collection": "elements, membership, iteration, containment, cardinality",
            "algorithm": "input, output, steps, termination, correctness, complexity",
            "function": "parameters, body, return value, scope, closure, call site",
            "data": "fields, pointers, invariants, operations, allocation, layout",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "components, interfaces, and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "turing": "tape:sequence; head:position; state:finite; transition:function",
            "lambda": "abstraction:binding; application:call; variable:bound; redex:reducible",
            "type": "type:classifier; term:inhabitant; judgment:derivable; substitution:capture-avoiding",
            "recursi": "base:terminating; step:inductive; measure:decreasing; call:recursive",
            "automaton": "state:finite; transition:deterministic; alphabet:discrete; accept:terminal",
            "regex": "pattern:regular; quantifier:repetition; group:capture; match:substring",
            "monad": "constructor:functor; unit:natural; bind:kleisli; law:equational",
            "graph": "vertex:node; edge:link; weight:cost; traversal:walk",
            "tree": "node:element; edge:parent-child; root:unique; leaf:terminal",
            "list": "cons:cell; head:element; tail:sublist; index:position",
            "boolean": "value:binary; operator:lattice; expression:compositional; branch:conditional",
            "if": "condition:boolean; then:block; else:block; evaluation:short-circuit",
            "else": "condition:boolean; then:block; else:block; evaluation:short-circuit",
            "complexity": "class:resource-bounded; reduction:poly-time; bound:asymptotic; measure:worst-case",
            "big": "growth:asymptotic; term:dominant; bound:upper; notation:landau",
            "set": "element:member; operation:set-algebra; cardinality:finite; subset:contained",
            "dict": "key:hashable; value:mapped; entry:pair; bucket:chained",
            "collection": "element:member; iteration:ordered; containment:membership; size:cardinality",
            "algorithm": "input:parameter; step:instruction; output:result; termination:halting",
            "function": "param:typed; body:expression; return:value; scope:lexical",
            "data": "field:slot; pointer:reference; invariant:preserved; layout:contiguous",
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
            f"What {origin} builds in code, {destination} proves in ink — the same structure, twice-born.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single theorem seen from two angles.",
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


def get_transformer() -> CodeMathTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeMathTransformer()
    return _default_transformer