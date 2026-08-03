"""Tests for src/ceremony.py — Ceremonial Match System."""

import pytest
from src.ceremony import (
    Audience,
    Ceremony,
    CeremonialPhase,
    FestivalRecord,
    FestivalType,
)


class TestAudience:
    def test_reverence_bounds(self):
        aud = Audience(size=100, reverence_score=0.95)
        aud.deepen_reverence(0.1)
        assert aud.reverence_score == 1.0
        aud.diminish_reverence(0.2)
        assert aud.reverence_score == 0.8
        aud.diminish_reverence(1.0)
        assert aud.reverence_score == 0.0


class TestCeremonyCreation:
    def test_requires_magister(self):
        with pytest.raises(ValueError, match="Ludi Magister"):
            Ceremony(magister_presiding="", festival_type=FestivalType.LUDUS_SOLLEMNIS, audience=Audience(10, 0.5))

    def test_requires_audience(self):
        with pytest.raises(ValueError, match="public audience"):
            Ceremony(
                magister_presiding="Magister Knecht",
                festival_type=FestivalType.LUDUS_SOLLEMNIS,
                audience=Audience(size=0, reverence_score=0.0),
            )

    def test_starts_at_prelude(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        assert c.current_phase is CeremonialPhase.PRELUDE
        assert not c.completed


class TestMeditation:
    def test_meditation_required(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        c.perform_meditation(minutes=10)
        assert c.meditation_performed
        assert c.meditation_minutes == 10
        assert c.reverence > 0

    def test_meditation_too_short(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        with pytest.raises(ValueError, match="at least one minute"):
            c.perform_meditation(minutes=0)


class TestPhaseProgression:
    def test_full_phases(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_ANNIVERSARIUS,
            audience=Audience(size=200, reverence_score=0.6),
        )
        c.perform_meditation(10)
        c.begin_prelude()
        c.begin_exposition(theme_clarity=0.8)
        c.begin_development(elaboration=0.7, contrast=0.6)
        c.begin_recapitulation(reconciliation=0.9)
        c.begin_coda(realization=0.8)
        assert c.completed
        assert len(c.phases_completed) == 5
        assert c.is_valid()

    def test_skip_phase_fails(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        c.perform_meditation(5)
        c.begin_prelude()
        with pytest.raises(RuntimeError, match="Development must follow Exposition"):
            c.begin_development(elaboration=0.5, contrast=0.5)

    def test_cannot_begin_prelude_twice(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        c.begin_prelude()
        with pytest.raises(RuntimeError, match="Prelude can only begin"):
            c.begin_prelude()


class TestScoring:
    def test_scores_capped(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        c.reverence = 5.0
        scores = c.calculate_scores()
        assert scores["reverence"] == 1.0
        assert 0.0 <= scores["overall"] <= 1.0

    def test_scores_improve_with_play(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        c.perform_meditation(10)
        before = c.calculate_scores()["overall"]
        c.begin_prelude()
        c.begin_exposition(theme_clarity=0.9)
        c.begin_development(elaboration=0.9, contrast=0.8)
        c.begin_recapitulation(reconciliation=0.9)
        c.begin_coda(realization=0.9)
        after = c.calculate_scores()["overall"]
        assert after > before


class TestFestivalRecord:
    def test_record_only_when_valid(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=50, reverence_score=0.5),
        )
        # No meditation, incomplete phases
        assert c.produce_festival_record() is None

    def test_full_play_produces_record(self):
        c = Ceremony(
            magister_presiding="Magister Knecht",
            festival_type=FestivalType.LUDUS_ANNIVERSARIUS,
            audience=Audience(size=300, reverence_score=0.7),
        )
        record = c.play_full_ceremony(
            theme_clarity=0.8,
            elaboration=0.8,
            contrast=0.7,
            reconciliation=0.9,
            realization=0.85,
        )
        assert isinstance(record, FestivalRecord)
        assert record.magister_name == "Magister Knecht"
        assert record.festival_type is FestivalType.LUDUS_ANNIVERSARIUS
        assert record.audience_size == 300
        assert len(record.phases_completed) == 5
        assert record.overall_score > 0
        assert record.reverence_score > 0
        assert record.virtuosity_score > 0
        assert record.synthesis_score > 0

    def test_record_attributes(self):
        c = Ceremony(
            magister_presiding="Magister Ludi",
            festival_type=FestivalType.LUDUS_SOLLEMNIS,
            audience=Audience(size=100, reverence_score=0.5),
        )
        record = c.play_full_ceremony()
        assert record.record_id
        assert record.played_at is not None
        assert record.meditation_minutes > 0
        assert record.final_reverence >= 0.0


class TestFestivalTypeEnum:
    def test_members(self):
        assert FestivalType.LUDUS_SOLLEMNIS.name == "LUDUS_SOLLEMNIS"
        assert FestivalType.LUDUS_ANNIVERSARIUS.name == "LUDUS_ANNIVERSARIUS"
