"""Tests for src/bead_agents.py — BeadAgent registry and skill execution."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

import pytest

from src.bead_agents import (
    BEAD_AGENTS,
    BeadAgent,
    execute_skill,
    agent_refact,
    get_agent,
    get_all_agents,
    get_agent_skills,
    agent_to_dict,
    all_agents_overview,
    get_skill_executor,
)
from src.bead_skills import get_skill_tree


# ─── Fixtures ─────────────────────────────────────────────────

EXPECTED_DOMAINS = [
    "musica",
    "mathematica",
    "historia",
    "natura",
    "lingua",
    "philosophia",
    "technologia",
    "medicina",
    "coda",
]


@pytest.fixture(autouse=True)
def reset_skill_tree():
    """Reset the singleton SkillTree before every test so unlock state is clean."""
    import src.bead_skills as _bs

    _bs._default_tree = None
    yield
    _bs._default_tree = None


@pytest.fixture
def all_unlocked_tree():
    """Unlock every skill (CORE + ADVANCED + MASTER) for all 9 domains."""
    tree = get_skill_tree()
    full_mastery = {d: 1.0 for d in EXPECTED_DOMAINS}
    full_contemplation = {d: 5.0 for d in EXPECTED_DOMAINS}
    tree.evaluate_unlocks(
        verified_moves=100,
        domain_mastery=full_mastery,
        contemplation_hours=50.0,
        domain_contemplation=full_contemplation,
    )
    return tree


# ─── Registry: BEAD_AGENTS ─────────────────────────────────────

class TestBeadAgentsRegistry:
    def test_registry_has_nine_entries(self):
        assert len(BEAD_AGENTS) == 9

    def test_registry_keys_match_expected_domains(self):
        assert set(BEAD_AGENTS.keys()) == set(EXPECTED_DOMAINS)

    def test_every_entry_is_beadagent_instance(self):
        for agent in BEAD_AGENTS.values():
            assert isinstance(agent, BeadAgent)

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_agent_has_required_fields(self, domain):
        agent = BEAD_AGENTS[domain]
        assert isinstance(agent.domain, str) and agent.domain == domain
        assert isinstance(agent.name, str) and agent.name
        assert isinstance(agent.color, str) and agent.color.startswith("#")
        assert isinstance(agent.icon, str) and len(agent.icon) >= 1

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_agent_has_exactly_five_skills(self, domain):
        agent = BEAD_AGENTS[domain]
        assert len(agent.skills) == 5
        # Each skill_id should be a non-empty string prefixed with the domain
        for sid in agent.skills:
            assert isinstance(sid, str) and sid
            assert sid.startswith(f"{domain}.")

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_agent_skill_ids_are_unique(self, domain):
        agent = BEAD_AGENTS[domain]
        assert len(set(agent.skills)) == len(agent.skills)

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_agent_names_are_magister_style(self, domain):
        # Each Magister name should start with "Magister"
        agent = BEAD_AGENTS[domain]
        assert agent.name.startswith("Magister")


# ─── get_agent ─────────────────────────────────────────────────

class TestGetAgent:
    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_returns_correct_agent(self, domain):
        agent = get_agent(domain)
        assert agent is not None
        assert isinstance(agent, BeadAgent)
        assert agent.domain == domain

    @pytest.mark.parametrize(
        "unknown",
        ["", "music", "math", "codex", "x", "Musica", "MUSICA", "unknown"],
    )
    def test_unknown_returns_none(self, unknown):
        assert get_agent(unknown) is None

    def test_returns_same_object_as_registry(self):
        # get_agent should return the same BeadAgent object referenced by BEAD_AGENTS
        for domain in EXPECTED_DOMAINS:
            assert get_agent(domain) is BEAD_AGENTS[domain]


# ─── get_all_agents ────────────────────────────────────────────

class TestGetAllAgents:
    def test_returns_nine_agents(self):
        agents = get_all_agents()
        assert len(agents) == 9

    def test_returns_list_of_beadagents(self):
        agents = get_all_agents()
        assert isinstance(agents, list)
        for a in agents:
            assert isinstance(a, BeadAgent)

    def test_covers_all_expected_domains(self):
        agents = get_all_agents()
        domains = {a.domain for a in agents}
        assert domains == set(EXPECTED_DOMAINS)

    def test_returns_a_copy_not_internal_list(self):
        a1 = get_all_agents()
        a1.clear()
        a2 = get_all_agents()
        assert len(a2) == 9


# ─── get_agent_skills ──────────────────────────────────────────

class TestGetAgentSkills:
    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_returns_five_skills(self, all_unlocked_tree, domain):
        skills = get_agent_skills(domain)
        assert len(skills) == 5

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_skill_dicts_have_required_keys(self, all_unlocked_tree, domain):
        skills = get_agent_skills(domain)
        for s in skills:
            assert "skill_id" in s
            assert "domain" in s
            assert "tier" in s
            assert "name" in s
            assert "unlocked" in s

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_skills_belong_to_agent_domain(self, all_unlocked_tree, domain):
        skills = get_agent_skills(domain)
        for s in skills:
            assert s["domain"] == domain

    def test_unknown_domain_returns_empty_list(self):
        assert get_agent_skills("nope") == []

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_all_unlocked_flag(self, all_unlocked_tree, domain):
        skills = get_agent_skills(domain)
        assert all(s["unlocked"] is True for s in skills)

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_unlocked_only_filter(self, all_unlocked_tree, domain):
        all_skills = get_agent_skills(domain)
        unlocked = get_agent_skills(domain, unlocked_only=True)
        assert len(unlocked) == len(all_skills)
        assert all(s["unlocked"] for s in unlocked)

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_only_core_unlocked_with_empty_mastery(self, domain):
        # evaluate_unlocks() with no mastery unlocks only CORE skills (2 per domain)
        tree = get_skill_tree()
        tree.evaluate_unlocks()
        skills = get_agent_skills(domain)
        unlocked = [s for s in skills if s["unlocked"]]
        assert len(unlocked) == 2
        assert all(s["tier"] == "CORE" for s in unlocked)


# ─── agent_refact ──────────────────────────────────────────────

class TestAgentRefact:
    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_returns_status_executed_for_each_domain(self, all_unlocked_tree, domain):
        result = agent_refact(domain, "harmony", source_domain="mathematica")
        assert result["status"] == "executed"
        assert "output" in result

    def test_result_contains_skill_id(self, all_unlocked_tree):
        result = agent_refact("musica", "fugue", source_domain="mathematica")
        assert result["skill_id"] == "musica.refract"

    def test_result_contains_domain_field(self, all_unlocked_tree):
        result = agent_refact("mathematica", "group", source_domain="musica")
        assert result["domain"] == "mathematica"

    def test_output_contains_translation(self, all_unlocked_tree):
        result = agent_refact("historia", "renaissance", source_domain="musica")
        assert "translation" in result["output"]

    def test_refraction_without_unlocks_errors(self):
        result = agent_refact("musica", "harmony", source_domain="mathematica")
        assert "error" in result


# ─── execute_skill ─────────────────────────────────────────────

class TestExecuteSkill:
    def test_unlocked_skill_works(self, all_unlocked_tree):
        result = execute_skill(
            "musica.refract",
            {"concept": "harmony", "source_domain": "mathematica"},
        )
        assert result["status"] == "executed"
        assert "output" in result

    def test_unlocked_advanced_skill_works(self, all_unlocked_tree):
        result = execute_skill(
            "musica.counterpoint",
            {"concept": "fugue", "structural_property": "stretto"},
        )
        assert result["status"] == "executed"

    def test_unlocked_master_skill_works(self, all_unlocked_tree):
        result = execute_skill(
            "musica.composition_engine",
            {"theme_concept": "harmony", "domain": "mathematica"},
        )
        assert result["status"] == "executed"

    def test_unknown_skill_returns_error(self, all_unlocked_tree):
        result = execute_skill("does.not.exist", {})
        assert "error" in result
        assert "Unknown skill" in result["error"]

    def test_locked_skill_returns_error(self):
        # Fresh tree — ADVANCED/MASTER skills should be locked
        result = execute_skill(
            "musica.counterpoint",
            {"concept": "fugue", "structural_property": "stretto"},
        )
        assert "error" in result
        assert "not unlocked" in result["error"]

    def test_locked_master_skill_returns_error(self):
        # Fresh tree — MASTER skills locked
        result = execute_skill(
            "musica.composition_engine",
            {"theme_concept": "harmony", "domain": "mathematica"},
        )
        assert "error" in result
        assert "not unlocked" in result["error"]

    def test_skill_executor_dispatches_to_generic_for_unhandled(self, all_unlocked_tree):
        # Skills not in _SKILL_EXECUTORS fall back to _generic_executor
        result = execute_skill(
            "musica.counterpoint",  # no specific executor in _SKILL_EXECUTORS
            {"concept": "fugue", "structural_property": "stretto"},
        )
        assert result["status"] == "executed"
        assert "output" in result

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_all_refract_skills_executable(self, all_unlocked_tree, domain):
        result = execute_skill(
            f"{domain}.refract",
            {"concept": "test concept", "source_domain": "musica"},
        )
        assert result["status"] == "executed"
        assert result["domain"] == domain


# ─── agent_to_dict ─────────────────────────────────────────────

class TestAgentToDict:
    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_returns_full_info(self, all_unlocked_tree, domain):
        d = agent_to_dict(domain)
        assert d is not None
        assert d["domain"] == domain
        assert d["name"]
        assert d["color"].startswith("#")
        assert d["icon"]
        assert d["skill_count"] == 5
        assert "skills" in d
        assert len(d["skills"]) == 5
        assert "skill_details" in d
        assert len(d["skill_details"]) == 5
        assert "unlocked_skills" in d

    def test_unknown_domain_returns_none(self):
        assert agent_to_dict("nonexistent") is None

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_skill_details_match_skill_list(self, all_unlocked_tree, domain):
        d = agent_to_dict(domain)
        assert d is not None
        skill_ids = {s for s in d["skills"]}
        detail_ids = {s["skill_id"] for s in d["skill_details"]}
        assert skill_ids == detail_ids

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_all_skills_unlocked_in_full_mastery(self, all_unlocked_tree, domain):
        d = agent_to_dict(domain)
        assert d is not None
        assert len(d["unlocked_skills"]) == 5


# ─── all_agents_overview ───────────────────────────────────────

class TestAllAgentsOverview:
    def test_returns_nine_entries(self, all_unlocked_tree):
        overview = all_agents_overview()
        assert len(overview) == 9

    def test_each_entry_is_dict(self, all_unlocked_tree):
        overview = all_agents_overview()
        for entry in overview:
            assert isinstance(entry, dict)

    def test_covers_all_expected_domains(self, all_unlocked_tree):
        overview = all_agents_overview()
        domains = {e["domain"] for e in overview}
        assert domains == set(EXPECTED_DOMAINS)

    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_overview_entry_has_skill_details(self, all_unlocked_tree, domain):
        overview = all_agents_overview()
        entry = next(e for e in overview if e["domain"] == domain)
        assert "skill_details" in entry
        assert len(entry["skill_details"]) == 5


# ─── get_skill_executor ────────────────────────────────────────

class TestGetSkillExecutor:
    def test_returns_callable(self):
        executor = get_skill_executor()
        assert callable(executor)

    def test_executor_is_execute_skill(self):
        executor = get_skill_executor()
        assert executor is execute_skill

    def test_executor_executes_unlocked_skill(self, all_unlocked_tree):
        executor = get_skill_executor()
        result = executor(
            "musica.refract",
            {"concept": "harmony", "source_domain": "mathematica"},
        )
        assert result["status"] == "executed"


# ─── BeadAgent.to_dict ─────────────────────────────────────────

class TestBeadAgentToDict:
    @pytest.mark.parametrize("domain", EXPECTED_DOMAINS)
    def test_to_dict_fields(self, domain):
        agent = BEAD_AGENTS[domain]
        d = agent.to_dict()
        assert d["domain"] == agent.domain
        assert d["name"] == agent.name
        assert d["color"] == agent.color
        assert d["icon"] == agent.icon
        assert d["skill_count"] == 5
        assert d["skills"] == agent.skills
        assert len(d["skills"]) == 5