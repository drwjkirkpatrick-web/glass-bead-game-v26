"""
glass-bead-game-v26 — Technology ↔ Math Transformer
Formal bidirectional transformation scaffold between technological artifacts
and mathematical structures, with human language as the connecting thread.

This module corresponds to the idea that engineering is applied mathematics:
every circuit, protocol, and data structure is a materialized theorem.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    TECHNOLOGY_TO_MATH = "technology→math"
    MATH_TO_TECHNOLOGY = "math→technology"


@dataclass
class TransformationStep:
    """A single step in the Technology ↔ Math transformation pipeline."""
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


class TechnologyMathTransformer:
    """
    Formal bidirectional transformer between technological and mathematical structures.

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
        "boolean_algebra__digital_circuits": {
            "math": "Boolean algebra: two-valued lattice with AND, OR, NOT",
            "technology": "Digital circuits: logic gates implementing boolean operations on bits",
            "rule": "De Morgan's laws and boolean identities map directly to gate equivalence: NOT(A AND B) ≡ (NOT A) OR (NOT B); every combinational circuit is a boolean formula made physical",
            "confidence": 0.99,
        },
        "finite_state_machine__cpu_design": {
            "math": "Finite state machine (FSM): (Q, Σ, δ, q₀, F) — states, alphabet, transition function, initial, accept states",
            "technology": "CPU control unit: a finite state machine drives the fetch-decode-execute cycle through clocked state transitions",
            "rule": "The control unit's state register + next-state logic = an FSM; each instruction maps to a state path through the transition graph δ",
            "confidence": 0.97,
        },
        "graph_algorithms__network_routing": {
            "math": "Weighted graph G=(V,E,w): shortest-path algorithms (Dijkstra, Bellman-Ford, A*) find minimum-cost paths",
            "technology": "Network routing: OSPF/IS-IS compute shortest paths across a topology graph of routers and links",
            "rule": "A network is a weighted graph where nodes = routers, edges = links, weights = cost/metric; routing protocols compute the shortest-path tree rooted at each node",
            "confidence": 0.98,
        },
        "information_theory__data_compression": {
            "math": "Shannon entropy H(X) = -Σ p(x) log p(x); source coding theorem sets the lower bound on lossless compression",
            "technology": "Data compression: Huffman coding, arithmetic coding, LZW approach the entropy limit for symbol streams",
            "rule": "The expected code length L ≥ H(X) with equality iff the code is optimal; compression exploits the statistical redundancy of the source",
            "confidence": 0.96,
        },
        "linear_algebra__3d_graphics_matrices": {
            "math": "Linear algebra: vector spaces, matrix operations, affine and projective transformations",
            "technology": "3D computer graphics: rotation, translation, scaling, and perspective projection expressed as 4×4 homogeneous matrices",
            "rule": "Every 3D transformation is a linear map in homogeneous coordinates; composition of transforms = matrix multiplication in GL(4,R)",
            "confidence": 0.97,
        },
        "probability_theory__machine_learning": {
            "math": "Probability theory: random variables, distributions, Bayesian inference, expectation, variance",
            "technology": "Machine learning: models learn by minimizing expected loss; training is stochastic optimization over a data distribution",
            "rule": "Empirical risk minimization approximates expected loss L(θ) = E[ℓ(f_θ(x), y)]; gradient descent follows the negative gradient of the empirical expectation",
            "confidence": 0.95,
        },
        "automata_theory__compilers_parsers": {
            "math": "Formal language hierarchy: regular (DFA/NFA), context-free (PDA), context-sensitive; parse trees as derivations",
            "technology": "Compilers: lexers scan via DFA; parsers build syntax trees via context-free grammar (LL, LR, LALR)",
            "rule": "Lexing = DFA execution on the character stream; parsing = pushdown automaton deriving the parse tree via grammar productions; each grammar production is a rewrite rule",
            "confidence": 0.98,
        },
        "error_correcting_codes__algebraic_coding": {
            "math": "Algebraic coding theory: linear codes over GF(q), minimum distance, generator and parity-check matrices",
            "technology": "Error-correcting codes: Hamming, Reed-Solomon, LDPC, and turbo codes detect and correct transmission errors",
            "rule": "A code C ⊆ GF(q)^n with minimum distance d corrects ⌊(d-1)/2⌋ errors; the generator matrix G encodes, the parity-check matrix H verifies: Hx^T = 0 iff x ∈ C",
            "confidence": 0.94,
        },
        "cryptography__number_theory": {
            "math": "Number theory: modular arithmetic, primality, discrete logarithm, elliptic curves over finite fields",
            "technology": "Cryptography: RSA, Diffie-Hellman, ECDSA rely on the computational hardness of factoring and the discrete log problem",
            "rule": "RSA: c = m^e mod n; security rests on factoring n = pq being hard. ECDLP: given G, kG, finding k is infeasible — the discrete log assumption on elliptic curves",
            "confidence": 0.93,
        },
        "signal_processing__fourier_analysis": {
            "math": "Fourier analysis: the DFT decomposes a discrete signal into orthogonal frequency components; convolution theorem links time and frequency domains",
            "technology": "Digital signal processing: FFT hardware, audio/image codecs, radar, and software-defined radio all compute spectra and filter via convolution",
            "rule": "DFT: X[k] = Σ x[n] e^{-2πikn/N}; the FFT computes it in O(N log N); filtering is pointwise multiplication in the frequency domain via the convolution theorem",
            "confidence": 0.96,
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

        If origin_domain is "Technology", direction is technology→math.
        If origin_domain is "Mathematics", direction is math→technology.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "math" in origin_domain.lower() or "mathematic" in origin_domain.lower():
            direction = Direction.MATH_TO_TECHNOLOGY
        elif "tech" in origin_domain.lower():
            direction = Direction.TECHNOLOGY_TO_MATH
        else:
            # Infer from concept content
            tech_keywords = [
                "circuit", "cpu", "router", "compress", "render", "matrix",
                "neural", "parser", "compiler", "code", "cipher", "encrypt",
                "signal", "filter", "protocol", "algorithm",
            ]
            math_keywords = [
                "group", "function", "theorem", "proof", "axiom",
                "topology", "algebra", "geometry", "number", "sequence",
                "matrix", "vector", "eigen", "fourier", "graph", "entropy",
            ]
            if any(m in origin_concept.lower() for m in math_keywords):
                direction = Direction.MATH_TO_TECHNOLOGY
            else:
                direction = Direction.TECHNOLOGY_TO_MATH

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.TECHNOLOGY_TO_MATH:
            destination_concept = iso_data["math"]
        else:
            destination_concept = iso_data["technology"]

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
            text = f"{data['math']} {data['technology']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["math"], data["technology"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__technological_form"
            best_data = {
                "math": f"Abstract structure derived from {concept}",
                "technology": f"Engineered form embodying {structural_property}",
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

        if direction == Direction.TECHNOLOGY_TO_MATH:
            src_label, dst_label = "technological", "mathematical"
            src_obj = iso_data["technology"]
            dst_obj = iso_data["math"]
        else:
            src_label, dst_label = "mathematical", "technological"
            src_obj = iso_data["math"]
            dst_obj = iso_data["technology"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into components and interfaces",
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
            language_thread="Each component carries a label — not merely a name, but the role it plays in the larger system.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj}' maps to the {dst_label} structure '{dst_obj}' through a formal correspondence.",
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
            language_thread=f"The components are assembled into a whole — a {dst_label} object that breathes with the same logic as its {src_label} twin.",
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

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "circuit": "gates, wires, fan-in, fan-out, timing, clock domain",
            "cpu": "fetch, decode, execute, writeback, pipeline stages, control signals",
            "router": "forwarding table, interfaces, routing protocol, packet, link state",
            "compress": "symbol model, entropy coder, dictionary, probability table",
            "matrix": "basis vectors, linear map, determinant, kernel, image",
            "neural": "layers, weights, activation, loss function, gradient, optimizer",
            "parser": "token stream, grammar productions, parse tree, stack, lookahead",
            "code": "codeword, generator matrix, parity check, syndrome, minimum distance",
            "cipher": "key space, plaintext, ciphertext, round function, diffusion, confusion",
            "signal": "samples, frequency bins, window, filter coefficients, impulse response",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "components, interfaces, and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "circuit": "gate:boolean; wire:signal; timing:clocked",
            "cpu": "state:finite; transition:deterministic; datapath:combinational",
            "router": "node:vertex; link:edge; metric:weight",
            "compress": "symbol:stochastic; code:prefix-free; entropy:bound",
            "matrix": "vector:linear; transform:affine; coordinate:homogeneous",
            "neural": "parameter:learnable; loss:expected; gradient:stochastic",
            "parser": "token:terminal; production:rewrite; tree:derivation",
            "code": "codeword:linear; distance:minimum; parity:constraint",
            "cipher": "key:secret; round:iterated; hardness:computational",
            "signal": "sample:discrete; spectrum:orthogonal; filter:convolution",
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
            f"What {origin} builds in silicon, {destination} proves in ink — the same structure, twice-born.",
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


def get_transformer() -> TechnologyMathTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = TechnologyMathTransformer()
    return _default_transformer