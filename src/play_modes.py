"""
glass-bead-game-v26 — Private vs. Public Play Distinction

"To this day everyone is free to play the Game privately, and young people
are encouraged... But the great public Games, the Ludus sollemnis and the
Ludus anniversarius..."

— Hesse, *Das Glasperlenspiel* (p. 1358-1361)

A Player begins in Private play — a sandbox for contemplation and
experimentation without judgment.  Transition to Public play is earned
through verified mastery, deepened contemplation, peer endorsement, and
magister review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional


class PlayMode(Enum):
    """The two great domains of the Glass Bead Game."""
    PRIVATE = auto()             # sandbox, no scoring
    PUBLIC_CEREMONIAL = auto()   # formal match, single player
    PUBLIC_TOURNAMENT = auto()   # competitive match, ranked
    PUBLIC_FESTIVAL = auto()     # cultural festival, audience present


# ---------------------------------------------------------------------------
# Private Play — sandbox, no scoring, contemplation encouraged
# ---------------------------------------------------------------------------

@dataclass
class PrivatePlay:
    """
    Free, unjudged play where a player explores the Game in silence.
    No audience, no scores, no formal requirements.  Contemplation
    and experimentation are the only goals.
    """
    player_name: str
    moves_made: int = 0
    contemplation_minutes: float = 0.0
    experiments_attempted: int = 0
    experiments_succeeded: int = 0
    notes: str = ""
    history: List[Dict[str, object]] = field(default_factory=list)

    @property
    def mode(self) -> PlayMode:
        return PlayMode.PRIVATE

    def make_move(self, description: str, *, contemplation_done: bool = False) -> Dict[str, object]:
        """
        Record a move in private play.
        Moves are not scored — they are merely noted for later review.
        """
        self.moves_made += 1
        if contemplation_done:
            self.contemplation_minutes += 5.0
        record = {
            "move_index": self.moves_made,
            "description": description,
            "contemplated": contemplation_done,
            "mode": PlayMode.PRIVATE.name,
        }
        self.history.append(record)
        return record

    def experiment(self, description: str, success: bool = True) -> Dict[str, object]:
        """
        Attempt an experimental variation.  Failure carries no penalty.
        This is the heart of private play: freedom to explore.
        """
        self.experiments_attempted += 1
        if success:
            self.experiments_succeeded += 1
        record = {
            "type": "experiment",
            "description": description,
            "success": success,
        }
        self.history.append(record)
        return record

    def contemplate(self, minutes: float = 10.0) -> None:
        """
        Silent, formal meditation on the content and meaning of the Game.
        Contemplation is encouraged but not enforced in private play.
        """
        if minutes < 0:
            raise ValueError("Contemplation minutes must be non-negative.")
        self.contemplation_minutes += minutes

    @property
    def is_eligible_for_public(self) -> bool:
        """
        Private play eligibility heuristic.
        A player who has played thoughtfully and meditated deeply
        is likely ready — but formal progression requires the
        ProgressionChecklist.
        """
        return self.moves_made >= 10 and self.contemplation_minutes >= 60


# ---------------------------------------------------------------------------
# Public Play — scored, judged, ceremonial
# ---------------------------------------------------------------------------

@dataclass
class PublicPlay:
    """
    Formal public play: scored, judged by a Magister, with audience present.
    Requires verified meditation, peer endorsement, and magister approval.
    """
    player_name: str
    public_mode: PlayMode
    magister_name: str
    audience_size: int = 0

    # Scoring dimensions (0.0 – 1.0)
    elegance: float = 0.0
    fertility: float = 0.0
    surprise: float = 0.0
    recursion: float = 0.0
    contemplative_depth: float = 0.0

    moves_made: int = 0
    meditation_minutes: float = 0.0
    completed: bool = False
    history: List[Dict[str, object]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.public_mode not in {
            PlayMode.PUBLIC_CEREMONIAL,
            PlayMode.PUBLIC_TOURNAMENT,
            PlayMode.PUBLIC_FESTIVAL,
        }:
            raise ValueError("PublicPlay must use a PUBLIC_* mode.")
        if not self.magister_name or not self.magister_name.strip():
            raise ValueError("Public play requires a Ludi Magister presiding.")

    @property
    def mode(self) -> PlayMode:
        return self.public_mode

    @property
    def overall_score(self) -> float:
        """Weighted composite score for public play."""
        weights = (0.25, 0.20, 0.20, 0.20, 0.15)
        vals = (self.elegance, self.fertility, self.surprise, self.recursion, self.contemplative_depth)
        return round(sum(w * v for w, v in zip(weights, vals)), 3)

    def make_move(
        self,
        description: str,
        *,
        contemplation_done: bool = False,
        elegance: float = 0.0,
        fertility: float = 0.0,
        surprise: float = 0.0,
        recursion: float = 0.0,
    ) -> Dict[str, object]:
        """
        Record a scored move in public play.  Each move contributes
        to the aggregate dimensions judged by the Magister.
        """
        self.moves_made += 1
        if contemplation_done:
            self.meditation_minutes += 5.0
            self.contemplative_depth = min(1.0, self.contemplative_depth + 0.05)

        self.elegance = min(1.0, self.elegance + elegance)
        self.fertility = min(1.0, self.fertility + fertility)
        self.surprise = min(1.0, self.surprise + surprise)
        self.recursion = min(1.0, self.recursion + recursion)

        record = {
            "move_index": self.moves_made,
            "description": description,
            "contemplated": contemplation_done,
            "mode": self.public_mode.name,
        }
        self.history.append(record)
        return record

    def perform_meditation(self, minutes: int = 10) -> None:
        """Formal meditation required before certain moves in public play."""
        if minutes < 1:
            raise ValueError("Meditation must last at least one minute.")
        self.meditation_minutes += minutes
        self.contemplative_depth = min(1.0, self.contemplative_depth + minutes * 0.01)


# ---------------------------------------------------------------------------
# Progression — Transition from Private to Public
# ---------------------------------------------------------------------------

@dataclass
class ProgressionChecklist:
    """
    The four gates a player must pass to move from Private to Public play.
    Each gate is verified independently; all four must be satisfied.
    """
    # 1. Verified moves count
    required_moves: int = 20
    moves_verified: int = 0

    # 2. Contemplation hours
    required_contemplation_hours: float = 5.0
    contemplation_hours_logged: float = 0.0

    # 3. Peer endorsement
    required_endorsements: int = 2
    endorsements: List[str] = field(default_factory=list)

    # 4. Magister review
    magister_reviewed: bool = False
    magister_approved: bool = False
    magister_notes: str = ""

    @property
    def moves_met(self) -> bool:
        return self.moves_verified >= self.required_moves

    @property
    def contemplation_met(self) -> bool:
        return self.contemplation_hours_logged >= self.required_contemplation_hours

    @property
    def endorsements_met(self) -> bool:
        return len(self.endorsements) >= self.required_endorsements

    @property
    def magister_met(self) -> bool:
        return self.magister_reviewed and self.magister_approved

    @property
    def all_met(self) -> bool:
        return self.moves_met and self.contemplation_met and self.endorsements_met and self.magister_met

    def verify_moves(self, count: int) -> None:
        if count < 0:
            raise ValueError("Move count cannot be negative.")
        self.moves_verified = count

    def log_contemplation(self, hours: float) -> None:
        if hours < 0:
            raise ValueError("Contemplation hours cannot be negative.")
        self.contemplation_hours_logged += hours

    def add_endorsement(self, peer_name: str) -> None:
        if not peer_name or not peer_name.strip():
            raise ValueError("Endorsement requires a named peer.")
        if peer_name not in self.endorsements:
            self.endorsements.append(peer_name)

    def submit_for_magister_review(self, approved: bool, notes: str = "") -> None:
        self.magister_reviewed = True
        self.magister_approved = approved
        self.magister_notes = notes


class PlayerProgression:
    """
    Orchestrates the lifecycle of a player from Private to Public play.
    A player begins in Private and may request progression when ready.
    """

    def __init__(self, player_name: str) -> None:
        self.player_name = player_name
        self.private_play = PrivatePlay(player_name=player_name)
        self.checklist = ProgressionChecklist()
        self.public_play: Optional[PublicPlay] = None

    @property
    def current_mode(self) -> PlayMode:
        if self.public_play is not None:
            return self.public_play.mode
        return PlayMode.PRIVATE

    def is_public(self) -> bool:
        return self.public_play is not None

    def update_from_private(self) -> None:
        """
        Synchronize the progression checklist with the player's
        accumulated private-play statistics.
        """
        self.checklist.verify_moves(self.private_play.moves_made)
        self.checklist.log_contemplation(self.private_play.contemplation_minutes / 60.0)

    def request_progression(
        self,
        target_mode: PlayMode,
        magister_name: str,
        *,
        audience_size: int = 0,
    ) -> PublicPlay:
        """
        Attempt to transition from Private to a Public play mode.
        Raises RuntimeError if the progression checklist is incomplete.
        """
        if target_mode == PlayMode.PRIVATE:
            raise ValueError("Cannot 'progress' to Private play.")
        self.update_from_private()
        if not self.checklist.all_met:
            missing = []
            if not self.checklist.moves_met:
                missing.append("verified moves")
            if not self.checklist.contemplation_met:
                missing.append("contemplation hours")
            if not self.checklist.endorsements_met:
                missing.append("peer endorsements")
            if not self.checklist.magister_met:
                missing.append("magister approval")
            raise RuntimeError(f"Progression blocked — missing: {', '.join(missing)}")

        self.public_play = PublicPlay(
            player_name=self.player_name,
            public_mode=target_mode,
            magister_name=magister_name,
            audience_size=audience_size,
        )
        return self.public_play

    def to_dict(self) -> Dict[str, object]:
        return {
            "player_name": self.player_name,
            "current_mode": self.current_mode.name,
            "is_public": self.is_public(),
            "private_moves": self.private_play.moves_made,
            "private_contemplation_minutes": self.private_play.contemplation_minutes,
            "progression": {
                "moves_met": self.checklist.moves_met,
                "contemplation_met": self.checklist.contemplation_met,
                "endorsements_met": self.checklist.endorsements_met,
                "magister_met": self.checklist.magister_met,
                "all_met": self.checklist.all_met,
            },
        }
