"""Tests for src/magister.py — Ludi Magister role."""

import pytest
from src.magister import (
    GameEvaluation,
    Magister,
    PlayerAssessment,
    Province,
    Rank,
    School,
)


class TestGameEvaluation:
    def test_default_scores_zero(self):
        ev = GameEvaluation()
        assert ev.technical_virtuosity == 0.0
        assert ev.overall_score == 0.0

    def test_overall_score_weighted(self):
        ev = GameEvaluation(
            technical_virtuosity=1.0,
            contemplative_depth=1.0,
            synthesis_quality=1.0,
            ceremonial_presence=1.0,
        )
        assert ev.overall_score == pytest.approx(1.0)

    def test_overall_score_mixed(self):
        ev = GameEvaluation(
            technical_virtuosity=0.8,
            contemplative_depth=0.6,
            synthesis_quality=0.4,
            ceremonial_presence=0.2,
        )
        expected = 0.8 * 0.25 + 0.6 * 0.30 + 0.4 * 0.30 + 0.2 * 0.15
        assert ev.overall_score == pytest.approx(expected)

    def test_to_dict(self):
        ev = GameEvaluation(0.5, 0.5, 0.5, 0.5)
        d = ev.to_dict()
        assert d["overall_score"] == pytest.approx(ev.overall_score)
        assert "technical_virtuosity" in d


class TestSchool:
    def test_enroll_and_remove(self):
        s = School("Bellavista", Province.WALDZELL, style="contrapuntal")
        s.enroll("Knecht")
        assert "Knecht" in s.players
        s.remove("Knecht")
        assert "Knecht" not in s.players

    def test_enroll_unique(self):
        s = School("Monteport", Province.MONTEPORT)
        s.enroll("Tito")
        s.enroll("Tito")
        assert s.players.count("Tito") == 1


class TestMagisterCreation:
    def test_requires_name(self):
        with pytest.raises(ValueError, match="must have a name"):
            Magister(name="", province=Province.WALDZELL)

    def test_defaults(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        assert m.rank is Rank.LUDI_MAGISTER
        assert m.province is Province.WALDZELL
        assert len(m.duties) > 0
        assert "successor" in " ".join(m.duties).lower()

    def test_list_duties(self):
        m = Magister("Magister Ludi", Province.WALDZELL)
        duties = m.list_duties()
        assert any("public matches" in d for d in duties)
        assert any("World Commission" in d for d in duties)

    def test_add_remove_duty(self):
        m = Magister("Magister Ludi", Province.WALDZELL)
        m.add_duty("mediate disputes between schools")
        assert "mediate disputes between schools" in m.duties
        m.remove_duty("mediate disputes between schools")
        assert "mediate disputes between schools" not in m.duties


class TestSchoolSupervision:
    def test_found_school(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        school = m.found_school("Mariafels", style="meditative")
        assert isinstance(school, School)
        assert school.name == "Mariafels"
        assert school.province is Province.WALDZELL
        assert "Mariafels" in m.list_schools()

    def test_supervise_existing(self):
        m = Magister("Magister Knecht", Province.MONTEPORT)
        s = School("Cantus Firmus", Province.MONTEPORT)
        m.supervise_school(s)
        assert "Cantus Firmus" in m.list_schools()


class TestEvaluation:
    def test_evaluate_game_clamps(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        ev = m.evaluate_game(
            player_name="Tito",
            technical_virtuosity=1.5,
            contemplative_depth=-0.2,
            synthesis_quality=0.8,
            ceremonial_presence=0.6,
        )
        assert ev.technical_virtuosity == 1.0
        assert ev.contemplative_depth == 0.0
        assert ev.synthesis_quality == 0.8

    def test_player_evaluations(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.evaluate_game("Tito", 0.5, 0.5, 0.5, 0.5)
        m.evaluate_game("Tito", 0.6, 0.6, 0.6, 0.6)
        evs = m.get_player_evaluations("Tito")
        assert len(evs) == 2

    def test_highest_evaluation(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.evaluate_game("Tito", 0.3, 0.3, 0.3, 0.3)
        m.evaluate_game("Tito", 0.9, 0.9, 0.9, 0.9)
        best = m.highest_evaluation("Tito")
        assert best is not None
        assert best.overall_score == pytest.approx(0.9)

    def test_highest_no_evaluations(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        assert m.highest_evaluation("Unknown") is None


class TestSuccessorTraining:
    def test_train_successor(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.train_successor("Tito")
        status = m.successor_status()
        assert status["has_successor"] is True
        assert status["candidate"] == "Tito"
        assert status["training_complete"] is False

    def test_cannot_train_two(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.train_successor("Tito")
        with pytest.raises(RuntimeError, match="Already training"):
            m.train_successor("Designori")

    def test_mark_training_complete(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.train_successor("Tito")
        m.mark_training_complete()
        assert m.successor_status()["training_complete"] is True

    def test_mark_complete_without_candidate(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        with pytest.raises(RuntimeError, match="No successor"):
            m.mark_training_complete()

    def test_dismiss_successor(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.train_successor("Tito")
        m.dismiss_successor()
        assert m.successor_status()["has_successor"] is False

    def test_appoint_successor(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.train_successor("Tito")
        m.mark_training_complete()
        appointed = m.appoint_successor()
        assert appointed == "Tito"
        assert m.successor_status()["has_successor"] is False

    def test_appoint_before_complete(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.train_successor("Tito")
        with pytest.raises(RuntimeError, match="not yet completed"):
            m.appoint_successor()

    def test_appoint_without_candidate(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        with pytest.raises(RuntimeError, match="No successor"):
            m.appoint_successor()


class TestCommission:
    def test_attend_session(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.attend_commission_session()
        m.attend_commission_session()
        assert m.commission_sessions_attended == 2


class TestSerialisation:
    def test_to_dict(self):
        m = Magister("Magister Knecht", Province.WALDZELL)
        m.found_school("Mariafels")
        m.evaluate_game("Tito", 0.8, 0.7, 0.9, 0.6, notes="Promising")
        d = m.to_dict()
        assert d["name"] == "Magister Knecht"
        assert d["province"] == "WALDZELL"
        assert d["rank"] == "LUDI_MAGISTER"
        assert len(d["duties"]) > 0
        assert d["evaluations_count"] == 1
        assert d["commission_sessions_attended"] == 0
        assert "successor" in d
