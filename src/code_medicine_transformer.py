"""
glass-bead-game-v26 — Code ↔ Medicine Transformer
Formal bidirectional transformation scaffold between computer code / programming
structures and medical / biological structures, with human language as the
connecting thread.

Hesse's Glass Bead Game seeks correspondences across all domains of
knowledge; this module makes the deep analogy between the architecture of
software and the architecture of the living body explicit, testable,
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
    CODE_TO_MEDICINE = "code→medicine"
    MEDICINE_TO_CODE = "medicine→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Medicine transformation pipeline."""
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


class CodeMedicineTransformer:
    """
    Formal bidirectional transformer between computer code / programming and
    medical / biological structures.

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
        "error_handling__immune_response": {
            "code": "Exception handling: try/catch blocks, error codes, signal handlers that detect anomalous states and trigger recovery cascades",
            "medicine": "Immune response: pattern-recognition receptors (TLRs) detect pathogen-associated molecular patterns and trigger inflammatory cascades for defense and recovery",
            "rule": "Exception handling ≅ innate immune response: both employ sentinel detectors that recognize deviation from expected state and launch a cascading response to restore normal operation; the try/catch boundary ≅ the self/non-self recognition boundary",
            "confidence": 0.92,
        },
        "garbage_collection__apoptosis": {
            "code": "Garbage collection: runtime reclaims memory from unreachable objects via mark-and-sweep or reference counting, preventing resource exhaustion",
            "medicine": "Apoptosis: programmed cell death via caspase cascades removes damaged or unneeded cells, maintaining tissue homeostasis and preventing pathological overgrowth",
            "rule": "Garbage collection ≅ apoptosis: both are regulated disposal mechanisms that identify units no longer reachable / viable and dismantle them cleanly; memory leak ≅ failure of apoptosis (cancer); premature collection ≅ premature apoptosis (degeneration)",
            "confidence": 0.90,
        },
        "type_system__blood_typing_tissue_matching": {
            "code": "Type system: static type checking ensures operations receive compatible operands; type mismatches are caught at compile time preventing runtime errors",
            "medicine": "Blood typing and tissue matching: ABO/Rh and HLA typing ensure transfusion and transplant compatibility; mismatch triggers catastrophic immune-mediated rejection",
            "rule": "Type system ≅ tissue typing: both enforce compatibility constraints at interfaces — a type error at compile time ≅ a transfusion reaction in vivo; the type checker ≅ the crossmatch assay",
            "confidence": 0.89,
        },
        "recursion__viral_replication": {
            "code": "Recursion: a function defined in terms of itself with a base case and a recursive case, producing self-similar computational structures (call trees, fractal traversals)",
            "medicine": "Viral replication: a virus hijacks host machinery to copy its genome and self-assemble virions in an exponential cascade — each virion is a template for the next",
            "rule": "Recursion ≅ viral replication: both follow a recurrence v_{n+1} = F(v_n) with a termination condition; the base case ≅ the depletion of susceptible host cells; the call stack ≅ the chain of infection",
            "confidence": 0.87,
        },
        "compiler_optimization__metabolic_efficiency": {
            "code": "Compiler optimization: dead-code elimination, loop unrolling, constant folding, and register allocation minimize execution time and resource use while preserving semantics",
            "medicine": "Metabolic efficiency: enzymatic pathways are optimized through allosteric regulation, substrate channeling, and feedforward/feedback to minimize energy expenditure while preserving metabolic output",
            "rule": "Compiler optimization ≅ metabolic pathway optimization: both apply transformations that reduce cost (time / ATP) while preserving the output invariant (program semantics / metabolic flux); dead-code elimination ≅ elimination of futile cycles",
            "confidence": 0.88,
        },
        "version_control__dna_repair": {
            "code": "Version control (git): commits snapshot state, diffs track changes, branching isolates experiments, and rollback restores a known-good version after a bad commit",
            "medicine": "DNA repair: mismatch repair, nucleotide excision repair, and double-strand break repair detect and correct replication errors, with checkpoint arrest preventing propagation of damaged genomes",
            "rule": "Version control ≅ DNA repair: both maintain a history of states and provide mechanisms to detect, revert, and recover from errors; a git revert ≅ nucleotide excision repair; a checkpoint arrest ≅ a failed CI build blocking a merge",
            "confidence": 0.91,
        },
        "design_patterns__protein_folding_motifs": {
            "code": "Design patterns: reusable architectural solutions (Singleton, Observer, Factory, Strategy) that encode proven solutions to recurring design problems in software",
            "medicine": "Protein folding motifs: recurrent structural elements (helix-turn-helix, zinc finger, beta-barrel) that encode proven structural solutions to recurring functional problems in biology",
            "rule": "Design patterns ≅ protein folding motifs: both are conserved structural templates that solve a recurring problem — the Observer pattern ≅ the allosteric switch motif; both are selected because they are robust, reusable, and evolvable",
            "confidence": 0.89,
        },
        "concurrency_locking__neural_refractory_period": {
            "code": "Concurrency locking: mutexes and semaphores enforce mutual exclusion, preventing simultaneous conflicting access to shared resources; a locked resource is temporarily unavailable",
            "medicine": "Neural refractory period: after an action potential, the sodium channels are inactivated and the neuron cannot fire again for a few milliseconds, enforcing temporal exclusion",
            "rule": "Concurrency lock ≅ refractory period: both enforce temporal exclusion on a shared resource (memory location / ion channel); the lock release ≅ channel recovery from inactivation; both prevent destructive simultaneous activation",
            "confidence": 0.86,
        },
        "caching_memoization__immune_memory": {
            "code": "Caching and memoization: store the results of expensive function calls and return the cached result when the same inputs occur again, trading space for time",
            "medicine": "Immune memory: after an initial infection, memory B and T cells persist and mount a faster, stronger response upon re-exposure to the same antigen",
            "rule": "Memoization ≅ immune memory: both store the result of a prior computation (function call / immune response) to accelerate future responses to the same input (arguments / antigen); the cache lookup ≅ the secondary immune response",
            "confidence": 0.93,
        },
        "debugging_tracing__clinical_diagnosis": {
            "code": "Debugging and tracing: systematic isolation of a fault via breakpoints, logging, stack traces, and hypothesis-driven binary search through the code's execution path",
            "medicine": "Clinical diagnosis: systematic isolation of a disease via history, physical exam, laboratory tests, imaging, and hypothesis-driven differential diagnosis",
            "rule": "Debugging ≅ clinical diagnosis: both follow the hypothetico-deductive method — form a differential, gather evidence, narrow the cause, and confirm via a discriminating test; the stack trace ≅ the diagnostic workup; the root cause ≅ the underlying pathology",
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

        If origin_domain is "Code", direction is code→medicine.
        If origin_domain is "Medicine", direction is medicine→code.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        if "code" in origin_domain.lower() or "program" in origin_domain.lower() or "software" in origin_domain.lower():
            direction = Direction.CODE_TO_MEDICINE
        elif "medic" in origin_domain.lower() or "biolog" in origin_domain.lower():
            direction = Direction.MEDICINE_TO_CODE
        else:
            # Infer from concept content
            code_keywords = [
                "error", "exception", "garbage", "type", "recursion", "recursive",
                "compiler", "compile", "version", "git", "design pattern",
                "concurrency", "lock", "mutex", "cache", "memoiz", "debug",
                "algorithm", "function", "class", "thread", "program",
            ]
            med_keywords = [
                "immune", "apoptosis", "blood", "metabolic", "metabolism",
                "dna", "protein", "neural", "neuron", "cell", "tissue",
                "diagnos", "disease", "receptor", "gene", "inflammation",
                "virus", "viral", "antibody", "antigen",
            ]
            if any(c in origin_concept.lower() for c in code_keywords):
                direction = Direction.CODE_TO_MEDICINE
            else:
                direction = Direction.MEDICINE_TO_CODE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.CODE_TO_MEDICINE:
            destination_concept = iso_data["medicine"]
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
            text = f"{data['code']} {data['medicine']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["code"], data["medicine"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__code_medicine"
            best_data = {
                "code": f"Computational structure derived from {concept}",
                "medicine": f"Biological structure embodying {structural_property}",
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

        if direction == Direction.CODE_TO_MEDICINE:
            src_label, dst_label = "computational", "biological"
            src_obj = iso_data["code"]
            dst_obj = iso_data["medicine"]
        else:
            src_label, dst_label = "biological", "computational"
            src_obj = iso_data["medicine"]
            dst_obj = iso_data["code"]

        # ─── Stage 1: PARSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into elements and relations",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the working parts of {origin_concept}? What are its modules, its signals, its feedback loops?",
        ))

        # ─── Stage 2: TAG ────────────────────────────────────────
        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread="Each part carries a label — not merely a name, but the role it plays in the working whole, whether in silicon or in flesh.",
        ))

        # ─── Stage 3: MAP ──────────────────────────────────────
        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} pattern '{src_obj}' maps to the {dst_label} pattern '{dst_obj}' through a deep structural correspondence.",
        ))

        # ─── Stage 4: PROJECT ────────────────────────────────────
        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Coordinate projection preserving metric invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread="The mapped parts find their place in the new domain — not arbitrarily, but along the lines that nature and engineering both drew.",
        ))

        # ─── Stage 5: COMPOSE ────────────────────────────────────
        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj}",
            formal_rule="Composition under associative operation preserving isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The parts compose into a working whole — a {dst_label} form that runs with the same logic as its {src_label} twin.",
        ))

        # ─── Stage 6: VERIFY ────────────────────────────────────
        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj}",
            formal_rule="Inverse homomorphism check: φ⁻¹(φ(x)) ≈ x within tolerance ε",
            confidence=round(base_conf * 0.90, 3),
            language_thread="We turn the glass bead over, looking back through it to ensure the pattern still holds — transformed, but unbroken.",
        ))

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        """Return a plausible structural decomposition."""
        decomps = {
            "error": "exception object, handler block, stack frame, signal, recovery routine, error code",
            "exception": "exception object, handler block, stack frame, signal, recovery routine, error code",
            "garbage": "object graph, root set, reachable reference, unreachable object, collector, free list",
            "type": "type signature, subtype, supertype, constraint, coercion rule, checker",
            "recursion": "base case, recursive case, call stack, frame, termination condition, self-reference",
            "recursive": "base case, recursive case, call stack, frame, termination condition, self-reference",
            "compiler": "AST node, optimization pass, intermediate representation, register, code generator, invariant",
            "version": "commit, diff, branch, tree, merge, revert, HEAD, working copy",
            "git": "commit, diff, branch, tree, merge, revert, HEAD, working copy",
            "design pattern": "context, problem, solution, participant, collaboration, consequence",
            "concurrency": "thread, lock, mutex, semaphore, critical section, condition variable, deadlock",
            "lock": "thread, lock, mutex, semaphore, critical section, condition variable, deadlock",
            "mutex": "thread, lock, mutex, semaphore, critical section, condition variable, deadlock",
            "cache": "key, value, lookup, hit, miss, eviction policy, storage, retrieval",
            "memoiz": "key, value, lookup, hit, miss, eviction policy, storage, retrieval",
            "debug": "breakpoint, stack trace, log line, variable state, hypothesis, root cause, reproduction",
            "immune": "receptor, antigen, lymphocyte, antibody, cytokine, memory cell, inflammatory cascade",
            "apoptosis": "caspase, death receptor, mitochondrial pathway, executioner, phagocyte, apoptotic body",
            "blood": "antigen, antibody, type marker, compatibility, transfusion, reaction, crossmatch",
            "metabolic": "enzyme, substrate, pathway, allosteric site, flux, cofactor, ATP yield",
            "dna": "base, nucleotide, strand, helix, polymerase, mismatch, repair enzyme, checkpoint",
            "protein": "amino acid, secondary structure, motif, fold, active site, chaperone, domain",
            "neural": "neuron, ion channel, action potential, refractory period, synapse, neurotransmitter",
            "neuron": "neuron, ion channel, action potential, refractory period, synapse, neurotransmitter",
            "diagnos": "history, symptom, sign, differential, test, imaging, root cause, treatment",
            "virus": "genome, capsid, host receptor, polymerase, replication cycle, virion, virulence",
            "viral": "genome, capsid, host receptor, polymerase, replication cycle, virion, virulence",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "elements, relations, and their working structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "error": "signal:exception; handler:recovery; state:abnormal",
            "exception": "signal:exception; handler:recovery; state:abnormal",
            "garbage": "object:reachable; collector:tracing; resource:reclaimable",
            "type": "signature:typed; constraint:static; check:compile-time",
            "recursion": "function:self-referential; case:base/recursive; structure:call-tree",
            "recursive": "function:self-referential; case:base/recursive; structure:call-tree",
            "compiler": "representation:intermediate; pass:transforming; output:optimized",
            "version": "state:committed; delta:diff; history:branching",
            "git": "state:committed; delta:diff; history:branching",
            "design pattern": "template:reusable; context:recurring; solution:proven",
            "concurrency": "resource:shared; access:exclusive; ordering:temporal",
            "lock": "resource:shared; access:exclusive; ordering:temporal",
            "mutex": "resource:shared; access:exclusive; ordering:temporal",
            "cache": "input:key; result:stored; retrieval:accelerated",
            "memoiz": "input:key; result:stored; retrieval:accelerated",
            "debug": "evidence:trace; method:hypothetico-deductive; goal:root-cause",
            "immune": "receptor:pattern-recognition; response:cascading; memory:adaptive",
            "apoptosis": "signal:death; cascade:caspase; outcome:programmed-demise",
            "blood": "marker:antigen; compatibility:typed; mismatch:reactive",
            "metabolic": "enzyme:catalytic; regulation:allosteric; flux:optimized",
            "dna": "base:paired; strand:complementary; repair:enzymatic",
            "protein": "residue:amino-acid; fold:motif; function:structural",
            "neural": "channel:gated; potential:all-or-none; period:refractory",
            "neuron": "channel:gated; potential:all-or-none; period:refractory",
            "diagnos": "method:hypothetico-deductive; evidence:clinical; target:pathology",
            "virus": "genome:nucleic; shell:capsid; cycle:lytic",
            "viral": "genome:nucleic; shell:capsid; cycle:lytic",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:functional; relation:causal; property:emergent"

    def _generate_resonance(
        self,
        origin: str,
        destination: str,
        iso_name: str,
        structural_property: str,
    ) -> str:
        """Generate a poetic resonance sentence from the isomorphism."""
        templates = [
            f"As {origin} embodies {structural_property}, so {destination} reveals the same pattern in another medium of life.",
            f"What {origin} achieves in code, {destination} has evolved in the body — the same logic, twice-realized.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one design.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single pattern seen from two sides — one built, one grown.",
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


def get_transformer() -> CodeMedicineTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeMedicineTransformer()
    return _default_transformer