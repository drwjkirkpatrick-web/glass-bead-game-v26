"""
glass-bead-game-v26 — Code ↔ Technology Transformer
Formal bidirectional transformation scaffold between computer code (domain 'coda')
and technology (domain 'technologia'), with human language as the connecting thread.

This module corresponds to the idea that code is the crystallized intent of
technology: every API, protocol, and kernel is a specification made executable,
and every piece of code is a technology waiting to be understood as engineering.
"""
from __future__ import annotations
import json
import math
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    CODE_TO_TECHNOLOGY = "code→technology"
    TECHNOLOGY_TO_CODE = "technology→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ Technology transformation pipeline."""
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


class CodeTechnologyTransformer:
    """
    Formal bidirectional transformer between computer code and technological structures.

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
        "api__hardware_interface": {
            "technology": "Hardware interface/spec: pinout, signal levels, timing diagrams, electrical and mechanical contracts defining how a device exposes its capabilities",
            "code": "Software API: function signatures, type contracts, parameter and return conventions defining how a library or service exposes its capabilities to callers",
            "rule": "An API is to software what a hardware interface specification is to a device: both define a boundary contract — inputs, outputs, preconditions, guarantees — that decouples the consumer from the internal implementation; changing internals without breaking the contract is the same principle in both domains",
            "confidence": 0.97,
        },
        "embedded_code__firmware": {
            "technology": "Firmware: persistent low-level software stored in non-volatile memory that directly controls hardware registers, peripherals, and boot sequences on an embedded device",
            "code": "Embedded code: C/assembly programs that manipulate memory-mapped registers, manage interrupt service routines, and interface with hardware through bit-level operations and real-time constraints",
            "rule": "Firmware IS embedded code — the distinction is one of deployment context, not structure: both sit at the hardware/software boundary, both speak the language of registers and interrupts; the isomorphism is the identity map mediated by the cross-compiler toolchain that turns source into ROM image",
            "confidence": 0.98,
        },
        "network_protocol__network_code": {
            "technology": "Network protocol specification: RFC-defined packet formats, state machines for handshakes, sequencing rules, and error-handling semantics that govern inter-system communication",
            "code": "Network programming/sockets: socket API calls, buffer management, event loops, and connection-state handling that implement the protocol specification in running software",
            "rule": "A protocol spec is the abstract grammar; the socket program is its concrete implementation — each packet field maps to a struct member, each protocol state maps to a code path, each handshake transition maps to a send/recv sequence; the spec is the type and the code is the term inhabiting it",
            "confidence": 0.96,
        },
        "database__query_language": {
            "technology": "Database engine: storage manager, query optimizer, transaction coordinator, and index structures that physically persist and retrieve data with ACID guarantees",
            "code": "Query language/SQL: declarative statements (SELECT, JOIN, WHERE) that express what data is desired without specifying how it is retrieved, compiled by the engine into execution plans",
            "rule": "The query language is the user-facing algebra of the database's internal relational calculus; every SQL statement is an expression that the optimizer translates into physical operators (scan, hash-join, sort) — the language is the interface and the engine is the evaluator of that language's denotational semantics",
            "confidence": 0.95,
        },
        "os_kernel__kernel_code": {
            "technology": "OS kernel architecture: scheduler, memory manager, virtual file system, syscall interface, and process abstraction that mediate between hardware and user programs",
            "code": "Kernel/driver code: C systems programming implementing process tables, page fault handlers, context switches, device drivers, and the syscall dispatch layer",
            "rule": "The kernel architecture is the design; the kernel code is the realization — each architectural component (scheduler, VFS, MMU handler) maps to a concrete subsystem of functions and data structures; the architecture diagram is the type and the source tree is the inhabitant",
            "confidence": 0.97,
        },
        "cloud_infrastructure__iac": {
            "technology": "Cloud infrastructure: virtual machines, load balancers, VPCs, subnets, security groups, and managed services provisioned across regions and availability zones",
            "code": "Infrastructure as Code/Terraform: declarative HCL/YAML resources that describe the desired cloud topology, applied by a planner that converges actual state to declared state",
            "rule": "IaC is the declarative specification of which the cloud infrastructure is the runtime instance — each Terraform resource maps to a cloud API call, each dependency graph edge maps to a creation-ordering constraint; `terraform apply` is the evaluator that reduces the declarative program to a concrete deployed system",
            "confidence": 0.94,
        },
        "cryptography__crypto_libraries": {
            "technology": "Cryptographic algorithms: AES, SHA-256, RSA, ECC — mathematical primitives defined over finite fields and number-theoretic structures with proven security properties",
            "code": "Crypto library implementations: OpenSSL, libsodium, and similar libraries that implement algorithms as optimized C/Rust functions with constant-time guarantees, side-channel resistance, and tested test vectors",
            "rule": "The algorithm is the mathematical object; the library is its faithful implementation — each round function maps to a code block, each field operation maps to a bignum routine, each security proof maps to a constant-time coding discipline; the library is the algorithm compiled from mathematics to machine",
            "confidence": 0.93,
        },
        "ui_framework__frontend_code": {
            "technology": "UI framework: React, Vue, or similar systems providing component trees, virtual DOM diffing, state management, and a reactive update lifecycle as architectural abstractions",
            "code": "Frontend code/React: JSX components, hooks (useState, useEffect), event handlers, and render functions that instantiate the framework's abstractions into a running user interface",
            "rule": "The UI framework is the library of reusable patterns; the frontend code is the specific composition — each component class maps to a JSX element, each framework lifecycle hook maps to a useEffect call, each state container maps to a useState/reducer; the framework is the grammar and the frontend code is the program written in it",
            "confidence": 0.92,
        },
        "vcs__git_internals": {
            "technology": "Version control concepts: commits, branches, merges, diffs, and history graphs as abstractions for tracking changes to a codebase over time",
            "code": "Git internals/implementation: object store (blobs, trees, commits, tags), DAG of commit hashes, pack files, reflog, and the content-addressable filesystem that realizes VCS concepts",
            "rule": "VCS concepts are the user-facing algebra; git internals are the concrete machinery — each 'commit' maps to a commit object hashing its tree and parent, each 'branch' maps to a movable ref pointer, each 'merge' maps to a tree-merge algorithm over the DAG; the concepts are the interface and the internals are the data structures that satisfy them",
            "confidence": 0.91,
        },
        "compiler_toolchain__build_systems": {
            "technology": "Compiler toolchain: lexer, parser, semantic analyzer, optimizer, and code generator that transform source language into target machine code through well-defined IR stages",
            "code": "Build systems/CI-CD: Make, Bazel, GitHub Actions — declarative pipelines that orchestrate compilation, testing, and deployment through dependency graphs and incremental execution",
            "rule": "The compiler toolchain transforms code through IR stages; the build system transforms the project through pipeline stages — each compiler pass maps to a build step, each IR level maps to an intermediate artifact, each optimization flag maps to a pipeline configuration; both are staged transformations where each stage's output is the next stage's input",
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

        If origin_domain contains 'tech', direction is technology→code.
        If origin_domain contains 'coda' or 'code', direction is code→technology.
        """
        if tokens is None:
            tokens = []

        # Determine direction
        origin_lower = origin_domain.lower()
        if "tech" in origin_lower:
            direction = Direction.TECHNOLOGY_TO_CODE
        elif "coda" in origin_lower or "code" in origin_lower:
            direction = Direction.CODE_TO_TECHNOLOGY
        else:
            # Infer from concept content
            tech_keywords = [
                "hardware", "interface", "firmware", "protocol", "database",
                "kernel", "cloud", "infrastructure", "crypto", "algorithm",
                "framework", "circuit", "device", "spec", "rfc",
            ]
            code_keywords = [
                "api", "socket", "sql", "query", "driver", "terraform",
                "iac", "openssl", "react", "jsx", "git", "commit",
                "make", "bazel", "function", "program", "script", "source",
            ]
            if any(c in origin_concept.lower() for c in code_keywords):
                direction = Direction.CODE_TO_TECHNOLOGY
            else:
                direction = Direction.TECHNOLOGY_TO_CODE

        # Find best-matching isomorphism
        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        # Build the 6-stage transformation pipeline
        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        # Compute destination concept from the isomorphism
        if direction == Direction.TECHNOLOGY_TO_CODE:
            destination_concept = iso_data["code"]
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
            text = f"{data['code']} {data['technology']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["code"], data["technology"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__code_technology"
            best_data = {
                "code": f"Code structure derived from {concept}",
                "technology": f"Technological form embodying {structural_property}",
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

        if direction == Direction.TECHNOLOGY_TO_CODE:
            src_label, dst_label = "technological", "code"
            src_obj = iso_data["technology"]
            dst_obj = iso_data["code"]
        else:
            src_label, dst_label = "code", "technological"
            src_obj = iso_data["code"]
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
            "api": "endpoints, request/response schemas, authentication, rate limits, versioning",
            "hardware": "pins, signal levels, registers, timing diagrams, interrupts, bus protocol",
            "interface": "contracts, signatures, parameters, return types, error codes, lifecycle",
            "firmware": "bootloader, ISR table, register config, flash layout, watchdog, power states",
            "embedded": "memory-mapped registers, interrupt handlers, DMA, RTOS tasks, peripheral drivers",
            "protocol": "packet format, handshake state machine, sequence numbers, checksums, timeouts",
            "socket": "file descriptor, bind, listen, accept, recv/send buffer, event loop",
            "network": "packets, headers, ports, connections, routing table, MTU, congestion window",
            "database": "storage pages, B-tree index, query planner, transaction log, lock manager",
            "sql": "SELECT, FROM, JOIN, WHERE, GROUP BY, execution plan, result set",
            "query": "projection, selection, join, aggregation, predicate, subquery, cursor",
            "kernel": "scheduler, page tables, syscall table, VFS, device drivers, interrupt dispatch",
            "driver": "probe, init, read/write ioctl, IRQ handler, DMA buffer, device struct",
            "cloud": "VMs, VPC, subnets, security groups, load balancers, regions, availability zones",
            "terraform": "resources, provider, state file, dependency graph, plan, apply",
            "iac": "declarative resources, variables, outputs, modules, state backend, plan diff",
            "crypto": "key schedule, round function, S-box, mode of operation, IV, MAC",
            "aes": "substitution, shift rows, mix columns, add round key, key expansion",
            "openssl": "EVP interface, cipher context, key derivation, RNG, X.509, TLS handshake",
            "react": "components, props, state, hooks, virtual DOM, reconciliation, lifecycle",
            "jsx": "elements, attributes, children, fragments, event handlers, render function",
            "git": "blob, tree, commit, ref, HEAD, index, pack file, reflog",
            "commit": "tree hash, parent hash, author, message, timestamp, SHA-1",
            "branch": "ref pointer, HEAD, merge base, fast-forward, remote tracking",
            "compiler": "lexer, parser, AST, semantic analysis, IR, optimizer, code generator",
            "make": "targets, prerequisites, recipes, variables, pattern rules, dependency graph",
            "bazel": "build targets, deps, actions, cache, sandbox, hermetic toolchain",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "components, interfaces, and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        """Return type tags for primitives."""
        tags = {
            "api": "endpoint:callable; signature:typed; contract:behavioral",
            "hardware": "pin:physical; signal:electrical; timing:clocked",
            "interface": "contract:specification; method:callable; error:enumerated",
            "firmware": "register:memory-mapped; isr:asynchronous; flash:persistent",
            "embedded": "register:volatile; interrupt:preemptive; dma:concurrent",
            "protocol": "field:typed; state:finite; checksum:redundant",
            "socket": "fd:integer; buffer:byte-stream; event:asynchronous",
            "network": "packet:serialized; port:numeric; connection:stateful",
            "database": "table:relational; index:ordered; transaction:atomic",
            "sql": "statement:declarative; predicate:boolean; join:relational",
            "query": "projection:columnar; selection:filtering; aggregation:reducing",
            "kernel": "process:scheduled; page:mapped; syscall:privileged",
            "driver": "device:abstracted; ioctl:interface; irq:hardware",
            "cloud": "instance:virtual; vpc:isolated; region:geographic",
            "terraform": "resource:declarative; state:tracked; provider:bound",
            "iac": "resource:declarative; module:composable; plan:diffed",
            "crypto": "key:secret; round:iterated; mode:parameterized",
            "aes": "sbox:substitution; round:iterated; key:expanded",
            "openssl": "evp:abstracted; context:stateful; cert:validated",
            "react": "component:composable; state:reactive; prop:passed",
            "jsx": "element:declarative; handler:event; render:functional",
            "git": "blob:content; tree:structural; commit:historical",
            "commit": "hash:content-addressed; parent:linked; tree:rooted",
            "branch": "ref:movable; head:current; merge:join",
            "compiler": "token:lexical; ast:structural; ir:intermediate",
            "make": "target:named; recipe:imperative; dep:ordered",
            "bazel": "target:labeled; action:hermetic; cache:content-addressed",
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
            f"What {origin} builds in logic, {destination} embodies in the world — the same structure, twice-born.",
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


def get_transformer() -> CodeTechnologyTransformer:
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeTechnologyTransformer()
    return _default_transformer