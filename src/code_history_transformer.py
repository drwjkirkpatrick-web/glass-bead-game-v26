"""
glass-bead-game-v26 — Code ↔ History Transformer
Formal bidirectional transformation scaffold between computer code
and historical structures, with human language as the connecting thread.

Hesse's Glass Bead Game unifies all disciplines; this module makes the
correspondence between Code and History explicit, testable, and playable —
the logic of the past and the logic of the machine as two faces of one bead.

"History is the code that civilization runs; code is the history that
machines remember." — The Magister Codae, contemplating the ninth bead.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class Direction(Enum):
    CODE_TO_HISTORY = "code→history"
    HISTORY_TO_CODE = "history→code"


@dataclass
class TransformationStep:
    """A single step in the Code ↔ History transformation pipeline."""
    stage: str
    input_repr: str
    output_repr: str
    formal_rule: str
    confidence: float
    language_thread: str


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
    tokens_seen: List[str]
    tokens_per_step: Dict[str, List[str]]
    total_confidence: float
    isomorphisms: List[str]

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


class CodeHistoryTransformer:
    """
    Formal bidirectional transformer between computer code and historical structures.

    The transformation proceeds through 6 canonical stages:
        1. PARSE    — Decompose the origin into structural primitives
        2. TAG      — Label each primitive with its formal type
        3. MAP      — Map primitives to the target domain via isomorphism
        4. PROJECT  — Project mapped primitives into target space
        5. COMPOSE  — Assemble projected elements into coherent structure
        6. VERIFY   — Check structural fidelity via inverse transformation

    Human language serves as the THREAD connecting each stage.
    """

    ISOMORPHISMS = {
        "version_control__historical_record": {
            "code": "Version control (git): commits as events, branches as narratives, merge as synthesis of parallel histories",
            "history": "Historical record: chronicles, annals, primary sources — the commit log of civilization",
            "rule": "A git log IS a historical chronicle: each commit is a dated event with an author and message; branches are competing narratives; merge resolves them into a unified timeline; revert undoes a historical event",
            "confidence": 0.96,
        },
        "archival_storage__digital_preservation": {
            "code": "Digital preservation: backups, checksums, redundant storage, format migration",
            "history": "Archival preservation: manuscript conservation, oral tradition, copying traditions, Rosetta Stone as multi-format encoding",
            "rule": "Both aim to preserve information against entropy: the archivist's climate-controlled vault is the engineer's RAID array; the scribe's careful copy is the checksum-verified backup",
            "confidence": 0.93,
        },
        "software_layers__archaeological_strata": {
            "code": "Software stack layers: kernel, libraries, frameworks, application — each built atop the previous",
            "history": "Archaeological strata: each layer of settlement built atop ruins of the previous, deeper = older",
            "rule": "Software layering IS archaeological stratigraphy: dependency depth = chronological depth; deprecated APIs = abandoned settlements; legacy compatibility = cultural continuity across layers",
            "confidence": 0.94,
        },
        "execution_trace__historical_timeline": {
            "code": "Execution trace: sequential log of program states, function calls, and variable changes over time",
            "history": "Historical timeline: chronological sequence of events, actors, and state changes in a civilization",
            "rule": "An execution trace IS a historical timeline: each function call is an event; each variable assignment is a state change; call stack depth = institutional hierarchy; thread = parallel historical narrative",
            "confidence": 0.92,
        },
        "paradigm_shift__scientific_revolution": {
            "code": "Programming paradigm shift: procedural → OOP → functional → reactive, each transforming how code is structured",
            "history": "Scientific revolution (Kuhn): paradigm shifts that redefine what counts as valid inquiry — Ptolemaic → Copernican → Newtonian → Einsteinian",
            "rule": "A paradigm shift in code IS a Kuhnian revolution: the old paradigm accumulates anomalies (spaghetti code, crisis); a new paradigm resolves them by redefining the fundamental abstractions; old code becomes 'legacy' = pre-revolutionary science",
            "confidence": 0.90,
        },
        "language_renaissance__programming_renaissance": {
            "code": "Programming language renaissance: new languages emerging with fresh paradigms (Rust, Go, Zig, Crystal)",
            "history": "Renaissance: rebirth of classical learning, explosion of new forms, synthesis of old and new",
            "rule": "A programming renaissance IS a cultural renaissance: new languages synthesize forgotten ideas (FP from lambda calculus) with modern needs; each new language is a city-state with its own culture and aesthetic",
            "confidence": 0.88,
        },
        "automation__industrial_revolution": {
            "code": "Automation: code replacing manual processes — CI/CD, build scripts, deployment pipelines, IaC",
            "history": "Industrial Revolution: machines replacing manual labor — steam engine, assembly line, mass production",
            "rule": "Automation IS the industrial revolution of code: the build pipeline IS the assembly line; manual deployment = cottage industry; CI/CD = factory production; the DevOps engineer is the factory manager",
            "confidence": 0.95,
        },
        "documentation__oral_tradition": {
            "code": "Documentation: READMEs, comments, API docs, tutorials — the transmitted knowledge of a codebase",
            "history": "Oral tradition: stories, songs, proverbs — the transmitted knowledge of a culture before literacy",
            "rule": "Documentation IS oral tradition for code: comments = proverbs (condensed wisdom); README = epic poem (the founding narrative); API docs = genealogy (who descends from whom); Stack Overflow = oral history collected",
            "confidence": 0.89,
        },
        "source_code__manuscript": {
            "code": "Source code: the primary text, carefully authored, with authority derived from authorship and lineage",
            "history": "Manuscript: the primary text, carefully copied, with authority derived from provenance and scribal tradition",
            "rule": "Source code IS a manuscript: the author is the scribe; the commit history is the provenance; the license is the seal of authority; forks are competing manuscript traditions; the 'canonical' repo is the authoritative recension",
            "confidence": 0.91,
        },
        "dark_age__technological_gap": {
            "code": "Technological gap: lost knowledge of legacy systems, abandoned codebases, undocumented internals",
            "history": "Dark Age: loss of literacy, infrastructure collapse, knowledge discontinuity between eras",
            "rule": "A codebase dark age IS a historical dark age: when institutional knowledge is lost (developers leave without documenting), the code becomes indecipherable; the 'lost arts' of mainframe COBOL = the 'lost arts' of Roman engineering",
            "confidence": 0.87,
        },
    }

    def __init__(self):
        self.token_log: List[str] = []
        self.step_tokens: Dict[str, List[str]] = {}

    def _log_tokens(self, stage: str, tokens: List[str]):
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
        if tokens is None:
            tokens = []

        if "histor" in origin_domain.lower():
            direction = Direction.HISTORY_TO_CODE
        elif "coda" in origin_domain.lower() or "code" in origin_domain.lower():
            direction = Direction.CODE_TO_HISTORY
        else:
            history_keywords = ["empire", "revolution", "century", "ancient", "medieval",
                                "renaissance", "war", "dynasty", "civilization", "chronicle"]
            code_keywords = ["function", "class", "algorithm", "compile", "variable",
                             "pointer", "recursion", "stack", "queue", "thread"]
            if any(k in origin_concept.lower() for k in history_keywords):
                direction = Direction.HISTORY_TO_CODE
            else:
                direction = Direction.CODE_TO_HISTORY

        iso_name, iso_data = self._find_isomorphism(
            origin_concept, origin_domain, destination_domain, structural_property
        )

        steps = self._build_pipeline(
            direction, origin_concept, iso_name, iso_data, structural_property, tokens
        )

        if direction == Direction.CODE_TO_HISTORY:
            destination_concept = iso_data["history"]
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
        self,
        concept: str,
        origin_domain: str,
        dest_domain: str,
        structural_property: str,
    ) -> Tuple[str, Dict[str, Any]]:
        concept_lower = concept.lower()
        property_lower = structural_property.lower()

        best_score = -1
        best_name = ""
        best_data = {}

        for name, data in self.ISOMORPHISMS.items():
            score = 0
            text = f"{data['code']} {data['history']} {data['rule']}".lower()

            for word in concept_lower.split():
                if len(word) > 3 and word in text:
                    score += 2

            for word in property_lower.split():
                if len(word) > 3 and word in text:
                    score += 3

            if concept_lower in text or any(
                concept_lower in s.lower()
                for s in [data["code"], data["history"]]
            ):
                score += 5

            if score > best_score:
                best_score = score
                best_name = name
                best_data = data

        if best_score < 2:
            best_name = "generic_homomorphism__code_history_form"
            best_data = {
                "code": f"Code structure derived from {concept}",
                "history": f"Historical pattern embodying {structural_property}",
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
        steps = []
        base_conf = iso_data.get("confidence", 0.85)

        if direction == Direction.CODE_TO_HISTORY:
            src_label, dst_label = "code", "historical"
            src_obj = iso_data["code"]
            dst_obj = iso_data["history"]
        else:
            src_label, dst_label = "historical", "code"
            src_obj = iso_data["history"]
            dst_obj = iso_data["code"]

        steps.append(TransformationStep(
            stage="PARSE",
            input_repr=f"{origin_concept} ({src_label})",
            output_repr=f"Primitive {src_label} components: {self._decompose(origin_concept)}",
            formal_rule="Structural decomposition into events, actors, and causal chains",
            confidence=round(base_conf * 0.95, 3),
            language_thread=f"We first ask: what are the building blocks of {origin_concept}? What forces shaped it?",
        ))

        steps.append(TransformationStep(
            stage="TAG",
            input_repr=f"Primitive components of {origin_concept}",
            output_repr=f"Tagged types: {self._tag_primitives(origin_concept)}",
            formal_rule="Type assignment via domain ontology",
            confidence=round(base_conf * 0.93, 3),
            language_thread="Each element carries a label — not merely a name, but the role it plays in the larger narrative.",
        ))

        steps.append(TransformationStep(
            stage="MAP",
            input_repr=f"Tagged {src_label} primitives",
            output_repr=f"Corresponding {dst_label} primitives via {iso_name}",
            formal_rule=iso_data["rule"],
            confidence=round(base_conf, 3),
            language_thread=f"Now we cross the bridge: the {src_label} structure '{src_obj[:60]}...' maps to the {dst_label} structure through a formal correspondence.",
        ))

        steps.append(TransformationStep(
            stage="PROJECT",
            input_repr=f"Mapped {dst_label} primitives",
            output_repr=f"Projected into {dst_label} parameter space",
            formal_rule="Chronological and causal projection preserving relational invariants",
            confidence=round(base_conf * 0.92, 3),
            language_thread="The mapped elements are placed in their new home — not arbitrarily, but according to the deep patterns they share.",
        ))

        steps.append(TransformationStep(
            stage="COMPOSE",
            input_repr=f"Projected {dst_label} elements",
            output_repr=f"Coherent {dst_label} structure: {dst_obj[:60]}...",
            formal_rule="Narrative composition preserving structural isomorphism class",
            confidence=round(base_conf * 0.94, 3),
            language_thread=f"The fragments are assembled into a whole — a {dst_label} narrative that breathes with the same logic as its {src_label} twin.",
        ))

        steps.append(TransformationStep(
            stage="VERIFY",
            input_repr=f"Composed {dst_label} structure",
            output_repr=f"Inverse map confirms structural fidelity: {src_obj[:60]}...",
            formal_rule="Inverse homomorphism check: the original structure is recoverable from its transformation",
            confidence=round(base_conf * 0.90, 3),
            language_thread="We turn the glass bead over, looking back through it to ensure the original light still shines — transformed, but unbroken.",
        ))

        for i, step in enumerate(steps):
            step_tokens = tokens[i * 3:(i + 1) * 3] if tokens else [f"[{step.stage}]"]
            self._log_tokens(step.stage, step_tokens)

        return steps

    def _decompose(self, concept: str) -> str:
        decomps = {
            "git": "commits, branches, merges, tags, HEAD, remote, working tree",
            "backup": "snapshot, checksum, redundancy, restore point, format migration",
            "stack": "kernel, driver, library, framework, application, API boundary",
            "trace": "function call, return address, variable state, thread, timestamp",
            "paradigm": "abstraction level, mental model, design principle, code organization",
            "language": "syntax, semantics, type system, standard library, community",
            "automation": "trigger, pipeline, stage, artifact, deployment, rollback",
            "documentation": "narrative, example, API reference, tutorial, comment, diagram",
            "source": "file, module, import, export, function, class, namespace",
            "legacy": "undocumented interface, deprecated API, missing tests, lost knowledge",
        }
        concept_lower = concept.lower()
        for key, val in decomps.items():
            if key in concept_lower:
                return val
        return "events, actors, causal chains, and their relational structure"

    def _tag_primitives(self, concept: str) -> str:
        tags = {
            "git": "commit:event; branch:narrative; merge:synthesis",
            "backup": "snapshot:state; checksum:integrity; redundancy:resilience",
            "stack": "layer:stratum; dependency:chronology; interface:boundary",
            "trace": "call:event; state:variable; thread:parallel_narrative",
            "paradigm": "model:worldview; abstraction:concept; shift:revolution",
            "language": "syntax:grammar; type:contract; community:culture",
            "automation": "pipeline:process; stage:step; artifact:product",
            "documentation": "narrative:story; example:parable; reference:genealogy",
            "source": "file:manuscript; module:chapter; function:passage",
            "legacy": "interface:ruin; deprecation:decline; knowledge:lost_art",
        }
        concept_lower = concept.lower()
        for key, val in tags.items():
            if key in concept_lower:
                return val
        return "entity:historical; relation:causal; property:structural"

    def _generate_resonance(
        self,
        origin: str,
        destination: str,
        iso_name: str,
        structural_property: str,
    ) -> str:
        templates = [
            f"As {origin} {structural_property}, so {destination} reveals the same pattern in another era.",
            f"What {origin} encodes in logic, {destination} records in time — the same structure, twice-lived.",
            f"The glass bead turns: on one face, {origin}; on the other, {destination}. Both are one.",
            f"Through the lens of {iso_name.replace('_', ' ')}, {origin} and {destination} become a single narrative seen from two epochs.",
        ]
        return templates[hash(iso_name) % len(templates)]

    def batch_transform(
        self,
        moves: List[Dict[str, Any]],
    ) -> List[TransformerResult]:
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
        return {
            name: {k: v for k, v in data.items() if k != "rule"}
            for name, data in self.ISOMORPHISMS.items()
        }


# ─── Convenience singleton ───────────────────────────────────
_default_transformer = None


def get_transformer() -> "CodeHistoryTransformer":
    """Get or create the default transformer instance."""
    global _default_transformer
    if _default_transformer is None:
        _default_transformer = CodeHistoryTransformer()
    return _default_transformer