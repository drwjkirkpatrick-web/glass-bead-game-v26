"""Tests for Bead Agent Skill Tree (bead_skills).

Covers:
  - SkillTier enum values
  - BeadSkill dataclass & to_dict
  - _build_skill_catalog: 9 domains, 45 skills, 2 CORE + 2 ADVANCED + 1 MASTER per domain
  - SkillTree.evaluate_unlocks (no mastery -> 18 CORE, 0.3 -> ADVANCED, 0.7+3h -> MASTER)
  - get_unlocked_skills / get_locked_skills (with domain filtering)
  - get_skills_by_domain / get_skill / is_unlocked
  - get_tree_overview
  - create_trace_program (valid, unknown skill raises ValueError)
  - get_trace_program / list_trace_programs
  - execute_trace_program with mock executor
  - to_dict
  - get_skill_tree singleton
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

import pytest

from src.bead_skills import (
    SkillTier,
    BeadSkill,
    SkillTree,
    _build_skill_catalog,
    get_skill_tree,
)


# ─── Fixtures ────────────────────────────────────────────────

@pytest.fixture
def catalog():
    return _build_skill_catalog()


@pytest.fixture
def tree():
    """Fresh SkillTree for each test (avoids singleton state leakage)."""
    return SkillTree()


@pytest.fixture
def all_unlocked_tree(tree):
    """A tree with every skill unlocked via full mastery + contemplation."""
    domains = list(SkillTree.ALL_SKILLS.keys())
    domain_mastery = {d: 1.0 for d in domains}
    domain_contemplation = {d: 5.0 for d in domains}
    tree.evaluate_unlocks(
        verified_moves=100,
        domain_mastery=domain_mastery,
        contemplation_hours=50.0,
        domain_contemplation=domain_contemplation,
    )
    return tree


# ─── SkillTier enum ──────────────────────────────────────────

class TestSkillTier:
    def test_core_value_is_zero(self):
        assert SkillTier.CORE.value == 0

    def test_advanced_value_is_one(self):
        assert SkillTier.ADVANCED.value == 1

    def test_master_value_is_two(self):
        assert SkillTier.MASTER.value == 2

    def test_three_tiers(self):
        assert len(list(SkillTier)) == 3

    def test_progressive_ordering(self):
        assert SkillTier.CORE.value < SkillTier.ADVANCED.value < SkillTier.MASTER.value


# ─── BeadSkill dataclass ─────────────────────────────────────

class TestBeadSkill:
    def test_default_reusable_and_trace_compatible(self):
        skill = BeadSkill(
            skill_id="test.skill",
            domain="test",
            tier=SkillTier.CORE,
            name="Test",
            description="desc",
            unlock_requirement="Always available",
        )
        assert skill.reusable is True
        assert skill.trace_compatible is True

    def test_default_schemas_are_empty_dicts(self):
        skill = BeadSkill(
            skill_id="test.skill",
            domain="test",
            tier=SkillTier.CORE,
            name="Test",
            description="desc",
            unlock_requirement="Always available",
        )
        assert skill.input_schema == {}
        assert skill.output_schema == {}

    def test_to_dict_keys(self):
        skill = BeadSkill(
            skill_id="musica.refract",
            domain="musica",
            tier=SkillTier.CORE,
            name="Harmonic Refraction",
            description="desc",
            unlock_requirement="Always available",
            input_schema={"concept": "str"},
            output_schema={"translation": "str"},
        )
        d = skill.to_dict()
        assert d["skill_id"] == "musica.refract"
        assert d["domain"] == "musica"
        assert d["tier"] == "CORE"          # tier is serialized as name string
        assert d["name"] == "Harmonic Refraction"
        assert d["description"] == "desc"
        assert d["unlock_requirement"] == "Always available"
        assert d["input_schema"] == {"concept": "str"}
        assert d["output_schema"] == {"translation": "str"}
        assert d["reusable"] is True
        assert d["trace_compatible"] is True

    def test_to_dict_tier_is_string_name(self):
        for tier in SkillTier:
            skill = BeadSkill(
                skill_id=f"t.{tier.name.lower()}",
                domain="t",
                tier=tier,
                name="N",
                description="d",
                unlock_requirement="r",
            )
            assert skill.to_dict()["tier"] == tier.name


# ─── Catalog structure ───────────────────────────────────────

class TestCatalog:
    def test_nine_domains(self, catalog):
        assert len(catalog) == 9

    def test_expected_domain_names(self, catalog):
        expected = {
            "musica", "mathematica", "historia", "natura", "lingua",
            "philosophia", "technologia", "medicina", "coda",
        }
        assert set(catalog.keys()) == expected

    def test_total_45_skills(self, catalog):
        total = sum(len(skills) for skills in catalog.values())
        assert total == 45

    def test_each_domain_has_5_skills(self, catalog):
        for domain, skills in catalog.items():
            assert len(skills) == 5, f"{domain} has {len(skills)} skills, expected 5"

    def test_each_domain_tier_distribution(self, catalog):
        """2 CORE + 2 ADVANCED + 1 MASTER per domain."""
        for domain, skills in catalog.items():
            tiers = [s.tier for s in skills]
            assert tiers.count(SkillTier.CORE) == 2, f"{domain} CORE count"
            assert tiers.count(SkillTier.ADVANCED) == 2, f"{domain} ADVANCED count"
            assert tiers.count(SkillTier.MASTER) == 1, f"{domain} MASTER count"

    def test_skill_ids_are_unique(self, catalog):
        all_ids = [s.skill_id for skills in catalog.values() for s in skills]
        assert len(all_ids) == len(set(all_ids)), "Duplicate skill_ids in catalog"

    def test_skill_domain_matches_key(self, catalog):
        for domain, skills in catalog.items():
            for skill in skills:
                assert skill.domain == domain

    def test_skill_id_prefixed_with_domain(self, catalog):
        for domain, skills in catalog.items():
            for skill in skills:
                assert skill.skill_id.startswith(f"{domain}."), (
                    f"{skill.skill_id} does not start with '{domain}.'"
                )

    def test_all_skills_trace_compatible(self, catalog):
        for skills in catalog.values():
            for skill in skills:
                assert skill.trace_compatible is True

    def test_all_skills_reusable(self, catalog):
        for skills in catalog.values():
            for skill in skills:
                assert skill.reusable is True


# ─── evaluate_unlocks ────────────────────────────────────────

class TestEvaluateUnlocks:
    def test_no_mastery_unlocks_only_core(self, tree):
        unlocked = tree.evaluate_unlocks()
        # 9 domains × 2 CORE = 18
        assert len(unlocked) == 18
        # Every unlocked skill is CORE tier
        for sid in unlocked:
            assert tree.get_skill(sid).tier == SkillTier.CORE

    def test_no_mastery_locks_advanced_and_master(self, tree):
        tree.evaluate_unlocks()
        for skills in SkillTree.ALL_SKILLS.values():
            for skill in skills:
                if skill.tier in (SkillTier.ADVANCED, SkillTier.MASTER):
                    assert not tree.is_unlocked(skill.skill_id)

    def test_mastery_0_3_unlocks_advanced(self, tree):
        domains = list(SkillTree.ALL_SKILLS.keys())
        domain_mastery = {d: 0.3 for d in domains}
        unlocked = tree.evaluate_unlocks(domain_mastery=domain_mastery)
        # 18 CORE + 9 domains × 2 ADVANCED = 36
        assert len(unlocked) == 36
        for skills in SkillTree.ALL_SKILLS.values():
            for skill in skills:
                if skill.tier == SkillTier.ADVANCED:
                    assert skill.skill_id in unlocked
                if skill.tier == SkillTier.MASTER:
                    assert skill.skill_id not in unlocked

    def test_mastery_0_7_unlocks_advanced_but_not_master_without_contemplation(self, tree):
        """MASTER requires both mastery >= 0.7 AND contemplation >= 3.0."""
        domains = list(SkillTree.ALL_SKILLS.keys())
        domain_mastery = {d: 0.7 for d in domains}
        unlocked = tree.evaluate_unlocks(domain_mastery=domain_mastery)
        # Only CORE + ADVANCED unlocked; MASTER still locked
        assert len(unlocked) == 36
        for skills in SkillTree.ALL_SKILLS.values():
            for skill in skills:
                if skill.tier == SkillTier.MASTER:
                    assert skill.skill_id not in unlocked

    def test_mastery_0_7_and_3_contemplation_unlocks_master(self, tree):
        domains = list(SkillTree.ALL_SKILLS.keys())
        domain_mastery = {d: 0.7 for d in domains}
        domain_contemplation = {d: 3.0 for d in domains}
        unlocked = tree.evaluate_unlocks(
            domain_mastery=domain_mastery,
            contemplation_hours=50.0,
            domain_contemplation=domain_contemplation,
        )
        # 18 CORE + 18 ADVANCED + 9 MASTER = 45
        assert len(unlocked) == 45
        for skills in SkillTree.ALL_SKILLS.values():
            for skill in skills:
                assert skill.skill_id in unlocked

    def test_mastery_above_threshold_unlocks_master(self, tree):
        """mastery > 0.7 and cont > 3.0 should also unlock MASTER."""
        domains = list(SkillTree.ALL_SKILLS.keys())
        unlocked = tree.evaluate_unlocks(
            domain_mastery={d: 1.0 for d in domains},
            domain_contemplation={d: 5.0 for d in domains},
        )
        assert len(unlocked) == 45

    def test_partial_mastery_unlocks_only_that_domain(self, tree):
        unlocked = tree.evaluate_unlocks(
            domain_mastery={"musica": 0.3},
        )
        # musica ADVANCED unlocked, other domains still CORE-only
        assert tree.is_unlocked("musica.counterpoint")
        assert tree.is_unlocked("musica.motivic_transform")
        assert not tree.is_unlocked("mathematica.symmetry")
        # Total: 18 CORE + 2 musica ADVANCED
        assert len(unlocked) == 20

    def test_partial_contemplation_unlocks_only_that_domain_master(self, tree):
        unlocked = tree.evaluate_unlocks(
            domain_mastery={"musica": 0.7},
            domain_contemplation={"musica": 3.0},
        )
        assert tree.is_unlocked("musica.composition_engine")
        assert not tree.is_unlocked("mathematica.isomorphism_engine")

    def test_returns_set(self, tree):
        result = tree.evaluate_unlocks()
        assert isinstance(result, set)

    def test_updates_internal_unlocked_state(self, tree):
        tree.evaluate_unlocks(domain_mastery={"musica": 0.3})
        assert tree.is_unlocked("musica.counterpoint")
        # Re-evaluate with no mastery resets to CORE-only
        tree.evaluate_unlocks()
        assert not tree.is_unlocked("musica.counterpoint")

    def test_below_0_3_mastery_does_not_unlock_advanced(self, tree):
        unlocked = tree.evaluate_unlocks(domain_mastery={"musica": 0.29})
        assert not tree.is_unlocked("musica.counterpoint")

    def test_below_0_7_mastery_does_not_unlock_master_even_with_contemplation(self, tree):
        unlocked = tree.evaluate_unlocks(
            domain_mastery={"musica": 0.69},
            domain_contemplation={"musica": 5.0},
        )
        assert not tree.is_unlocked("musica.composition_engine")

    def test_below_3_contemplation_does_not_unlock_master(self, tree):
        unlocked = tree.evaluate_unlocks(
            domain_mastery={"musica": 0.9},
            domain_contemplation={"musica": 2.99},
        )
        assert not tree.is_unlocked("musica.composition_engine")


# ─── get_unlocked_skills ─────────────────────────────────────

class TestGetUnlockedSkills:
    def test_empty_tree_returns_core_skills(self, tree):
        tree.evaluate_unlocks()
        unlocked = tree.get_unlocked_skills()
        assert len(unlocked) == 18
        for skill in unlocked:
            assert skill.tier == SkillTier.CORE

    def test_domain_filter(self, tree):
        tree.evaluate_unlocks()
        musica_unlocked = tree.get_unlocked_skills(domain="musica")
        assert len(musica_unlocked) == 2  # 2 CORE in musica
        for skill in musica_unlocked:
            assert skill.domain == "musica"

    def test_all_unlocked(self, all_unlocked_tree):
        unlocked = all_unlocked_tree.get_unlocked_skills()
        assert len(unlocked) == 45

    def test_all_unlocked_domain_filter(self, all_unlocked_tree):
        unlocked = all_unlocked_tree.get_unlocked_skills(domain="natura")
        assert len(unlocked) == 5

    def test_nonexistent_domain_returns_empty(self, tree):
        tree.evaluate_unlocks()
        assert tree.get_unlocked_skills(domain="nonexistent") == []

    def test_returns_list_of_beadskills(self, tree):
        tree.evaluate_unlocks()
        unlocked = tree.get_unlocked_skills()
        assert all(isinstance(s, BeadSkill) for s in unlocked)


# ─── get_locked_skills ───────────────────────────────────────

class TestGetLockedSkills:
    def test_no_mastery_locks_27(self, tree):
        tree.evaluate_unlocks()
        locked = tree.get_locked_skills()
        # 45 - 18 CORE = 27
        assert len(locked) == 27
        for skill in locked:
            assert skill.tier in (SkillTier.ADVANCED, SkillTier.MASTER)

    def test_domain_filter(self, tree):
        tree.evaluate_unlocks()
        musica_locked = tree.get_locked_skills(domain="musica")
        # 3 locked in musica: 2 ADVANCED + 1 MASTER
        assert len(musica_locked) == 3
        for skill in musica_locked:
            assert skill.domain == "musica"

    def test_all_unlocked_no_locked(self, all_unlocked_tree):
        assert all_unlocked_tree.get_locked_skills() == []

    def test_all_unlocked_domain_filter_empty(self, all_unlocked_tree):
        assert all_unlocked_tree.get_locked_skills(domain="coda") == []

    def test_nonexistent_domain_returns_empty(self, tree):
        tree.evaluate_unlocks()
        assert tree.get_locked_skills(domain="nope") == []

    def test_returns_list_of_beadskills(self, tree):
        tree.evaluate_unlocks()
        locked = tree.get_locked_skills()
        assert all(isinstance(s, BeadSkill) for s in locked)


# ─── get_skills_by_domain ────────────────────────────────────

class TestGetSkillsByDomain:
    def test_returns_5_per_domain(self, tree):
        for domain in SkillTree.ALL_SKILLS:
            skills = tree.get_skills_by_domain(domain)
            assert len(skills) == 5

    def test_returns_all_tiers(self, tree):
        skills = tree.get_skills_by_domain("philosophia")
        tiers = [s.tier for s in skills]
        assert SkillTier.CORE in tiers
        assert SkillTier.ADVANCED in tiers
        assert SkillTier.MASTER in tiers

    def test_nonexistent_domain_returns_empty(self, tree):
        assert tree.get_skills_by_domain("void") == []

    def test_returns_copy_not_reference(self, tree):
        s1 = tree.get_skills_by_domain("musica")
        s2 = tree.get_skills_by_domain("musica")
        assert s1 == s2
        assert s1 is not s2  # list() creates a new list


# ─── get_skill ───────────────────────────────────────────────

class TestGetSkill:
    def test_existing_skill(self, tree):
        skill = tree.get_skill("musica.refract")
        assert skill is not None
        assert skill.skill_id == "musica.refract"
        assert skill.domain == "musica"

    def test_master_skill(self, tree):
        skill = tree.get_skill("mathematica.isomorphism_engine")
        assert skill is not None
        assert skill.tier == SkillTier.MASTER

    def test_nonexistent_returns_none(self, tree):
        assert tree.get_skill("nonexistent.skill") is None

    def test_empty_string_returns_none(self, tree):
        assert tree.get_skill("") is None

    def test_returns_beadskill_instance(self, tree):
        skill = tree.get_skill("coda.refract")
        assert isinstance(skill, BeadSkill)


# ─── is_unlocked ─────────────────────────────────────────────

class TestIsUnlocked:
    def test_core_always_unlocked_after_evaluate(self, tree):
        tree.evaluate_unlocks()
        assert tree.is_unlocked("musica.refract") is True

    def test_advanced_locked_without_mastery(self, tree):
        tree.evaluate_unlocks()
        assert tree.is_unlocked("musica.counterpoint") is False

    def test_unlocked_after_mastery(self, tree):
        tree.evaluate_unlocks(domain_mastery={"musica": 0.3})
        assert tree.is_unlocked("musica.counterpoint") is True

    def test_nonexistent_skill_returns_false(self, tree):
        tree.evaluate_unlocks()
        assert tree.is_unlocked("nope.nope") is False

    def test_fresh_tree_nothing_unlocked(self, tree):
        """Before evaluate_unlocks is called, nothing is unlocked."""
        assert tree.is_unlocked("musica.refract") is False


# ─── get_tree_overview ───────────────────────────────────────

class TestGetTreeOverview:
    def test_has_all_nine_domains(self, tree):
        tree.evaluate_unlocks()
        overview = tree.get_tree_overview()
        assert len(overview) == 9
        for domain in SkillTree.ALL_SKILLS:
            assert domain in overview

    def test_domain_entry_structure(self, tree):
        tree.evaluate_unlocks()
        overview = tree.get_tree_overview()
        musica = overview["musica"]
        assert musica["total"] == 5
        assert musica["unlocked"] == 2  # only CORE
        assert "tiers" in musica
        assert musica["tiers"]["CORE"] == 2
        assert musica["tiers"]["ADVANCED"] == 2
        assert musica["tiers"]["MASTER"] == 1
        assert "skills" in musica
        assert len(musica["skills"]) == 5

    def test_skill_entries_have_unlocked_flag(self, tree):
        tree.evaluate_unlocks()
        overview = tree.get_tree_overview()
        for skill_entry in overview["musica"]["skills"]:
            assert "unlocked" in skill_entry
            assert "skill_id" in skill_entry
            assert "tier" in skill_entry

    def test_unlocked_count_reflects_mastery(self, tree):
        tree.evaluate_unlocks(domain_mastery={"natura": 0.3})
        overview = tree.get_tree_overview()
        assert overview["natura"]["unlocked"] == 4  # 2 CORE + 2 ADVANCED

    def test_all_unlocked_overview(self, all_unlocked_tree):
        overview = all_unlocked_tree.get_tree_overview()
        for domain in overview:
            assert overview[domain]["unlocked"] == 5

    def test_skill_entries_contain_to_dict_fields(self, tree):
        tree.evaluate_unlocks()
        overview = tree.get_tree_overview()
        entry = overview["musica"]["skills"][0]
        for key in ("skill_id", "domain", "tier", "name", "description",
                     "unlock_requirement", "input_schema", "output_schema",
                     "reusable", "trace_compatible", "unlocked"):
            assert key in entry


# ─── create_trace_program ────────────────────────────────────

class TestCreateTraceProgram:
    def test_valid_two_step_program(self, tree):
        tree.evaluate_unlocks()  # CORE unlocked
        program = tree.create_trace_program(
            name="My Trace",
            steps=[
                {
                    "skill_id": "musica.refract",
                    "input_mapping": {"concept": "harmony", "source_domain": "math"},
                },
                {
                    "skill_id": "mathematica.refract",
                    "input_mapping": {
                        "concept": "step[0].output.translation",
                        "source_domain": "musica",
                    },
                },
            ],
        )
        assert program["name"] == "My Trace"
        assert program["total_steps"] == 2
        assert program["reusable"] is True
        assert program["all_unlocked"] is True
        assert "program_id" in program
        assert program["program_id"].startswith("trace_my_trace_")

    def test_validated_steps_structure(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="Single",
            steps=[{"skill_id": "coda.compile", "input_mapping": {"concept": "x"}}],
        )
        step = program["steps"][0]
        assert step["step_index"] == 0
        assert step["skill_id"] == "coda.compile"
        assert step["skill_name"] == "Concept Compilation"
        assert step["domain"] == "coda"
        assert step["unlocked"] is True
        assert step["input_mapping"] == {"concept": "x"}

    def test_unknown_skill_raises_value_error(self, tree):
        tree.evaluate_unlocks()
        with pytest.raises(ValueError, match="unknown skill"):
            tree.create_trace_program(
                name="Bad",
                steps=[{"skill_id": "nonexistent.skill"}],
            )

    def test_unknown_skill_error_mentions_step_index(self, tree):
        tree.evaluate_unlocks()
        with pytest.raises(ValueError, match="Step 0"):
            tree.create_trace_program(
                name="Bad",
                steps=[{"skill_id": "ghost.skill"}],
            )

    def test_unknown_skill_in_second_step_raises(self, tree):
        tree.evaluate_unlocks()
        with pytest.raises(ValueError, match="Step 1"):
            tree.create_trace_program(
                name="Bad",
                steps=[
                    {"skill_id": "musica.refract", "input_mapping": {}},
                    {"skill_id": "ghost.skill"},
                ],
            )

    def test_locked_skill_creates_program_with_all_unlocked_false(self, tree):
        tree.evaluate_unlocks()  # only CORE
        program = tree.create_trace_program(
            name="Locked",
            steps=[{"skill_id": "musica.counterpoint", "input_mapping": {}}],
        )
        # ADVANCED is locked -> program created but all_unlocked is False
        assert program["all_unlocked"] is False
        assert program["steps"][0]["unlocked"] is False

    def test_empty_steps_creates_empty_program(self, tree):
        program = tree.create_trace_program(name="Empty", steps=[])
        assert program["total_steps"] == 0
        assert program["all_unlocked"] is True  # all() on empty is True

    def test_program_id_increments(self, tree):
        tree.evaluate_unlocks()
        p1 = tree.create_trace_program(name="A", steps=[])
        p2 = tree.create_trace_program(name="A", steps=[])
        # Same name but different index suffix
        assert p1["program_id"] != p2["program_id"]

    def test_input_mapping_defaults_to_empty(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="NoMapping",
            steps=[{"skill_id": "musica.refract"}],
        )
        assert program["steps"][0]["input_mapping"] == {}


# ─── get_trace_program / list_trace_programs ─────────────────

class TestTraceProgramRetrieval:
    def test_get_existing_program(self, tree):
        tree.evaluate_unlocks()
        created = tree.create_trace_program(name="Retrievable", steps=[])
        fetched = tree.get_trace_program(created["program_id"])
        assert fetched is not None
        assert fetched["name"] == "Retrievable"

    def test_get_nonexistent_returns_none(self, tree):
        assert tree.get_trace_program("trace_nonexistent_0") is None

    def test_list_empty_initially(self, tree):
        assert tree.list_trace_programs() == []

    def test_list_after_creation(self, tree):
        tree.evaluate_unlocks()
        tree.create_trace_program(name="One", steps=[])
        tree.create_trace_program(name="Two", steps=[])
        programs = tree.list_trace_programs()
        assert len(programs) == 2
        names = [p["name"] for p in programs]
        assert "One" in names
        assert "Two" in names

    def test_list_returns_list_type(self, tree):
        assert isinstance(tree.list_trace_programs(), list)


# ─── execute_trace_program ───────────────────────────────────

class TestExecuteTraceProgram:
    def test_successful_execution_single_step(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="Exec Single",
            steps=[
                {
                    "skill_id": "musica.refract",
                    "input_mapping": {"concept": "harmony", "source_domain": "math"},
                },
            ],
        )

        def mock_executor(skill_id, inputs):
            return {"translation": f"refracted-{skill_id}", "confidence": 0.9}

        result = tree.execute_trace_program(
            program["program_id"],
            initial_inputs={},
            skill_executor=mock_executor,
        )
        assert "program_id" in result
        assert result["name"] == "Exec Single"
        assert len(result["trace"]) == 1
        assert result["trace"][0]["skill_id"] == "musica.refract"
        assert result["trace"][0]["output"]["translation"] == "refracted-musica.refract"
        assert result["final_output"] == result["trace"][0]["output"]

    def test_multi_step_with_step_reference(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="Chain",
            steps=[
                {
                    "skill_id": "musica.refract",
                    "input_mapping": {"concept": "concept_a", "source_domain": "math"},
                },
                {
                    "skill_id": "mathematica.refract",
                    "input_mapping": {
                        "concept": "step[0].output.translation",
                        "source_domain": "musica",
                    },
                },
            ],
        )

        call_log = []

        def mock_executor(skill_id, inputs):
            call_log.append((skill_id, inputs))
            return {"translation": f"out-{skill_id}"}

        result = tree.execute_trace_program(
            program["program_id"],
            initial_inputs={},
            skill_executor=mock_executor,
        )
        assert len(result["trace"]) == 2
        # Second step should receive the first step's output as its "concept" input
        assert call_log[1][1]["concept"] == "out-musica.refract"
        assert result["final_output"] == {"translation": "out-mathematica.refract"}

    def test_literal_inputs_passed_directly(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="Literal",
            steps=[
                {
                    "skill_id": "natura.classify",
                    "input_mapping": {"concept": "photosynthesis"},
                },
            ],
        )

        def mock_executor(skill_id, inputs):
            assert inputs == {"concept": "photosynthesis"}
            return {"kingdom": "plantae"}

        result = tree.execute_trace_program(
            program["program_id"], initial_inputs={}, skill_executor=mock_executor,
        )
        assert result["trace"][0]["input"] == {"concept": "photosynthesis"}

    def test_context_reference_inputs(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="Context",
            steps=[
                {
                    "skill_id": "musica.refract",
                    "input_mapping": {"concept": "my_concept", "source_domain": "src"},
                },
            ],
        )

        def mock_executor(skill_id, inputs):
            return {"translation": "done"}

        result = tree.execute_trace_program(
            program["program_id"],
            initial_inputs={"my_concept": "from_context", "src": "historia"},
            skill_executor=mock_executor,
        )
        # input_mapping values are resolved from initial_inputs context
        assert result["trace"][0]["input"]["concept"] == "from_context"
        assert result["trace"][0]["input"]["source_domain"] == "historia"

    def test_unknown_program_returns_error(self, tree):
        def mock_executor(skill_id, inputs):
            return {}

        result = tree.execute_trace_program("ghost", {}, mock_executor)
        assert "error" in result
        assert "Unknown trace program" in result["error"]

    def test_locked_skills_return_error(self, tree):
        tree.evaluate_unlocks()  # CORE only
        program = tree.create_trace_program(
            name="LockedExec",
            steps=[{"skill_id": "musica.counterpoint", "input_mapping": {}}],
        )
        assert not program["all_unlocked"]

        result = tree.execute_trace_program(
            program["program_id"], {}, lambda sid, inp: {},
        )
        assert "error" in result
        assert "Locked skills" in result["error"]
        assert "musica.counterpoint" in result["error"]

    def test_trace_entries_contain_full_structure(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="Structure",
            steps=[{"skill_id": "musica.refract", "input_mapping": {"concept": "x"}}],
        )

        def mock_executor(skill_id, inputs):
            return {"translation": "t"}

        result = tree.execute_trace_program(
            program["program_id"], {}, mock_executor,
        )
        entry = result["trace"][0]
        assert "step_index" in entry
        assert "skill_id" in entry
        assert "skill_name" in entry
        assert "domain" in entry
        assert "input" in entry
        assert "output" in entry

    def test_empty_program_execution(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(name="EmptyExec", steps=[])

        result = tree.execute_trace_program(
            program["program_id"], {}, lambda sid, inp: {},
        )
        assert result["trace"] == []
        assert result["final_output"] == {}

    def test_executor_called_per_step(self, tree):
        tree.evaluate_unlocks()
        program = tree.create_trace_program(
            name="CallCount",
            steps=[
                {"skill_id": "musica.refract", "input_mapping": {"concept": "a", "source_domain": "b"}},
                {"skill_id": "mathematica.refract", "input_mapping": {"concept": "a", "source_domain": "b"}},
                {"skill_id": "historia.refract", "input_mapping": {"concept": "a", "source_domain": "b"}},
            ],
        )
        calls = []

        def mock_executor(skill_id, inputs):
            calls.append(skill_id)
            return {"translation": "x"}

        tree.execute_trace_program(program["program_id"], {}, mock_executor)
        assert len(calls) == 3
        assert calls == ["musica.refract", "mathematica.refract", "historia.refract"]


# ─── to_dict ─────────────────────────────────────────────────

class TestToDict:
    def test_structure(self, tree):
        tree.evaluate_unlocks()
        d = tree.to_dict()
        assert d["total_skills"] == 45
        assert d["unlocked_count"] == 18
        assert len(d["domains"]) == 9
        assert "tree" in d
        assert "trace_programs" in d
        assert d["trace_programs"] == []

    def test_unlocked_count_reflects_state(self, tree):
        domains = list(SkillTree.ALL_SKILLS.keys())
        tree.evaluate_unlocks(domain_mastery={d: 0.3 for d in domains})
        d = tree.to_dict()
        assert d["unlocked_count"] == 36

    def test_domains_match_catalog(self, tree):
        d = tree.to_dict()
        assert set(d["domains"]) == set(SkillTree.ALL_SKILLS.keys())

    def test_trace_programs_serialized(self, tree):
        tree.evaluate_unlocks()
        tree.create_trace_program(name="SerTest", steps=[])
        d = tree.to_dict()
        assert len(d["trace_programs"]) == 1
        assert d["trace_programs"][0]["name"] == "SerTest"

    def test_all_unlocked_to_dict(self, all_unlocked_tree):
        d = all_unlocked_tree.to_dict()
        assert d["total_skills"] == 45
        assert d["unlocked_count"] == 45


# ─── get_skill_tree singleton ────────────────────────────────

class TestGetSkillTree:
    def test_returns_skilltree_instance(self):
        tree = get_skill_tree()
        assert isinstance(tree, SkillTree)

    def test_singleton_identity(self):
        t1 = get_skill_tree()
        t2 = get_skill_tree()
        assert t1 is t2

    def test_singleton_persists_state(self):
        """The singleton retains unlocked state across calls."""
        tree = get_skill_tree()
        tree.evaluate_unlocks(domain_mastery={"musica": 0.3})
        assert get_skill_tree().is_unlocked("musica.counterpoint")
        # Clean up so other tests aren't affected
        tree.evaluate_unlocks()


# ─── Integration ─────────────────────────────────────────────

class TestIntegration:
    def test_full_workflow(self, tree):
        """End-to-end: evaluate -> overview -> create trace -> execute."""
        # 1. Evaluate with partial mastery
        tree.evaluate_unlocks(domain_mastery={"musica": 0.3, "mathematica": 0.3})
        assert tree.is_unlocked("musica.counterpoint")
        assert not tree.is_unlocked("musica.composition_engine")

        # 2. Overview reflects state
        overview = tree.get_tree_overview()
        assert overview["musica"]["unlocked"] == 4
        assert overview["mathematica"]["unlocked"] == 4
        assert overview["historia"]["unlocked"] == 2

        # 3. Create and execute a trace program using unlocked skills
        program = tree.create_trace_program(
            name="Integration Trace",
            steps=[
                {"skill_id": "musica.refract", "input_mapping": {"concept": "c", "source_domain": "math"}},
                {"skill_id": "musica.counterpoint", "input_mapping": {"concept": "step[0].output.translation", "structural_property": "fugue"}},
            ],
        )
        assert program["all_unlocked"] is True

        def executor(skill_id, inputs):
            return {"translation": f"t-{skill_id}", "interval": "P5"}

        result = tree.execute_trace_program(program["program_id"], {}, executor)
        assert len(result["trace"]) == 2
        assert result["trace"][1]["input"]["concept"] == "t-musica.refract"

        # 4. to_dict captures everything
        d = tree.to_dict()
        assert d["unlocked_count"] == 22  # 18 + 2 + 2
        assert len(d["trace_programs"]) == 1

    def test_unlocked_plus_locked_equals_total(self, tree):
        tree.evaluate_unlocks(domain_mastery={"natura": 0.7}, domain_contemplation={"natura": 3.0})
        for domain in SkillTree.ALL_SKILLS:
            unlocked = tree.get_unlocked_skills(domain=domain)
            locked = tree.get_locked_skills(domain=domain)
            assert len(unlocked) + len(locked) == 5


if __name__ == '__main__':
    pytest.main([__file__, "-v"])