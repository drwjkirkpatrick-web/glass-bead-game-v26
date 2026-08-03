"""Tests for src/play_modes.py — Private vs. Public Play distinction."""

import pytest
from src.play_modes import (
    PlayMode,
    PrivatePlay,
    PublicPlay,
    ProgressionChecklist,
    PlayerProgression,
)


class TestPrivatePlay:
    def test_mode_is_private(self):
        pp = PrivatePlay(player_name="Tito")
        assert pp.mode is PlayMode.PRIVATE

    def test_make_move_no_scoring(self):
        pp = PrivatePlay(player_name="Tito")
        record = pp.make_move("Theme from Bach", contemplation_done=True)
        assert pp.moves_made == 1
        assert record["contemplated"] is True
        assert pp.contemplation_minutes == 5.0

    def test_experiment_no_penalty_for_failure(self):
        pp = PrivatePlay(player_name="Tito")
        pp.experiment("wild counterpoint", success=False)
        assert pp.experiments_attempted == 1
        assert pp.experiments_succeeded == 0
        assert len(pp.history) == 1

    def test_contemplate_negative_minutes_raises(self):
        pp = PrivatePlay(player_name="Tito")
        with pytest.raises(ValueError, match="non-negative"):
            pp.contemplate(-5)

    def test_eligibility_heuristic(self):
        pp = PrivatePlay(player_name="Tito")
        assert not pp.is_eligible_for_public
        for _ in range(10):
            pp.make_move("move")
        pp.contemplate(60)
        assert pp.is_eligible_for_public


class TestPublicPlay:
    def test_requires_public_mode(self):
        with pytest.raises(ValueError, match="PUBLIC_"):
            PublicPlay(
                player_name="Knecht",
                public_mode=PlayMode.PRIVATE,
                magister_name="Magister Waldzell",
            )

    def test_requires_magister(self):
        with pytest.raises(ValueError, match="Magister"):
            PublicPlay(
                player_name="Knecht",
                public_mode=PlayMode.PUBLIC_CEREMONIAL,
                magister_name="",
            )

    def test_make_move_increments_score(self):
        pub = PublicPlay(
            player_name="Knecht",
            public_mode=PlayMode.PUBLIC_FESTIVAL,
            magister_name="Magister Waldzell",
            audience_size=200,
        )
        pub.make_move("fugue exposition", contemplation_done=True, elegance=0.4)
        assert pub.moves_made == 1
        assert pub.elegance == 0.4
        assert pub.contemplative_depth > 0

    def test_overall_score_bounds(self):
        pub = PublicPlay(
            player_name="Knecht",
            public_mode=PlayMode.PUBLIC_TOURNAMENT,
            magister_name="Magister Monteport",
            audience_size=50,
        )
        pub.make_move("theme", elegance=1.0, fertility=1.0, surprise=1.0, recursion=1.0, contemplation_done=True)
        pub.make_move("counter-subject", elegance=1.0, fertility=1.0, surprise=1.0, recursion=1.0, contemplation_done=True)
        assert 0.0 <= pub.overall_score <= 1.0

    def test_meditation_too_short(self):
        pub = PublicPlay(
            player_name="Knecht",
            public_mode=PlayMode.PUBLIC_CEREMONIAL,
            magister_name="Magister Waldzell",
        )
        with pytest.raises(ValueError, match="at least one minute"):
            pub.perform_meditation(0)


class TestProgressionChecklist:
    def test_all_met_initially_false(self):
        cl = ProgressionChecklist()
        assert not cl.all_met

    def test_individual_gates(self):
        cl = ProgressionChecklist()
        cl.verify_moves(20)
        assert cl.moves_met
        cl.log_contemplation(5.0)
        assert cl.contemplation_met
        cl.add_endorsement("Peer A")
        cl.add_endorsement("Peer B")
        assert cl.endorsements_met
        cl.submit_for_magister_review(approved=True, notes="ready")
        assert cl.magister_met
        assert cl.all_met

    def test_duplicate_endorsement_ignored(self):
        cl = ProgressionChecklist()
        cl.add_endorsement("Peer A")
        cl.add_endorsement("Peer A")
        assert len(cl.endorsements) == 1

    def test_empty_peer_name_raises(self):
        cl = ProgressionChecklist()
        with pytest.raises(ValueError, match="named peer"):
            cl.add_endorsement("")

    def test_negative_contemplation_raises(self):
        cl = ProgressionChecklist()
        with pytest.raises(ValueError, match="negative"):
            cl.log_contemplation(-1)


class TestPlayerProgression:
    def test_starts_private(self):
        prog = PlayerProgression(player_name="Tito")
        assert prog.current_mode is PlayMode.PRIVATE
        assert not prog.is_public()

    def test_progression_blocks_when_unready(self):
        prog = PlayerProgression(player_name="Tito")
        with pytest.raises(RuntimeError, match="blocked"):
            prog.request_progression(PlayMode.PUBLIC_CEREMONIAL, magister_name="Magister Waldzell")

    def test_full_private_to_public_transition(self):
        prog = PlayerProgression(player_name="Tito")
        # satisfy private requirements
        for _ in range(20):
            prog.private_play.make_move("practice theme")
        prog.private_play.contemplate(300.0)  # 5 hours
        # endorsements
        prog.checklist.add_endorsement("Peer A")
        prog.checklist.add_endorsement("Peer B")
        # magister review
        prog.checklist.submit_for_magister_review(approved=True, notes="proceed")
        # transition
        public = prog.request_progression(
            PlayMode.PUBLIC_FESTIVAL,
            magister_name="Magister Waldzell",
            audience_size=500,
        )
        assert prog.is_public()
        assert prog.current_mode is PlayMode.PUBLIC_FESTIVAL
        assert public.audience_size == 500
        assert public.magister_name == "Magister Waldzell"

    def test_to_dict_snapshot(self):
        prog = PlayerProgression(player_name="Tito")
        snapshot = prog.to_dict()
        assert snapshot["player_name"] == "Tito"
        assert snapshot["current_mode"] == "PRIVATE"
        assert snapshot["is_public"] is False
        assert snapshot["progression"]["all_met"] is False
