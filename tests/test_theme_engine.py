"""
tests/test_theme_engine.py

Unit tests for the Bach-fugue compositional arc (src/theme_engine.py).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from theme_engine import (
    Theme, CounterSubject, Episode, Stretto, Coda,
    GlassBeadGameMove, FugueBuilder, FugueScorer,
)


# ───────────────────────────────────────────────────────────────
# Phase human-language thread tests
# ───────────────────────────────────────────────────────────────

class TestTheme:
    def test_human_thread(self):
        t = Theme(text="The Golden Ratio", domain="mathematics", motifs=["spiral", "growth"], voice_id=1)
        thread = t.human_thread()
        assert "Voice 1" in thread
        assert "The Golden Ratio" in thread
        assert "mathematics" in thread
        assert "spiral" in thread

    def test_defaults(self):
        t = Theme(text="Plain Theme")
        assert t.domain == "music"
        assert t.voice_id == 1
        assert t.motifs == []


class TestCounterSubject:
    def test_human_thread_direct(self):
        cs = CounterSubject(text="Retrograde canon", domain="music", voice_id=2, inversion=False)
        thread = cs.human_thread()
        assert "Voice 2" in thread
        assert "direct counterpoint" in thread
        assert "Retrograde canon" in thread

    def test_human_thread_inversion(self):
        cs = CounterSubject(text="Inverted answer", domain="mathematics", voice_id=2, inversion=True)
        thread = cs.human_thread()
        assert "inversion" in thread


class TestEpisode:
    def test_human_thread(self):
        ep = Episode(
            text="Free development",
            bridges=["music → mathematics", "mathematics → nature"],
            modulations=["C major → A minor"],
        )
        thread = ep.human_thread()
        assert "Episode" in thread
        assert "music → mathematics" in thread
        assert "C major → A minor" in thread


class TestStretto:
    def test_human_thread(self):
        st = Stretto(compression_ratio=0.5)
        st.add_entry(voice_id=1, text="T", domain="music", delay_beats=0)
        st.add_entry(voice_id=3, text="T'", domain="philosophy", delay_beats=2)
        thread = st.human_thread()
        assert "Stretto" in thread
        assert "2 overlapping" in thread
        assert "50%" in thread


class TestCoda:
    def test_human_thread(self):
        c = Coda(text="Unity", synthesis_domains=["music", "mathematics"], closing_motif="the One.")
        thread = c.human_thread()
        assert "Coda" in thread
        assert "Unity" in thread
        assert "music and mathematics" in thread
        assert "the One." in thread


# ───────────────────────────────────────────────────────────────
# Builder tests
# ───────────────────────────────────────────────────────────────

class TestFugueBuilder:
    def test_builder_basic(self):
        builder = FugueBuilder(player="Knecht")
        move = (
            builder
            .set_theme("The Golden Ratio", domain="mathematics", motifs=["spiral"])
            .set_counter_subject("A Bach canon", domain="music", against_motifs=["retrograde"], inversion=True)
            .set_episode("Exploration", bridges=["math → music"], modulations=["mod-1"])
            .set_stretto(compression_ratio=0.6)
            .add_stretto_entry("Unison", "philosophy", voice_id=3, delay_beats=1)
            .set_coda("Beauty", synthesis_domains=["mathematics", "music"], closing_motif="the eternal Atman")
            .build()
        )
        assert isinstance(move, GlassBeadGameMove)
        assert move.player == "Knecht"
        assert move.theme.text == "The Golden Ratio"
        assert move.counter_subject.inversion is True
        assert len(move.stretto.entries) == 1

    def test_builder_incomplete_raises(self):
        builder = FugueBuilder()
        builder.set_theme("Only theme")
        with pytest.raises(ValueError) as exc:
            builder.build()
        assert "Incomplete fugue move" in str(exc.value)

    def test_builder_fluent_add_bridge(self):
        builder = FugueBuilder(player="Tegularius")
        move = (
            builder
            .set_theme("Idea A")
            .set_counter_subject("Idea B")
            .add_episode_bridge("A → B")
            .add_episode_bridge("B → C")
            .set_stretto()
            .add_stretto_entry("E1", "music", 1)
            .add_stretto_entry("E2", "philosophy", 2)
            .set_coda("Synthesis")
            .build()
        )
        assert len(move.episode.bridges) == 2
        assert len(move.stretto.entries) == 2


# ───────────────────────────────────────────────────────────────
# Scoring tests
# ───────────────────────────────────────────────────────────────

class TestFugueScorer:
    def test_score_theme(self):
        scorer = FugueScorer()
        t = Theme(text="X", motifs=["m1", "m2"])
        s = scorer.score_theme(t)
        assert 0 <= s["elegance"] <= 1
        assert s["fertility"] > 0.5  # two motifs

    def test_score_counter_subject_inversion(self):
        scorer = FugueScorer()
        cs = CounterSubject(text="Y", domain="astronomy", inversion=True)
        s = scorer.score_counter_subject(cs)
        assert s["surprise"] > 0.6  # inversion + foreign domain

    def test_score_move_aggregate(self):
        scorer = FugueScorer()
        move = GlassBeadGameMove(
            move_id="m1",
            player="Test",
            theme=Theme("T"),
            counter_subject=CounterSubject("CS"),
            episode=Episode("E"),
            stretto=Stretto(entries=[{}], compression_ratio=0.5),
            coda=Coda("C"),
        )
        totals = scorer.score_move(move)
        for dim in FugueScorer.DIMENSIONS:
            assert dim in totals
            assert 0 <= totals[dim] <= 1
        assert move.total_score > 0

    def test_narrate_contains_all_phases(self):
        builder = FugueBuilder(player="Knecht")
        move = (
            builder
            .set_theme("T")
            .set_counter_subject("CS")
            .set_episode("E")
            .set_stretto()
            .add_stretto_entry("S", "music", 1)
            .set_coda("C")
            .build()
        )
        narration = move.narrate()
        assert "Theme" in narration
        assert "CounterSubject" in narration or "CounterSubject" in narration.replace(" ", "")
        assert "Episode" in narration
        assert "Stretto" in narration
        assert "Coda" in narration
        assert "Total score" in narration


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
