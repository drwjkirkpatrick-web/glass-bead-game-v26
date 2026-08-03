"""
glass-bead-game-v26 — Bead Agent Skill Tree
Unlockable, reusable skills for each glass bead (Hermes agent) in the Game.

Each glass bead is an agent — a Hermes instance specialized for one of the
nine Castalian disciplines.  Agents begin with a CORE skill set (always
available) and unlock ADVANCED and MASTER skills as the player demonstrates
mastery through verified moves, contemplation hours, and peer endorsement.

Skills are REUSABLE: once unlocked, a skill can be invoked in any future
Glass Bead Game session.  Skills compose into custom TRACE PROGRAMS —
player-defined pipelines that chain bead agent operations across domains.

Hesse, *Das Glasperlenspiel*:
    "The Glass Bead Game was a mode of playing with the total contents
    and values of our culture..."
    Every bead-agent is a custodian of one facet of that culture.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from collections import defaultdict
import json


# ─── Skill Tier Enum ──────────────────────────────────────────

class SkillTier(Enum):
    """Three tiers of skills, unlocked progressively."""
    CORE = 0       # Always available — the bead's native disciplinary lens
    ADVANCED = 1   # Unlocked after 5 verified moves in this domain
    MASTER = 2     # Unlocked after 15 verified moves + 3 contemplation hours


# ─── Skill Dataclass ──────────────────────────────────────────

@dataclass
class BeadSkill:
    """A single unlockable skill belonging to a bead agent."""
    skill_id: str                          # unique e.g. "musica.harmonic_analysis"
    domain: str                            # e.g. "musica"
    tier: SkillTier                        # CORE, ADVANCED, or MASTER
    name: str                              # human-readable name
    description: str                       # what the skill does
    unlock_requirement: str                # human-readable unlock condition
    input_schema: Dict[str, str] = field(default_factory=dict)
    output_schema: Dict[str, str] = field(default_factory=dict)
    reusable: bool = True                  # all skills are reusable
    trace_compatible: bool = True          # can be used in trace programs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "domain": self.domain,
            "tier": self.tier.name,
            "name": self.name,
            "description": self.description,
            "unlock_requirement": self.unlock_requirement,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "reusable": self.reusable,
            "trace_compatible": self.trace_compatible,
        }


# ─── Skill Definitions (9 domains × 5 skills = 45 total) ─────

def _build_skill_catalog() -> Dict[str, List[BeadSkill]]:
    """
    Build the complete skill catalog for all 9 bead agents.
    Each domain has: 2 CORE, 2 ADVANCED, 1 MASTER = 5 skills.
    Total: 45 skills across 9 domains.
    """
    catalog: Dict[str, List[BeadSkill]] = {}

    # ── Musica ──────────────────────────────────────────────
    catalog["musica"] = [
        BeadSkill(
            skill_id="musica.refract",
            domain="musica", tier=SkillTier.CORE,
            name="Harmonic Refraction",
            description="Refract an incoming concept through musical vocabulary: map it to intervals, scales, and harmonic relationships.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "interval": "str", "confidence": "float"},
        ),
        BeadSkill(
            skill_id="musica.sonify",
            domain="musica", tier=SkillTier.CORE,
            name="Sonification",
            description="Convert a concept or transformation into a Web Audio API tone cluster with pitch, tempo, and harmonic mapping.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "domain": "str"},
            output_schema={"notes": "list[dict]", "bpm": "int"},
        ),
        BeadSkill(
            skill_id="musica.counterpoint",
            domain="musica", tier=SkillTier.ADVANCED,
            name="Contrapuntal Analysis",
            description="Analyze a concept as a fugue: identify subject, answer, countersubject, stretto, and episode structure.",
            unlock_requirement="5 verified moves involving musica",
            input_schema={"concept": "str", "structural_property": "str"},
            output_schema={"form": "str", "voices": "list[str]", "stretto_possible": "bool"},
        ),
        BeadSkill(
            skill_id="musica.motivic_transform",
            domain="musica", tier=SkillTier.ADVANCED,
            name="Motivic Transformation",
            description="Apply inversion, retrograde, augmentation, or diminution to a concept's structural motif.",
            unlock_requirement="5 verified moves involving musica",
            input_schema={"concept": "str", "transform_type": "str"},
            output_schema={"transformed_concept": "str", "interval_mapping": "str"},
        ),
        BeadSkill(
            skill_id="musica.composition_engine",
            domain="musica", tier=SkillTier.MASTER,
            name="Algorithmic Composition",
            description="Generate a complete compositional arc (theme → countersubject → episode → stretto → coda) from a cross-domain concept.",
            unlock_requirement="15 verified moves + 3 contemplation hours in musica",
            input_schema={"theme_concept": "str", "domain": "str"},
            output_schema={"fugue_structure": "dict", "narrative": "str"},
        ),
    ]

    # ── Mathematica ─────────────────────────────────────────
    catalog["mathematica"] = [
        BeadSkill(
            skill_id="mathematica.refract",
            domain="mathematica", tier=SkillTier.CORE,
            name="Formal Refraction",
            description="Refract an incoming concept through mathematical vocabulary: identify its algebraic, topological, and analytic structure.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "structure_type": "str", "confidence": "float"},
        ),
        BeadSkill(
            skill_id="mathematica.prove",
            domain="mathematica", tier=SkillTier.CORE,
            name="Structural Proof Check",
            description="Verify whether a claimed structural correspondence between two domains satisfies formal isomorphism criteria.",
            unlock_requirement="Always available",
            input_schema={"claim": "str", "domain_a": "str", "domain_b": "str"},
            output_schema={"valid": "bool", "reason": "str", "formal_rule": "str"},
        ),
        BeadSkill(
            skill_id="mathematica.symmetry",
            domain="mathematica", tier=SkillTier.ADVANCED,
            name="Symmetry Analysis",
            description="Identify the symmetry group (cyclic, dihedral, etc.) underlying a concept and map it to a transformation family.",
            unlock_requirement="5 verified moves involving mathematica",
            input_schema={"concept": "str"},
            output_schema={"group": "str", "order": "int", "generators": "list[str]"},
        ),
        BeadSkill(
            skill_id="mathematica.recursive_decompose",
            domain="mathematica", tier=SkillTier.ADVANCED,
            name="Recursive Decomposition",
            description="Decompose a concept into its recursive structure: base case, inductive step, and self-referential depth.",
            unlock_requirement="5 verified moves involving mathematica",
            input_schema={"concept": "str"},
            output_schema={"base_case": "str", "inductive_step": "str", "depth": "int"},
        ),
        BeadSkill(
            skill_id="mathematica.isomorphism_engine",
            domain="mathematica", tier=SkillTier.MASTER,
            name="Isomorphism Discovery",
            description="Search the full isomorphism library for the deepest formal correspondence between two arbitrary concepts across any domains.",
            unlock_requirement="15 verified moves + 3 contemplation hours in mathematica",
            input_schema={"concept_a": "str", "concept_b": "str", "domain_a": "str", "domain_b": "str"},
            output_schema={"isomorphism": "str", "rule": "str", "confidence": "float", "depth": "int"},
        ),
    ]

    # ── Historia ────────────────────────────────────────────
    catalog["historia"] = [
        BeadSkill(
            skill_id="historia.refract",
            domain="historia", tier=SkillTier.CORE,
            name="Historical Refraction",
            description="Refract a concept through historical vocabulary: place it in a timeline, identify precedents and consequences.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "era": "str", "precedent": "str"},
        ),
        BeadSkill(
            skill_id="historia.chronicle",
            domain="historia", tier=SkillTier.CORE,
            name="Chronicle",
            description="Record a move as a historical chronicle entry with proper provenance and temporal context.",
            unlock_requirement="Always available",
            input_schema={"move": "dict"},
            output_schema={"entry": "str", "timestamp": "str", "provenance": "str"},
        ),
        BeadSkill(
            skill_id="historia.dialectic",
            domain="historia", tier=SkillTier.ADVANCED,
            name="Dialectical Analysis",
            description="Analyze a concept as a Hegelian dialectic: thesis, antithesis, synthesis — the historical progression of ideas.",
            unlock_requirement="5 verified moves involving historia",
            input_schema={"concept": "str", "opposing_concept": "str"},
            output_schema={"thesis": "str", "antithesis": "str", "synthesis": "str"},
        ),
        BeadSkill(
            skill_id="historia.renaissance",
            domain="historia", tier=SkillTier.ADVANCED,
            name="Renaissance Pattern",
            description="Identify periods of cultural rebirth and synthesis — when old ideas return transformed by new context.",
            unlock_requirement="5 verified moves involving historia",
            input_schema={"concepts": "list[str]"},
            output_schema={"pattern": "str", "rebirth_indicators": "list[str]"},
        ),
        BeadSkill(
            skill_id="historia.dark_age_recovery",
            domain="historia", tier=SkillTier.MASTER,
            name="Dark Age Recovery",
            description="Identify lost knowledge patterns and reconstruct bridging concepts across historical discontinuities.",
            unlock_requirement="15 verified moves + 3 contemplation hours in historia",
            input_schema={"concept_before": "str", "concept_after": "str"},
            output_schema={"lost_knowledge": "str", "reconstruction": "str", "plausibility": "float"},
        ),
    ]

    # ── Natura ──────────────────────────────────────────────
    catalog["natura"] = [
        BeadSkill(
            skill_id="natura.refract",
            domain="natura", tier=SkillTier.CORE,
            name="Natural Refraction",
            description="Refract a concept through the vocabulary of natural sciences: physics, biology, ecology, chemistry.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "natural_analogue": "str", "confidence": "float"},
        ),
        BeadSkill(
            skill_id="natura.classify",
            domain="natura", tier=SkillTier.CORE,
            name="Taxonomic Classification",
            description="Classify a concept into a natural hierarchy: kingdom, phylum, class — the Linnaean structure of ideas.",
            unlock_requirement="Always available",
            input_schema={"concept": "str"},
            output_schema={"kingdom": "str", "phylum": "str", "class": "str"},
        ),
        BeadSkill(
            skill_id="natura.evolve",
            domain="natura", tier=SkillTier.ADVANCED,
            name="Evolutionary Model",
            description="Model how a concept might evolve under natural selection pressure: variation, selection, retention.",
            unlock_requirement="5 verified moves involving natura",
            input_schema={"concept": "str", "selection_pressure": "str"},
            output_schema={"variations": "list[str]", "fittest": "str", "retention": "str"},
        ),
        BeadSkill(
            skill_id="natura.fractal",
            domain="natura", tier=SkillTier.ADVANCED,
            name="Fractal Self-Similarity",
            description="Identify self-similar patterns in a concept that repeat at different scales — the natural fractal geometry.",
            unlock_requirement="5 verified moves involving natura",
            input_schema={"concept": "str"},
            output_schema={"pattern": "str", "scales": "list[str]", "hausdorff_dim": "float"},
        ),
        BeadSkill(
            skill_id="natura.ecosystem",
            domain="natura", tier=SkillTier.MASTER,
            name="Ecosystem Mapping",
            description="Map an entire knowledge ecosystem: producers, consumers, decomposers — the ecological web of concepts.",
            unlock_requirement="15 verified moves + 3 contemplation hours in natura",
            input_schema={"concepts": "list[str]", "domain": "str"},
            output_schema={"trophic_levels": "dict", "keystone_concepts": "list[str]", "stability": "float"},
        ),
    ]

    # ── Lingua ──────────────────────────────────────────────
    catalog["lingua"] = [
        BeadSkill(
            skill_id="lingua.refract",
            domain="lingua", tier=SkillTier.CORE,
            name="Linguistic Refraction",
            description="Refract a concept through linguistic vocabulary: syntax, semantics, pragmatics, morphology.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "syntactic_role": "str", "semantic_field": "str"},
        ),
        BeadSkill(
            skill_id="lingua.parse",
            domain="lingua", tier=SkillTier.CORE,
            name="Parse Tree Construction",
            description="Construct a syntactic parse tree of a concept's structural components — the grammar of ideas.",
            unlock_requirement="Always available",
            input_schema={"concept": "str"},
            output_schema={"tree": "dict", "terminals": "list[str]", "nonterminals": "list[str]"},
        ),
        BeadSkill(
            skill_id="lingua.translate",
            domain="lingua", tier=SkillTier.ADVANCED,
            name="Cross-Domain Translation",
            description="Translate a concept from one domain's jargon into another's, preserving structural meaning while changing surface form.",
            unlock_requirement="5 verified moves involving lingua",
            input_schema={"concept": "str", "from_domain": "str", "to_domain": "str"},
            output_schema={"translation": "str", "cognates": "list[str]", "false_friends": "list[str]"},
        ),
        BeadSkill(
            skill_id="lingua.etymologize",
            domain="lingua", tier=SkillTier.ADVANCED,
            name="Etymological Tracing",
            description="Trace a concept's etymology across domains: root forms, semantic shifts, and borrowed structures.",
            unlock_requirement="5 verified moves involving lingua",
            input_schema={"concept": "str"},
            output_schema={"root": "str", "cognates": "list[str]", "semantic_shift": "str"},
        ),
        BeadSkill(
            skill_id="lingua.semantic_engine",
            domain="lingua", tier=SkillTier.MASTER,
            name="Semantic Field Mapping",
            description="Map the complete semantic field around a concept — every meaning, connotation, and contextual register.",
            unlock_requirement="15 verified moves + 3 contemplation hours in lingua",
            input_schema={"concept": "str", "context": "str"},
            output_schema={"field": "dict", "connotations": "list[str]", "register": "str"},
        ),
    ]

    # ── Philosophia ─────────────────────────────────────────
    catalog["philosophia"] = [
        BeadSkill(
            skill_id="philosophia.refract",
            domain="philosophia", tier=SkillTier.CORE,
            name="Philosophical Refraction",
            description="Refract a concept through philosophical vocabulary: ontology, epistemology, ethics, aesthetics.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "branch": "str", "confidence": "float"},
        ),
        BeadSkill(
            skill_id="philosophia.dialectic",
            domain="philosophia", tier=SkillTier.CORE,
            name="Socratic Dialectic",
            description="Engage a concept through Socratic questioning: elenchus, aporia, and the pursuit of definition.",
            unlock_requirement="Always available",
            input_schema={"concept": "str"},
            output_schema={"questions": "list[str]", "aporia": "str", "definition": "str"},
        ),
        BeadSkill(
            skill_id="philosophia.phenomenology",
            domain="philosophia", tier=SkillTier.ADVANCED,
            name="Phenomenological Reduction",
            description="Apply epoché to a concept: bracket assumptions, attend to lived experience, describe the phenomenon as it appears.",
            unlock_requirement="5 verified moves involving philosophia",
            input_schema={"concept": "str"},
            output_schema={"bracketed": "list[str]", "noema": "str", "noesis": "str"},
        ),
        BeadSkill(
            skill_id="philosophia.ethical_eval",
            domain="philosophia", tier=SkillTier.ADVANCED,
            name="Ethical Evaluation",
            description="Evaluate a concept through ethical frameworks: deontological, consequentialist, virtue-based.",
            unlock_requirement="5 verified moves involving philosophia",
            input_schema={"concept": "str", "context": "str"},
            output_schema={"deontological": "str", "consequentialist": "str", "virtue": "str"},
        ),
        BeadSkill(
            skill_id="philosophia.synthesis_engine",
            domain="philosophia", tier=SkillTier.MASTER,
            name="Hegelian Synthesis",
            description="Find the Aufhebung — the synthesis that preserves and elevates two opposing concepts into a higher unity.",
            unlock_requirement="15 verified moves + 3 contemplation hours in philosophia",
            input_schema={"thesis": "str", "antithesis": "str"},
            output_schema={"synthesis": "str", "preserved": "list[str]", "elevated": "str"},
        ),
    ]

    # ── Technologia ─────────────────────────────────────────
    catalog["technologia"] = [
        BeadSkill(
            skill_id="technologia.refract",
            domain="technologia", tier=SkillTier.CORE,
            name="Technological Refraction",
            description="Refract a concept through engineering vocabulary: systems, interfaces, protocols, and material constraints.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "system_type": "str", "confidence": "float"},
        ),
        BeadSkill(
            skill_id="technologia.optimize",
            domain="technologia", tier=SkillTier.CORE,
            name="Optimization Analysis",
            description="Analyze a concept for efficiency: identify bottlenecks, resource costs, and optimization opportunities.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "context": "str"},
            output_schema={"bottlenecks": "list[str]", "complexity": "str", "optimal": "str"},
        ),
        BeadSkill(
            skill_id="technologia.architect",
            domain="technologia", tier=SkillTier.ADVANCED,
            name="System Architecture",
            description="Design a system architecture for a concept: components, interfaces, data flow, and failure modes.",
            unlock_requirement="5 verified moves involving technologia",
            input_schema={"concept": "str"},
            output_schema={"components": "list[dict]", "interfaces": "list[str]", "failure_modes": "list[str]"},
        ),
        BeadSkill(
            skill_id="technologia.protocol",
            domain="technologia", tier=SkillTier.ADVANCED,
            name="Protocol Design",
            description="Design a communication protocol between two domain agents: handshake, message format, error handling.",
            unlock_requirement="5 verified moves involving technologia",
            input_schema={"domain_a": "str", "domain_b": "str"},
            output_schema={"handshake": "str", "message_format": "dict", "error_handling": "str"},
        ),
        BeadSkill(
            skill_id="technologia.full_stack",
            domain="technologia", tier=SkillTier.MASTER,
            name="Full-Stack Integration",
            description="Integrate all 9 domain agents into a single coherent system with end-to-end data flow.",
            unlock_requirement="15 verified moves + 3 contemplation hours in technologia",
            input_schema={"domains": "list[str]", "goal": "str"},
            output_schema={"architecture": "dict", "data_flow": "str", "integration_points": "list[str]"},
        ),
    ]

    # ── Medicina ────────────────────────────────────────────
    catalog["medicina"] = [
        BeadSkill(
            skill_id="medicina.refract",
            domain="medicina", tier=SkillTier.CORE,
            name="Medical Refraction",
            description="Refract a concept through medical vocabulary: diagnosis, pathology, treatment, and physiological systems.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "system_affected": "str", "confidence": "float"},
        ),
        BeadSkill(
            skill_id="medicina.diagnose",
            domain="medicina", tier=SkillTier.CORE,
            name="Diagnostic Pattern",
            description="Identify the diagnostic pattern in a concept: symptoms, signs, differential diagnosis, and clinical reasoning.",
            unlock_requirement="Always available",
            input_schema={"concept": "str"},
            output_schema={"symptoms": "list[str]", "differential": "list[str]", "diagnosis": "str"},
        ),
        BeadSkill(
            skill_id="medicina.homeostasis",
            domain="medicina", tier=SkillTier.ADVANCED,
            name="Homeostatic Analysis",
            description="Analyze a concept as a homeostatic feedback loop: set point, sensor, controller, effector, and perturbation.",
            unlock_requirement="5 verified moves involving medicina",
            input_schema={"concept": "str"},
            output_schema={"set_point": "str", "feedback_loop": "str", "perturbation": "str"},
        ),
        BeadSkill(
            skill_id="medicina.vital_signs",
            domain="medicina", tier=SkillTier.ADVANCED,
            name="Vital Signs Monitor",
            description="Monitor the 'vital signs' of a knowledge graph: density (blood pressure), connectivity (heart rate), novelty (oxygen).",
            unlock_requirement="5 verified moves involving medicina",
            input_schema={"graph": "dict"},
            output_schema={"density": "float", "connectivity": "float", "novelty": "float", "diagnosis": "str"},
        ),
        BeadSkill(
            skill_id="medicina.treatment_plan",
            domain="medicina", tier=SkillTier.MASTER,
            name="Treatment Protocol",
            description="Design a treatment protocol for an ailing knowledge graph: interventions, dosing, prognosis, and follow-up.",
            unlock_requirement="15 verified moves + 3 contemplation hours in medicina",
            input_schema={"graph": "dict", "diagnosis": "str"},
            output_schema={"interventions": "list[dict]", "prognosis": "str", "follow_up": "str"},
        ),
    ]

    # ── Coda (Computer Code) ────────────────────────────────
    catalog["coda"] = [
        BeadSkill(
            skill_id="coda.refract",
            domain="coda", tier=SkillTier.CORE,
            name="Code Refraction",
            description="Refract a concept through programming vocabulary: algorithms, data structures, complexity, and design patterns.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "source_domain": "str"},
            output_schema={"translation": "str", "pattern": "str", "complexity": "str"},
        ),
        BeadSkill(
            skill_id="coda.compile",
            domain="coda", tier=SkillTier.CORE,
            name="Concept Compilation",
            description="Compile a cross-domain concept into an executable trace: parse, type-check, optimize, and emit a transformation pipeline.",
            unlock_requirement="Always available",
            input_schema={"concept": "str", "domain": "str"},
            output_schema={"ast": "dict", "optimized": "str", "pipeline": "list[str]"},
        ),
        BeadSkill(
            skill_id="coda.debug",
            domain="coda", tier=SkillTier.ADVANCED,
            name="Debug & Trace",
            description="Debug a failed correspondence: set breakpoints, inspect the transformation at each stage, identify where the isomorphism breaks.",
            unlock_requirement="5 verified moves involving coda",
            input_schema={"failed_move": "dict"},
            output_schema={"breakpoint": "str", "root_cause": "str", "fix": "str"},
        ),
        BeadSkill(
            skill_id="coda.refactor",
            domain="coda", tier=SkillTier.ADVANCED,
            name="Concept Refactoring",
            description="Refactor a concept's structure: extract shared interfaces, rename for clarity, simplify without changing meaning.",
            unlock_requirement="5 verified moves involving coda",
            input_schema={"concept": "str", "target_domains": "list[str]"},
            output_schema={"refactored": "str", "extracted_interface": "str", "simplification": "str"},
        ),
        BeadSkill(
            skill_id="coda.trace_program",
            domain="coda", tier=SkillTier.MASTER,
            name="Trace Program Builder",
            description="Build a custom reusable trace program: a player-defined pipeline that chains bead agent skills across multiple domains.",
            unlock_requirement="15 verified moves + 3 contemplation hours in coda",
            input_schema={"steps": "list[dict]", "name": "str"},
            output_schema={"program_id": "str", "pipeline": "list[dict]", "reusable": "bool"},
        ),
    ]

    return catalog


# ─── Skill Tree Manager ───────────────────────────────────────

class SkillTree:
    """
    Manages skill unlocking, querying, and trace program construction
    for all 9 bead agents.

    A player's skill tree is driven by their PlayerIdentity:
      - verified_moves: total count
      - domain_mastery: {domain: float} — 0.0 to 1.0
      - contemplation_hours: total hours
      - peer_endorsements: count

    Unlock rules:
      CORE:      always unlocked
      ADVANCED:  ≥5 verified moves involving that domain
                 (domain_mastery[domain] >= 0.3)
      MASTER:    ≥15 verified moves involving that domain
                 + ≥3 contemplation hours in that domain
                 (domain_mastery[domain] >= 0.7)
    """

    ALL_SKILLS: Dict[str, List[BeadSkill]] = _build_skill_catalog()

    def __init__(self):
        self._unlocked: Set[str] = set()  # skill_ids
        self._trace_programs: Dict[str, Dict[str, Any]] = {}

    def evaluate_unlocks(
        self,
        verified_moves: int = 0,
        domain_mastery: Optional[Dict[str, float]] = None,
        contemplation_hours: float = 0.0,
        domain_contemplation: Optional[Dict[str, float]] = None,
    ) -> Set[str]:
        """
        Evaluate which skills should be unlocked given player stats.
        Returns the set of unlocked skill_ids.
        """
        domain_mastery = domain_mastery or {}
        domain_contemplation = domain_contemplation or {}
        unlocked = set()

        for domain, skills in self.ALL_SKILLS.items():
            mastery = domain_mastery.get(domain, 0.0)
            cont_hours = domain_contemplation.get(domain, 0.0)

            for skill in skills:
                if skill.tier == SkillTier.CORE:
                    unlocked.add(skill.skill_id)
                elif skill.tier == SkillTier.ADVANCED:
                    if mastery >= 0.3:
                        unlocked.add(skill.skill_id)
                elif skill.tier == SkillTier.MASTER:
                    if mastery >= 0.7 and cont_hours >= 3.0:
                        unlocked.add(skill.skill_id)

        self._unlocked = unlocked
        return unlocked

    def get_unlocked_skills(self, domain: Optional[str] = None) -> List[BeadSkill]:
        """Return all unlocked skills, optionally filtered by domain."""
        result = []
        for dom, skills in self.ALL_SKILLS.items():
            if domain and dom != domain:
                continue
            for skill in skills:
                if skill.skill_id in self._unlocked:
                    result.append(skill)
        return result

    def get_locked_skills(self, domain: Optional[str] = None) -> List[BeadSkill]:
        """Return skills not yet unlocked, optionally filtered by domain."""
        result = []
        for dom, skills in self.ALL_SKILLS.items():
            if domain and dom != domain:
                continue
            for skill in skills:
                if skill.skill_id not in self._unlocked:
                    result.append(skill)
        return result

    def get_skills_by_domain(self, domain: str) -> List[BeadSkill]:
        """Return all skills (locked + unlocked) for a domain."""
        return list(self.ALL_SKILLS.get(domain, []))

    def get_skill(self, skill_id: str) -> Optional[BeadSkill]:
        """Look up a single skill by ID."""
        for skills in self.ALL_SKILLS.values():
            for skill in skills:
                if skill.skill_id == skill_id:
                    return skill
        return None

    def is_unlocked(self, skill_id: str) -> bool:
        """Check if a specific skill is unlocked."""
        return skill_id in self._unlocked

    def get_tree_overview(self) -> Dict[str, Any]:
        """
        Return a full tree overview grouped by domain, showing
        locked/unlocked status and tier for each skill.
        """
        overview = {}
        for domain, skills in self.ALL_SKILLS.items():
            overview[domain] = {
                "total": len(skills),
                "unlocked": sum(1 for s in skills if s.skill_id in self._unlocked),
                "tiers": {
                    "CORE": sum(1 for s in skills if s.tier == SkillTier.CORE),
                    "ADVANCED": sum(1 for s in skills if s.tier == SkillTier.ADVANCED),
                    "MASTER": sum(1 for s in skills if s.tier == SkillTier.MASTER),
                },
                "skills": [
                    {
                        **s.to_dict(),
                        "unlocked": s.skill_id in self._unlocked,
                    }
                    for s in skills
                ],
            }
        return overview

    # ─── Trace Programs ─────────────────────────────────────

    def create_trace_program(
        self,
        name: str,
        steps: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Create a reusable trace program — a pipeline of bead skills.

        Each step: {skill_id, input_mapping: {param: source}}
        where source is either a literal value or "step[N].output[param]".

        Returns the program definition.  All skills referenced must be
        unlocked for the program to execute.
        """
        program_id = f"trace_{name.lower().replace(' ', '_')}_{len(self._trace_programs)}"

        # Validate all skills exist and are trace_compatible
        validated_steps = []
        for i, step in enumerate(steps):
            skill_id = step.get("skill_id", "")
            skill = self.get_skill(skill_id)
            if not skill:
                raise ValueError(f"Step {i}: unknown skill '{skill_id}'")
            if not skill.trace_compatible:
                raise ValueError(f"Step {i}: skill '{skill_id}' is not trace-compatible")
            validated_steps.append({
                "step_index": i,
                "skill_id": skill_id,
                "skill_name": skill.name,
                "domain": skill.domain,
                "input_mapping": step.get("input_mapping", {}),
                "unlocked": self.is_unlocked(skill_id),
            })

        program = {
            "program_id": program_id,
            "name": name,
            "steps": validated_steps,
            "total_steps": len(validated_steps),
            "all_unlocked": all(s["unlocked"] for s in validated_steps),
            "reusable": True,
        }
        self._trace_programs[program_id] = program
        return program

    def get_trace_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a saved trace program."""
        return self._trace_programs.get(program_id)

    def list_trace_programs(self) -> List[Dict[str, Any]]:
        """List all saved trace programs."""
        return list(self._trace_programs.values())

    def execute_trace_program(
        self,
        program_id: str,
        initial_inputs: Dict[str, Any],
        skill_executor: Callable,
    ) -> Dict[str, Any]:
        """
        Execute a trace program by running each skill in sequence.

        skill_executor: a callable (skill_id, inputs) -> dict that
        dispatches to the appropriate bead agent function.

        Returns the full trace with each step's input and output.
        """
        program = self.get_trace_program(program_id)
        if not program:
            return {"error": f"Unknown trace program: {program_id}"}
        if not program["all_unlocked"]:
            locked = [s["skill_id"] for s in program["steps"] if not s["unlocked"]]
            return {"error": f"Locked skills in program: {locked}"}

        context = dict(initial_inputs)
        trace = []

        for step in program["steps"]:
            # Resolve input mappings from context
            step_inputs = {}
            for param, source in step.get("input_mapping", {}).items():
                if isinstance(source, str) and source.startswith("step["):
                    # Reference to previous step output
                    # Format: step[N].output[key]
                    parts = source.replace("step[", "").replace("]", "").split(".output.")
                    if len(parts) == 2:
                        step_idx = int(parts[0])
                        key = parts[1]
                        if step_idx < len(trace):
                            step_inputs[param] = trace[step_idx]["output"].get(key, "")
                        else:
                            step_inputs[param] = ""
                    else:
                        step_inputs[param] = source
                else:
                    # Literal value or context reference
                    step_inputs[param] = context.get(source, source)

            # Execute skill
            output = skill_executor(step["skill_id"], step_inputs)
            trace.append({
                "step_index": step["step_index"],
                "skill_id": step["skill_id"],
                "skill_name": step["skill_name"],
                "domain": step["domain"],
                "input": step_inputs,
                "output": output,
            })

            # Store output in context for later steps
            context[f"step[{step['step_index']}].output"] = output

        return {
            "program_id": program_id,
            "name": program["name"],
            "trace": trace,
            "final_output": trace[-1]["output"] if trace else {},
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the full skill tree state."""
        return {
            "total_skills": sum(len(skills) for skills in self.ALL_SKILLS.values()),
            "unlocked_count": len(self._unlocked),
            "domains": list(self.ALL_SKILLS.keys()),
            "tree": self.get_tree_overview(),
            "trace_programs": list(self._trace_programs.values()),
        }


# ─── Convenience singleton ────────────────────────────────────

_default_tree: Optional[SkillTree] = None


def get_skill_tree() -> SkillTree:
    """Get or create the default SkillTree instance."""
    global _default_tree
    if _default_tree is None:
        _default_tree = SkillTree()
    return _default_tree