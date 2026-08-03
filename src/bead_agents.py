"""
glass-bead-game-v26 — Bead Agents
Agent functions for each of the 9 glass bead (Hermes agent) locations.

Each bead agent is a specialized disciplinary intelligence that:
  1. Receives concepts cast from other domains
  2. Refracts them through its native disciplinary lens
  3. Maps cross-domain tension to a musical interval
  4. Rates confidence and austerity of the analogy
  5. Can invoke domain-specific skills from the SkillTree

Agents are stateless within a session — their skill unlocks are managed
by the SkillTree, which persists across sessions via PlayerIdentity.

Hesse: "Each bead is a custodian of one facet of culture."
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum

from src.bead_skills import SkillTree, SkillTier, get_skill_tree


# ─── Bead Agent Dataclass ─────────────────────────────────────

@dataclass
class BeadAgent:
    """A single glass bead agent at one domain location."""
    domain: str               # e.g. "musica"
    name: str                 # e.g. "Magister Musicae"
    color: str                # hex color
    icon: str                 # single-char icon
    skills: List[str] = field(default_factory=list)  # skill_ids

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "name": self.name,
            "color": self.color,
            "icon": self.icon,
            "skill_count": len(self.skills),
            "skills": self.skills,
        }


# ─── Bead Agent Registry ──────────────────────────────────────

BEAD_AGENTS: Dict[str, BeadAgent] = {
    "musica": BeadAgent(
        domain="musica", name="Magister Musicae",
        color="#00e5ff", icon="♪",
        skills=["musica.refract", "musica.sonify", "musica.counterpoint",
                "musica.motivic_transform", "musica.composition_engine"],
    ),
    "mathematica": BeadAgent(
        domain="mathematica", name="Magister Mathematicae",
        color="#ff00ff", icon="∑",
        skills=["mathematica.refract", "mathematica.prove", "mathematica.symmetry",
                "mathematica.recursive_decompose", "mathematica.isomorphism_engine"],
    ),
    "historia": BeadAgent(
        domain="historia", name="Magister Historiae",
        color="#ffd700", icon="⌛",
        skills=["historia.refract", "historia.chronicle", "historia.dialectic",
                "historia.renaissance", "historia.dark_age_recovery"],
    ),
    "natura": BeadAgent(
        domain="natura", name="Magister Naturae",
        color="#00ff7f", icon="⚛",
        skills=["natura.refract", "natura.classify", "natura.evolve",
                "natura.fractal", "natura.ecosystem"],
    ),
    "lingua": BeadAgent(
        domain="lingua", name="Magister Linguae",
        color="#ff6b6b", icon="✎",
        skills=["lingua.refract", "lingua.parse", "lingua.translate",
                "lingua.etymologize", "lingua.semantic_engine"],
    ),
    "philosophia": BeadAgent(
        domain="philosophia", name="Magister Philosophiae",
        color="#9370db", icon="◊",
        skills=["philosophia.refract", "philosophia.dialectic", "philosophia.phenomenology",
                "philosophia.ethical_eval", "philosophia.synthesis_engine"],
    ),
    "technologia": BeadAgent(
        domain="technologia", name="Magister Technologiae",
        color="#ffa500", icon="⚙",
        skills=["technologia.refract", "technologia.optimize", "technologia.architect",
                "technologia.protocol", "technologia.full_stack"],
    ),
    "medicina": BeadAgent(
        domain="medicina", name="Magister Medicinae",
        color="#ff69b4", icon="✚",
        skills=["medicina.refract", "medicina.diagnose", "medicina.homeostasis",
                "medicina.vital_signs", "medicina.treatment_plan"],
    ),
    "coda": BeadAgent(
        domain="coda", name="Magister Codae",
        color="#39ff14", icon="⌘",
        skills=["coda.refract", "coda.compile", "coda.debug",
                "coda.refactor", "coda.trace_program"],
    ),
}


# ─── Agent Skill Executors ────────────────────────────────────

def _refract_generic(concept: str, source_domain: str, target_domain: str,
                     vocabulary: Dict[str, List[str]]) -> Dict[str, Any]:
    """Generic refraction logic used by all bead agents."""
    concept_lower = concept.lower()
    domain_vocab = vocabulary.get(target_domain, [])

    # Score domain terms against the concept
    matched_terms = [term for term in domain_vocab if term in concept_lower]
    confidence = min(0.99, 0.5 + 0.1 * len(matched_terms))

    return {
        "translation": f"{concept} refracted through {target_domain}",
        "matched_terms": matched_terms,
        "confidence": round(confidence, 3),
        "austerity": round(0.5 + 0.05 * (5 - min(len(matched_terms), 5)), 3),
    }


# Domain vocabulary for refraction
_DOMAIN_VOCAB = {
    "musica": ["harmony", "counterpoint", "fugue", "canon", "interval", "scale",
               "tonic", "dominant", "pitch", "rhythm", "chord", "voice", "theme",
               "motif", "crescendo", "diminuendo", "sonata", "concerto", "overture"],
    "mathematica": ["group", "ring", "field", "topology", "manifold", "function",
                    "theorem", "proof", "axiom", "eigenvalue", "matrix", "vector",
                    "category", "functor", "homomorphism", "isomorphism", "graph",
                    "set", "sequence", "limit", "convergence", "operator"],
    "historia": ["empire", "revolution", "renaissance", "dynasty", "chronicle",
                 "era", "epoch", "civilization", "barbarian", "enlightenment",
                 "reformation", "colonial", "feudal", "guild", "republic"],
    "natura": ["evolution", "ecosystem", "organism", "cell", "gene", "species",
               "mutation", "adaptation", "symbiosis", "photosynthesis", "fractal",
               "crystal", "wave", "particle", "entropy", "energy", "field",
               "quantum", "relativity", "DNA", "protein"],
    "lingua": ["syntax", "semantics", "phonology", "morphology", "pragmatics",
               "grammar", "lexicon", "phoneme", "morpheme", "dialect", "creole",
               "etymology", "cognate", "syntax tree", "parse", "corpus"],
    "philosophia": ["ontology", "epistemology", "ethics", "aesthetics", "dialectic",
                    "phenomenology", "existential", "metaphysics", "logic", "truth",
                    "being", "consciousness", "virtue", "telos", "aufhebung",
                    "aporia", "elenchus", "categorical", "imperative"],
    "technologia": ["system", "circuit", "protocol", "interface", "architecture",
                    "algorithm", "compiler", "kernel", "network", "encryption",
                    "optimization", "pipeline", "framework", "hardware", "software",
                    "debug", "deploy", "scale", "throughput", "latency"],
    "medicina": ["diagnosis", "symptom", "pathology", "treatment", "prognosis",
                 "homeostasis", "immunity", "inflammation", "metabolism", "neuron",
                 "hormone", "receptor", "antibody", "therapy", "differential",
                 "clinical", "epidemiology", "vital", "lesion", "syndrome"],
    "coda": ["function", "class", "algorithm", "recursion", "compile", "debug",
             "refactor", "variable", "pointer", "stack", "queue", "tree", "graph",
             "sort", "search", "optimize", "complexity", "pattern", "interface",
             "inheritance", "polymorphism", "encapsulation", "concurrency"],
}


# ─── Skill Execution Dispatcher ───────────────────────────────

def execute_skill(skill_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a single bead agent skill by its skill_id.
    This is the central dispatcher used by the trace program executor.
    """
    tree = get_skill_tree()
    skill = tree.get_skill(skill_id)
    if not skill:
        return {"error": f"Unknown skill: {skill_id}"}
    if not tree.is_unlocked(skill_id):
        return {"error": f"Skill not unlocked: {skill_id}"}

    # Dispatch to domain-specific executor
    domain = skill.domain
    executor = _SKILL_EXECUTORS.get(skill_id, _generic_executor)
    return executor(skill, inputs)


def _generic_executor(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback executor for skills without a specific handler."""
    return {
        "skill_id": skill.skill_id,
        "skill_name": skill.name,
        "domain": skill.domain,
        "status": "executed",
        "inputs": inputs,
        "output": {
            "message": f"Skill '{skill.name}' executed with provided inputs.",
            "note": "Domain-specific logic should be implemented for full execution.",
        },
    }


# ─── Domain-Specific Skill Executors ──────────────────────────

def _musica_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "musica", _DOMAIN_VOCAB)
    # Map to musical interval based on domain distance
    interval_map = {0: "unison", 1: "minor second", 2: "major second",
                    3: "perfect fourth", 4: "tritone", 5: "perfect fifth",
                    6: "minor seventh", 7: "octave", 8: "major seventh"}
    domain_list = list(BEAD_AGENTS.keys())
    dist = abs(domain_list.index("musica") - domain_list.index(source_domain)) if source_domain in domain_list else 4
    result["interval"] = interval_map.get(min(dist, 8), "tritone")
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "musica",
            "status": "executed", "output": result}


def _musica_sonify(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    domain = inputs.get("domain", "")
    domain_list = list(BEAD_AGENTS.keys())
    domain_idx = domain_list.index(domain) if domain in domain_list else 0
    base_pitch = 60 + domain_idx * 4
    return {
        "skill_id": skill.skill_id, "skill_name": skill.name, "domain": "musica",
        "status": "executed",
        "output": {
            "notes": [
                {"pitch": base_pitch, "duration": 1.0, "velocity": 0.7},
                {"pitch": base_pitch + 7, "duration": 1.5, "velocity": 0.8},
                {"pitch": base_pitch + 12, "duration": 2.0, "velocity": 0.6},
            ],
            "bpm": 60 + len(concept) % 60,
            "concept": concept,
        },
    }


def _mathematica_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "mathematica", _DOMAIN_VOCAB)
    # Identify structure type
    structure_types = []
    if any(w in concept.lower() for w in ["group", "symmetry", "rotation"]):
        structure_types.append("algebraic")
    if any(w in concept.lower() for w in ["space", "surface", "manifold", "topology"]):
        structure_types.append("topological")
    if any(w in concept.lower() for w in ["function", "series", "limit", "integral"]):
        structure_types.append("analytic")
    if any(w in concept.lower() for w in ["graph", "tree", "network"]):
        structure_types.append("combinatorial")
    result["structure_type"] = " + ".join(structure_types) if structure_types else "abstract"
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "mathematica",
            "status": "executed", "output": result}


def _mathematica_prove(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    claim = inputs.get("claim", "")
    domain_a = inputs.get("domain_a", "")
    domain_b = inputs.get("domain_b", "")
    # Check if domains differ
    valid = domain_a != domain_b and bool(claim)
    return {
        "skill_id": skill.skill_id, "skill_name": skill.name, "domain": "mathematica",
        "status": "executed",
        "output": {
            "valid": valid,
            "reason": "Domains differ and claim is non-empty" if valid else "Invalid: same domain or empty claim",
            "formal_rule": "Isomorphism requires: (1) distinct domains, (2) non-trivial mapping, (3) structure preservation",
        },
    }


def _coda_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "coda", _DOMAIN_VOCAB)
    # Identify design pattern
    patterns = []
    if any(w in concept.lower() for w in ["recursion", "self", "nested"]):
        patterns.append("recursive")
    if any(w in concept.lower() for w in ["object", "class", "encapsul"]):
        patterns.append("object-oriented")
    if any(w in concept.lower() for w in ["function", "pure", "immutable"]):
        patterns.append("functional")
    if any(w in concept.lower() for w in ["state", "machine", "transition"]):
        patterns.append("state-driven")
    result["pattern"] = " + ".join(patterns) if patterns else "procedural"
    result["complexity"] = "O(n)" if len(concept) < 50 else "O(n log n)"
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "coda",
            "status": "executed", "output": result}


def _coda_compile(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    domain = inputs.get("domain", "")
    return {
        "skill_id": skill.skill_id, "skill_name": skill.name, "domain": "coda",
        "status": "executed",
        "output": {
            "ast": {"type": "ConceptNode", "value": concept, "domain": domain},
            "optimized": f"refactored({concept})",
            "pipeline": ["parse", "type-check", "optimize", "emit"],
        },
    }


def _historia_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "historia", _DOMAIN_VOCAB)
    eras = ["Classical", "Medieval", "Renaissance", "Enlightenment", "Modern", "Contemporary"]
    result["era"] = eras[hash(concept) % len(eras)]
    result["precedent"] = f"Roots in {result['era']} thought"
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "historia",
            "status": "executed", "output": result}


def _natura_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "natura", _DOMAIN_VOCAB)
    analogues = ["ecosystem", "neural network", "crystal lattice", "wave interference",
                 "genetic algorithm", "fractal coastline", "chemical equilibrium"]
    result["natural_analogue"] = analogues[hash(concept) % len(analogues)]
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "natura",
            "status": "executed", "output": result}


def _lingua_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "lingua", _DOMAIN_VOCAB)
    roles = ["noun phrase", "verb phrase", "modifier", "complement", "adjunct"]
    fields = ["cognition", "communication", "expression", "representation", "interpretation"]
    result["syntactic_role"] = roles[hash(concept) % len(roles)]
    result["semantic_field"] = fields[hash(source_domain) % len(fields)]
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "lingua",
            "status": "executed", "output": result}


def _philosophia_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "philosophia", _DOMAIN_VOCAB)
    branches = ["ontology", "epistemology", "ethics", "aesthetics", "metaphysics", "logic"]
    result["branch"] = branches[hash(concept) % len(branches)]
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "philosophia",
            "status": "executed", "output": result}


def _technologia_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "technologia", _DOMAIN_VOCAB)
    system_types = ["distributed system", "embedded system", "client-server", "pipeline",
                    "event-driven", "batch processing", "real-time"]
    result["system_type"] = system_types[hash(concept) % len(system_types)]
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "technologia",
            "status": "executed", "output": result}


def _medicina_refract(skill, inputs: Dict[str, Any]) -> Dict[str, Any]:
    concept = inputs.get("concept", "")
    source_domain = inputs.get("source_domain", "")
    result = _refract_generic(concept, source_domain, "medicina", _DOMAIN_VOCAB)
    systems = ["nervous", "cardiovascular", "immune", "endocrine", "musculoskeletal",
               "digestive", "respiratory"]
    result["system_affected"] = systems[hash(concept) % len(systems)]
    return {"skill_id": skill.skill_id, "skill_name": skill.name, "domain": "medicina",
            "status": "executed", "output": result}


# ─── Skill Executor Registry ──────────────────────────────────

_SKILL_EXECUTORS: Dict[str, Callable] = {
    # Musica
    "musica.refract": _musica_refract,
    "musica.sonify": _musica_sonify,
    # Mathematica
    "mathematica.refract": _mathematica_refract,
    "mathematica.prove": _mathematica_prove,
    # Historia
    "historia.refract": _historia_refract,
    # Natura
    "natura.refract": _natura_refract,
    # Lingua
    "lingua.refract": _lingua_refract,
    # Philosophia
    "philosophia.refract": _philosophia_refract,
    # Technologia
    "technologia.refract": _technologia_refract,
    # Medicina
    "medicina.refract": _medicina_refract,
    # Coda
    "coda.refract": _coda_refract,
    "coda.compile": _coda_compile,
}


# ─── Agent Query Functions ────────────────────────────────────

def get_agent(domain: str) -> Optional[BeadAgent]:
    """Get the bead agent for a specific domain."""
    return BEAD_AGENTS.get(domain)


def get_all_agents() -> List[BeadAgent]:
    """Return all 9 bead agents."""
    return list(BEAD_AGENTS.values())


def get_agent_skills(domain: str, unlocked_only: bool = False) -> List[Dict[str, Any]]:
    """Get skills for a specific bead agent."""
    agent = BEAD_AGENTS.get(domain)
    if not agent:
        return []
    tree = get_skill_tree()
    skills = []
    for skill in tree.get_skills_by_domain(domain):
        if unlocked_only and not tree.is_unlocked(skill.skill_id):
            continue
        skills.append({
            **skill.to_dict(),
            "unlocked": tree.is_unlocked(skill.skill_id),
        })
    return skills


def agent_refact(domain: str, concept: str, source_domain: str = "") -> Dict[str, Any]:
    """
    Invoke a bead agent's core refraction skill.
    This is the primary interaction: cast a concept to a bead, get its refraction.
    """
    skill_id = f"{domain}.refract"
    return execute_skill(skill_id, {
        "concept": concept,
        "source_domain": source_domain,
    })


def agent_to_dict(domain: str) -> Optional[Dict[str, Any]]:
    """Full agent info including skills."""
    agent = BEAD_AGENTS.get(domain)
    if not agent:
        return None
    tree = get_skill_tree()
    return {
        **agent.to_dict(),
        "skill_details": get_agent_skills(domain),
        "unlocked_skills": get_agent_skills(domain, unlocked_only=True),
    }


def all_agents_overview() -> List[Dict[str, Any]]:
    """Return an overview of all 9 bead agents with their skills."""
    return [a for a in (agent_to_dict(d) for d in BEAD_AGENTS.keys()) if a is not None]


def get_skill_executor() -> Callable:
    """Return the skill execution function for trace programs."""
    return execute_skill